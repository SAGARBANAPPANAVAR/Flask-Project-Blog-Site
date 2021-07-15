from flask import render_template, url_for, request, redirect, flash, Blueprint
from flask_login import login_user, logout_user, login_required, current_user
from companyblog import db
from companyblog.model import User, BlogPost
from companyblog.user.picture_handler import add_profile_pic
from companyblog.user.forms import Loginform, Register, UpdateUserForm

users = Blueprint('users',__name__)

#logout
@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('core.index'))

#Register
@users.route('/register', methods = ['POST','GET'])
def register():
    form = Register()

    if form.validate_on_submit():
        user = User(email=form.email.data,username=form.username.data,
                    password=form.password.data)

        db.session.add(user)
        db.session.commit()
        flash('Registration Successful')
        return redirect(url_for('users.login'))
    return render_template('register.html',form = form)

#login
@users.route('/login', methods = ['POST','GET'])
def login():
    form = Loginform()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user.check_password(form.password.data) and user is not None:
            login_user(user)
            flash('Login Successful')

            next = request.args.get('next')
            if next == None or next[0] == '/':
                next = url_for('core.index')

            return redirect(next)
    return render_template('login.html', form = form)

#Account
@users.route('/account', methods=['POST','GET'])
@login_required
def account():
    form = UpdateUserForm()
    if form.validate_on_submit():
        if form.picture.data:
            username = current_user.username
            pic = add_profile_pic(form.picture.data, username)
            current_user.profile_image = pic

        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Account Updated')

    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

    profile_image = url_for('static',filename='profile_pics/'+current_user.profile_image)
    return render_template('account.html', profile_image = profile_image, form = form)

#BlogPost
@users.route('/<username>')
def user_posts(username):
    page = request.args.get('pages',1, type = int)
    user = User.query.filter_by(username = username).first_or_404()
    blog_posts = BlogPost.query.filter_by(author=user).order_by(BlogPost.date.desc()).paginate(page=page,per_page=5)
    return render_template('user_blog.html',blog_posts=blog_posts, user=user)
