from .application import celery, db, mail
from .config import Config
from .models import Run, RunState
from flask import render_template
from flask_mail import Message
import time
from pathlib import Path


@celery.task
def runLSDFailtools(runid, rundir, inname, outname, url):
    run = Run.query.filter_by(id=runid).one_or_none()
    if run is None:
        raise RuntimeError(f'no such run {runid}')

    run.status = RunState.running
    db.session.commit()
    rundir = Path(rundir)
    out = rundir / outname
    time.sleep(10)

    with out.open('w') as o:
        o.write('hello world')

    run.status = RunState.complete
    db.session.commit()

    # send mail
    msg = Message(f'run {run.id} complete', sender=Config.ADMIN,
                  recipients=[run.user.email])
    msg.body = render_template('email/run_complete.txt', run=run, download=url)
    msg.html = render_template('email/run_complete.html', run=run,
                               download=url)
    mail.send(msg)
