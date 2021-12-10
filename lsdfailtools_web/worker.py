from .application import celery
import time
from pathlib import Path


@celery.task
def runLSDFailtools(rundir, inname, outname):
    rundir = Path(rundir)
    out = rundir / outname
    time.sleep(10)

    with out.open('w') as o:
        o.write('hello world')
