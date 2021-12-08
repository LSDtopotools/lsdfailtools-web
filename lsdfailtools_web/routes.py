from .application import app, db, login_manager
from .forms import UploadDataForm
from .models import User, Run, RunState
from .config import Config

from flask_login import current_user, login_user, logout_user, login_required
from flask import render_template, flash
from flask import request, redirect, url_for
import requests
import json
from oauthlib.oauth2 import WebApplicationClient
from pathlib import Path
import uuid
import datetime

# OAuth 2 client setup
client = WebApplicationClient(Config.GOOGLE_CLIENT_ID)

# Flask-Login helper to retrieve a user from our db
@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).one()


@app.route('/')
@app.route('/index')
def index():
    if current_user.is_authenticated:
        runs = current_user.runs
    else:
        runs = []

    return render_template('index.html', user=current_user, runs=runs)


@app.route('/new', methods=['GET', 'POST'])
@login_required
def new():
    form = UploadDataForm()
    basedir = Path(Config.BASEDIR)
    if form.validate_on_submit():

        run = Run(id=uuid.uuid4(), submitted=datetime.datetime.now(),
                  status=RunState.new, user=current_user)

        rundir = basedir / str(run.id)
        rundir.mkdir()

        form.lsddata.data.save((rundir / 'data.csv').open('wb'))

        db.session.add(run)
        db.session.commit()

        flash('Document uploaded successfully.')

        return redirect(url_for('index'))

    return render_template('new.html', user=current_user, form=form)


def get_google_provider_cfg():
    return requests.get(Config.GOOGLE_DISCOVERY_URL).json()


@app.route("/login")
def login():
    # Find out what URL to hit for Google login
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]

    # Use library to construct the request for Google login and provide
    # scopes that let you retrieve user's profile from Google
    # make sure the scheme is https to allow it to work behind a proxy
    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=(
            request.base_url.replace('http://', 'https://') + "/callback"),
        scope=["openid", "email", "profile"],
    )
    return redirect(request_uri)


@app.route("/login/callback")
def callback():
    # Get authorization code Google sent back to you
    code = request.args.get("code")

    # Find out what URL to hit to get tokens that allow you to ask for
    # things on behalf of a user
    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]

    # Prepare and send a request to get tokens! Yay tokens!
    # make sure the scheme is https to allow it to work behind a proxy
    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url.replace('http://', 'https://'),
        redirect_url=request.base_url.replace('http://', 'https://'),
        code=code
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(Config.GOOGLE_CLIENT_ID, Config.GOOGLE_CLIENT_SECRET),
    )

    # Parse the tokens!
    client.parse_request_body_response(json.dumps(token_response.json()))

    # Now that you have tokens (yay) let's find and hit the URL
    # from Google that gives you the user's profile information,
    # including their Google profile image and email
    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)

    # You want to make sure their email is verified.
    # The user authenticated with Google, authorized your
    # app, and now you've verified their email through Google!
    if userinfo_response.json().get("email_verified"):
        unique_id = userinfo_response.json()["sub"]
        users_email = userinfo_response.json()["email"]
        picture = userinfo_response.json()["picture"]
        users_name = userinfo_response.json()["given_name"]
    else:
        return "User email not available or not verified by Google.", 400

    # Create a user in your db with the information provided
    # by Google
    user = User.query.filter_by(id=unique_id).one_or_none()
    if user is None:
        # User does not exist in DB so create them
        user = User(
            id=unique_id,
            name=users_name,
            email=users_email,
            profile_pic=picture)
        db.session.add(user)
        db.session.commit()

    # Begin user session by logging the user in
    login_user(user)

    # Send user back to homepage
    return redirect(url_for("index"))


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))
