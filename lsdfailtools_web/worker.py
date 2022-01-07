from .application import celery, db, mail
from .config import Config
from .models import Run, RunState
from flask import render_template
from flask_mail import Message
from pathlib import Path
import subprocess


@celery.task
def runLSDFailtools(runid, rundir, coords, rain, outname, url):
    run = Run.query.filter_by(id=runid).one_or_none()
    if run is None:
        raise RuntimeError(f'no such run {runid}')

    run.status = RunState.running
    db.session.commit()
    rundir = Path(rundir)

    error_msg = ''
    try:
        subprocess.run([Config.LSDFAILTOOL, str(rundir) + '/',
                        '-c', coords, '-p', rain,
                        '-f', Config.LSDFAILTOOL_CFG],
                       check=True, stdout=subprocess.PIPE,
                       stderr=subprocess.STDOUT)
        run.status = RunState.complete
    except Exception as e:
        error_msg = e.stdout.decode('utf-8')
        run.status = RunState.failed

    db.session.commit()

    # send mail
    if run.status == RunState.complete:
        msg = Message(f'run {run.id} complete', sender=Config.ADMIN,
                      recipients=[run.user.email])
        msg.body = render_template('email/run_complete.txt', run=run,
                                   download=url)
        msg.html = render_template('email/run_complete.html', run=run,
                                   download=url)
    elif run.status == RunState.failed:
        msg = Message(f'run {run.id} failed', sender=Config.ADMIN,
                      recipients=[run.user.email])
        msg.body = render_template('email/run_failed.txt', run=run,
                                   error=error_msg)
        msg.html = render_template('email/run_failed.html', run=run,
                                   error=error_msg)
    mail.send(msg)
