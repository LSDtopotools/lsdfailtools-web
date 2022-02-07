from .application import app, db
from .dec import authorized, ACTUAL_USER_KEY
from .models import User, Run, RunState, jsonify_run
from .config import Config
from .worker import runLSDFailtools

from flask import flash, send_file
from flask import request, redirect, url_for
import json
from pathlib import Path
import uuid
import datetime


@app.route('/new', methods=['GET', 'POST'])
@authorized
def new(*args, **kwargs):
    actual_user = kwargs[ACTUAL_USER_KEY]
    key_user = actual_user['sub']
    user_db = User.query.filter_by(id=key_user).one_or_none()
    if user_db is None:
        user = User(
            id=key_user,
            name=actual_user['preferred_username'],
            email=(actual_user['email']
                   if hasattr(actual_user, 'email') else None)
        )
        db.session.add(user)
    else:
        user = user_db

    basedir = Path(Config.BASEDIR)

    coords = 'coords.csv'
    rain = 'rain.csv'

    if request.files['Coordinates'] and request.files['Precipitation']:

        run = Run(id=uuid.uuid4(), submitted=datetime.datetime.now(),
                  status=RunState.new, user=user)

        rundir = basedir / str(run.id)
        rundir.mkdir()

        request.files['Coordinates'].save((rundir / coords).open('wb'))
        request.files['Precipitation'].save((rundir / coords).open('wb'))

        db.session.add(run)
        db.session.commit()

        flash('Document uploaded successfully.')
        runLSDFailtools.delay(
            run.id, str(rundir), coords, rain,
            Config.RESULT_NAME
        )
        return {"run_id": str(run.id)}, 200, {}
    else:
        return ("You must attach 'Coordinates' and 'Precipitation' files!",
                400, {})

        return redirect(url_for('index'))


@app.route('/<ruid>/download')
@authorized
def download(*args, **kwargs):
    run = Run.query.filter_by(id=kwargs['ruid']).one_or_none()
    if run is None:
        return "Run not found", 404, {}
    if run.status != RunState.complete:
        return "Run not finished yet!", 400, {}
    return send_file(
        str(Path(Config.BASEDIR, str(run.id), Config.RESULT_NAME)),
        as_attachment=True)


@app.route('/run-list')
@authorized
def run_list(*args, **kwargs):
    actual_user = kwargs[ACTUAL_USER_KEY]
    runs = Run.query.filter_by(user_id=actual_user['sub']).all()
    print(json.dumps(jsonify_run(runs)))
    return json.dumps(jsonify_run(runs)), 200, {}
