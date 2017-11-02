import requests
import google.oauth2.credentials
import googleapiclient.discovery
import google_auth_oauthlib.flow
from flask import (render_template, url_for, redirect,
                    session, jsonify, request)
from .. import auth
import models
from forms import UserRegisterForm, LogInForm
from flask_login import login_user, login_required, logout_user

CLIENT_SECRETS_FILE = 'client_secret.json'
SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']
API_SERVICE_NAME = 'drive'
API_VERSION = 'v2'

@auth.route('/')
def main():
    if 'credentials' not in session:
        login_form = LogInForm()
        return render_template("auth/main.html", form=login_form)
    else:
        credentials = google.oauth2.credentials.Credentials(
            **session['credentials']
        )
        drive = googleapiclient.discovery.build(
            API_SERVICE_NAME, API_VERSION, credentials=credentials
        )
        files = drive.files().list().execute()
        session['credentials'] = credentials_to_dict(credentials)
        return jsonify(**files)


@auth.route('/login', methods=['GET', 'POST'])
def google_login():
    form = LogInForm()
    if form.validate_on_submit():
        login_email = form.email.data + '@mahidol.edu'
        session['login_email'] = login_email
        print(session['login_email'])
    else:
        login_email = None
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(CLIENT_SECRETS_FILE, scopes=SCOPES)
    flow.redirect_uri = url_for('auth.oauth2callback', _external=True)
    authorization_url, state = flow.authorization_url(
            access_type='offline',
            include_granted_scopes='true',
            login_hint=login_email
        )
    session['state'] = state
    return redirect(authorization_url)


@auth.route('/oauth2callback')
def oauth2callback():
    state = session['state']
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, scopes=SCOPES, state=state
    )
    flow.redirect_uri = url_for('auth.oauth2callback', _external=True)
    authorization_response = request.url
    flow.fetch_token(authorization_response=authorization_response)
    # save these credentials in a persistent database instead
    credentials = flow.credentials
    session['credentials'] = credentials_to_dict(credentials)
    return redirect(url_for('auth.weblogin'))


@login_required
@auth.route('/weblogin')
def weblogin():
    print(session.keys())
    if 'credentials' in session and 'login_email' in session:
        user = models.Person.query.filter_by(email=session['login_email']).first()
        login_user(user, True)
        return redirect('/')
    else:
        return 'Error! no credentials or email for logging in.'


@login_required
@auth.route('/weblogout')
def weblogout():
    if 'credentials' in session:
        del session['credentials']
    if 'login_email' in session:
        del session['login_email']
    logout_user()
    return redirect(url_for('auth.main'))

@auth.route('/revoke')
def revoke():
    if 'credentials' not in session:
        return ('You need to authorize before testing the credentials.')
    credentials = google.oauth2.credentials.Credentials(**session['credentials'])
    revoke = requests.post('https://accounts.google.com/o/oauth2/revoke',
        params={'token': credentials.token},
        headers={'content-type': 'application/x-www-form-urlencoded'})
    status_code = getattr(revoke, 'status_code')
    if status_code == 200:
        return ('Credentials successfully revoked.')
    else:
        return ('An error occured.')


def credentials_to_dict(credentials):
    return {'token': credentials.token,
            'refresh_token': credentials.refresh_token,
            'token_uri': credentials.token_uri,
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret,
            'scopes': credentials.scopes
            }

@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = UserRegisterForm()
    if form.validate_on_submit():
        firstname_en = form.firstname_en.data
        email = form.email.data
        form.firstname_en.data = ''
        return jsonify([{'name': firstname_en, 'email': email}])
    return render_template('auth/user_register.html', form=form)