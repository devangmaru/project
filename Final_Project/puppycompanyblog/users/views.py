from flask import render_template, url_for, flash, redirect, request, Blueprint,jsonify
from flask_login import login_user, current_user, logout_user, login_required
from puppycompanyblog import db
from sqlalchemy.exc import IntegrityError
from wtforms.validators import ValidationError
from werkzeug.security import generate_password_hash,check_password_hash
from puppycompanyblog.models import User, BlogPost
from puppycompanyblog.users.forms import RegistrationForm, LoginForm, UpdateUserForm
from puppycompanyblog.users.picture_handler import add_profile_pic


users = Blueprint('users', __name__)

@users.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            flash('Username already exists.', 'error')
        else:
            user = User(email=form.email.data,
                        username=form.username.data,
                        password=form.password.data)

            db.session.add(user)
            db.session.commit()
            flash('Thanks for registering! Now you can login!')
            return redirect(url_for('users.login'))
    for field, errors in form.errors.items():
        for error in errors:
            flash(f"Error in {getattr(form, field).label.text}: {error}")
    return render_template('register.html', form=form)

    
@users.route('/login', methods=['GET', 'POST'])
def login():

    form = LoginForm()
    if form.validate_on_submit():
        # Grab the user from our User Models table
        user = User.query.filter_by(email=form.email.data).first()

        # Check that the user was supplied and the password is right
        # The verify_password method comes from the User object
        # https://stackoverflow.com/questions/2209755/python-operation-vs-is-not

      #  if user.check_password(form.password.data) and user is not None:
        if user is not None and user.check_password(form.password.data):
            #Log in the user

            login_user(user)
            flash('Logged in successfully.')

            # If a user was trying to visit a page that requires a login
            # flask saves that URL as 'next'.
            next = request.args.get('next')

            # So let's now check if that next exists, otherwise we'll go to
            # the welcome page.
            if next == None or not next[0]=='/':
                next = url_for('core.index')

            return redirect(next)
    return render_template('login.html', form=form)




@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('core.index'))


@users.route("/account", methods=['GET', 'POST'])
@login_required
def account():

    form = UpdateUserForm()

    if form.validate_on_submit():
        print(form)
        if form.picture.data:
            username = current_user.username
            pic = add_profile_pic(form.picture.data,username)
            current_user.profile_image = pic

        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('User Account Updated')
        return redirect(url_for('users.account'))

    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

    profile_image = url_for('static', filename='profile_pics/' + current_user.profile_image)
    user = current_user
    page = request.args.get('page', 1, type=int)
    blog_posts = BlogPost.query.filter_by(user_id=current_user.id).order_by(BlogPost.date.desc()).paginate(page=page, per_page=5)

    return render_template('account.html', user=user, profile_image=profile_image, blog_posts=blog_posts, form=form)



@users.route("/<username>")
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    blog_posts = BlogPost.query.filter_by(author=user).order_by(BlogPost.date.desc()).paginate(page=page, per_page=5)
    return render_template('user_blog_posts.html', blog_posts=blog_posts, user=user)
    
 
@users.route('/list')
def listall():
    return render_template('list.html',user= User.query.all())

@users.route('/delete_user/<int:user_id>',methods=['DELETE'])
def delete_user(user_id):
    try:
        # Fetch the user by ID
        user = User.query.get(user_id)

        if not user:
            return jsonify({"error": "User not found"}), 404

        # Disassociate all blog posts from this user
        for post in user.posts:
            post.user_id = None

        # Delete the user
        db.session.delete(user)
        db.session.commit()

        return jsonify({"message": "User deleted successfully"}), 200
    except IntegrityError as e:
        print("IntegrityError:", e)
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

    

 
 
