from .application import celery, db
from .models import Run, RunState
import time
from pathlib import Path


@celery.task
def runLSDFailtools(runid, rundir, inname, outname):
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
