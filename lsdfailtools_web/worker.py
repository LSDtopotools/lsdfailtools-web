import requests

from .application import celery, db
from .config import Config
from .models import Run, RunState
from pathlib import Path
import subprocess


@celery.task
def runLSDFailtools(runid, rundir, coords, rain, outname):
    run = Run.query.filter_by(id=runid).one_or_none()
    if run is None:
        raise RuntimeError(f'no such run {runid}')

    run.status = RunState.running
    db.session.commit()
    rundir = Path(rundir)

    try:
        subprocess.run([Config.LSDFAILTOOL, str(rundir) + '/',
                        '-c', coords, '-p', rain,
                        '-f', Config.LSDFAILTOOL_CFG],
                       check=True, stdout=subprocess.PIPE,
                       stderr=subprocess.STDOUT)
        run.status = RunState.complete
    except Exception:
        run.status = RunState.failed

    db.session.commit()

    requests.get(
        Config.WORK_END_ENDPOINT + str(run.id) + '/' + str(run.status)
    )
