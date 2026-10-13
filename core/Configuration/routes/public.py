from flask import render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user

from core.Configuration.models import User, uploadLog
from core.extensions import db
from core.Configuration.decorators import permission_level_required
from flask import render_template, flash, url_for, redirect

from core.Configuration import bp


@bp.route("/")
def Index():
    return render_template("Configuration/public/index.html")

@bp.route('/login')
def Login():
    if current_user.is_authenticated:
        flash("You're already logged in, silly goose.", "info")
        return redirect(url_for('Configuration.Index'))
    return render_template('Configuration/public/login.html')

@bp.route('/login', methods=['POST'])
def Login_POST():
    username = request.form.get('username')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter(User.username.ilike(username)).first()

    # check if user actually exists
    # take the user supplied password, hash it, and compare it to the hashed password in database
    if not user or not check_password_hash(user.password, password):  # type: ignore
        flash('Please check your login details and try again.')
        return redirect(url_for('Configuration.Login')) # if user doesn't exist or password is wrong, reload the page

    # if the above check passes, then we know the user has the right credentials
    login_user(user, remember=remember)
    user.set_image_link()
    return redirect(url_for('Configuration.Index'))

@bp.route('/signup')
def Signup():
    return render_template('Configuration/public/signup.html')


@bp.route('/signup', methods=['POST'])
def Signup_POST():
    name = request.form.get('username')
    password = request.form.get('password')
    confirmedPassword = request.form.get('confirmpassword')
    
    problems = []
    if not password or len(password) < 8:
        problems.append("Password must be at least 8 characters long.")
    
    if not name or len(name) < 3:
        problems.append("Username must be at least 3 characters long.")
    
    if password != confirmedPassword:
        problems.append("Passwords must match, please try again.")
        
    user = User.query.filter(User.username.ilike(name)).first() # if this returns a user, then the email already exists in database
    if name and user != None: # if a user is found, we want to redirect back to signup page so user can try again  
        problems.append("Username already exists, please choose a new one.")

    if len(problems) > 0:
        for problem in problems:
            flash(problem, "info")
        return redirect(url_for('Configuration.Signup'))
    
    # create new user with the form data. Hash the password so plaintext version isn't saved.
    new_user = User(username=name, password=generate_password_hash(password, method='pbkdf2:sha256')) # type: ignore
    if User.query.count() < 1:
        new_user.permissions = 100
    else:
        new_user.permissions = 10
    new_user.staffRole = ""
    new_user.maintainerStatus = ""

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()
    uploadLog(new_user, "User", "signed up.", None)
    flash(f"User successfully created! Please Login.", "info")
    return redirect(url_for('Configuration.Login'))


@bp.route('/resetpass')
@permission_level_required(0)
def ResetPass():
    return render_template('Configuration/public/resetpass.html')


@bp.route('/resetpass', methods=['POST'])
@permission_level_required(0)
def ResetPass_POST():
    password = request.form.get('password')
    confirmedPassword = request.form.get('confirmpassword')
    
    problems = []
    if not password or len(password) < 8:
        problems.append("Password must be at least 8 characters long.")
    
    if password != confirmedPassword:
        problems.append("Passwords must match, please try again.")
        
    
    if len(problems) > 0:
        for problem in problems:
            flash(problem, "info")
        return redirect(url_for('Configuration.ResetPass'))
    

    current_user.password = generate_password_hash(password, method='pbkdf2:sha256') # type: ignore
    db.session.commit()
    uploadLog(current_user, "User", "reset their password.", current_user.id)
    flash(f"Password reset.", "info")
    return redirect(url_for('Configuration.Index'))


@bp.route('/logout')
@login_required
def Logout():
    logout_user()
    return redirect(url_for('_Shared.Index'))

@bp.route('/setbio', methods=["GET"])
@permission_level_required(10)
def SetBio():
    return render_template('Configuration/public/setBio.html')

@bp.route('/setbio', methods=["POST"])
@permission_level_required(10)
def SetBio_POST():
    niceRequest = request.form.to_dict()

    current_user.bio = niceRequest["Bio"]

    db.session.commit()
    
    return redirect(url_for("Configuration.SetBio"))