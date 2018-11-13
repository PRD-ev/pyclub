from flask import render_template, request, url_for, redirect, session, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from pyclub.dbconnect import create_user, confirm_email, get_user, create_organization, get_all_organization_names, get_organization_by_name, create_club, create_club_membership, get_club, get_club_by_organization, create_event, get_club_membership
from werkzeug.security import generate_password_hash, check_password_hash
from email_confirmation import confirm_token, send_email_authentication
from main import app


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login_page"
login_manager.login_message = "Zaloguj się aby uzyskać dostęp"

@login_manager.user_loader
def load_user(user_id):
    return get_user(user_id)


@app.route("/")
def index_page():
    return render_template("index.html")


@app.route("/register/", methods = ["POST", "GET"])
def register_page():
    error_message = None
    if request.method == "POST":
        new_email = request.form['email']
        new_password = request.form['password']
        new_password_confirm = request.form['password_confirm']
        new_first_name = request.form['name']
        new_last_name = request.form['last_name']
        if new_email and new_password and new_first_name and new_last_name and new_password == new_password_confirm and '@' in new_email:
            new_password = generate_password_hash(new_password)
            create_user(new_first_name, new_last_name, new_email, new_password)
            send_email_authentication(new_email)
            return redirect(url_for('index_page'))
        elif '@' not in new_email:
            error_message = "Email musi zawierać znak @"
        elif new_password != new_password_confirm:
            error_message = "Hasła muszą się zgadzać"
        else:
            error_message = "Uzupełnij wszystkie pola"
    return render_template("register.html", error = error_message)


@app.route("/login/", methods = ["POST", "GET"])
def login_page():
    error_message = None
    if request.method == "POST":
        attempted_email = request.form['email']
        attempted_password = request.form['password']
        user_dict = get_user(str(attempted_email))
        if user_dict is None:
            error_message = 'Użytkownika nie ma w systemie'
        else:
            db_password = user_dict.get('password')
            if check_password_hash(db_password, attempted_password):
                login_user(get_user(attempted_email))
                flash('Logged in successfully.')
                return redirect(url_for('index_page'))
            error_message = "Nieprawidłowe hasło"
    return render_template("login.html", error = error_message)


@app.route("/profile/add_organization/", methods = ["POST", "GET"])
@login_required
def add_organization_page():
    if request.method == 'POST':
        new_organization_name = request.form['organization_name']
        new_organization_contact = request.form['organization_contact']
        all_organization_list = get_all_organization_names()
        if new_organization_name and new_organization_contact:
            if new_organization_name not in all_organization_list: 
                create_organization(new_organization_name, new_organization_contact)
                return redirect(url_for('profile_page'))
            flash('Istnieje już organizacje o podanej nazwie')
        else:    
            flash('Fill in all the fields')
    return render_template('add_organization.html')
            

@app.route("/organizations/")
def get_all_organization_page():
    organization_list = get_all_organization_names()
    return render_template('organizations.html', list = organization_list)  


@app.route('/organizations/<organization_name>/')
@login_required
def organization_page(organization_name):
    organization_dict = get_organization_by_name(organization_name)
    current_organization_contact = organization_dict.get('contact')
    current_organization_name = organization_dict.get('name')
    current_organization_id = organization_dict.get('idorganization')
    current_organization_club_list = get_club_by_organization(current_organization_id)
    return render_template('organization_profile.html', name = current_organization_name, contact = current_organization_contact, list = current_organization_club_list)

@app.route('/organizations/<organization_name>/new_club/', methods = ["POST", "GET"])
@login_required
def add_club_page(organization_name):
    if request.method == 'POST':
        organization_dict = get_organization_by_name(organization_name)
        parent_organization = organization_dict.get('idorganization')
        new_club_name = request.form["club_name"]
        new_club_info = request.form["club_info"]
        if parent_organization and new_club_info:
            create_club(new_club_info, parent_organization, new_club_name)
            club_dict = get_club(new_club_name)
            new_club_id = club_dict.get('idclub')
            create_club_membership(current_user.id,new_club_id)
            return redirect(url_for('organization_page', organization_name=organization_name))
    return render_template('add_club.html', parent_name=organization_name)


@app.route('/organizations/<organization_name>/<club_name>/')
def club_page(organization_name, club_name):
    current_club_dict = get_club(club_name)
    current_club_info = current_club_dict.get('info')
    return render_template('club_profile.html', club_name=club_name, info=current_club_info,organization_name=organization_name)

@app.route('/organizations/<organization_name>/<club_name>/join/')
def clun_join_page(organization_name, club_name):
    current_club_dict = get_club(club_name)
    current_club_id = current_club_dict.get('idclub')
    club_members = get_club_membership(current_club_id)
    if current_user.id in club_members:
        flash('Należysz już do klubu')
    else:
        create_club_membership(current_user.id,current_club_id)
    return redirect(url_for('club_page', organization_name=organization_name, club_name=club_name))


@app.route('/organizations/<organization_name>/<club_name>/new_event/', methods=["POST", "GET"])
def new_event_page(organization_name, club_name):
    if request.method == 'POST':
        current_club_dict = get_club(club_name)
        current_club_id = current_club_dict.get('idclub')
        print(current_club_id)
        new_event_date = request.form['event_date']
        new_event_date = new_event_date.split('T')
        new_event_date = new_event_date[0] + " " + new_event_date[1] + ":00"
        print(new_event_date)
        new_event_info = request.form['event_info']
        if new_event_date and new_event_info and current_club_id:
            create_event(new_event_date, new_event_info, current_club_id)
    return render_template('add_event.html', organization_name=organization_name, club_name=club_name)

@app.route('/test/')
def test():
    xist = get_all_organization_names()
    x = str(xist)
    return x


@app.route('/logout/')
def logout():
    logout_user()
    return redirect(url_for('index_page'))


@app.route("/contact/")
def contact_page():
    return render_template("contact.html")


@app.route("/about/")
def about_page():
    return render_template("about.html")

@app.route("/profile/")
@login_required
def profile_page():
    return render_template("profile.html")


@app.route("/activate/<confirmation_token>/")
def activate_account(confirmation_token):
        mail = confirm_token(confirmation_token)
        confirm_email(mail)
        return redirect(url_for('index_page'))


#error handlers

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404notfound.html'), 404


@app.errorhandler(500)
def server_error(e):
    return render_template('505server_error.html')


if __name__ == "__main__":
    app.run(host = app.config["HOST"], port = app.config["PORT"], debug=app.config["DEBUG"])
