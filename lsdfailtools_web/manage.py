from .application import db
from .config import Config
from .models import Run
import argparse
from pathlib import Path
import datetime
import shutil
import logging

NDAYS = 10


def main():
    logging.basicConfig(level=logging.INFO)

    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--init-db', action='store_true',
                       default=False, help="initialise database")
    group.add_argument('--remove-old', '-r', nargs='?', type=int,
                       const=NDAYS, metavar='N',
                       help="remove entries older than N days, "
                       f"default: {NDAYS}")

    args = parser.parse_args()
    basedir = Path(Config.BASEDIR)

    if not basedir.exists():
        basedir.mkdir(parents=True)

    if args.init_db:
        db.create_all()
    elif args.remove_old is not None:
        old = datetime.datetime.now() - datetime.timedelta(
            days=args.remove_old)
        for run in Run.query.filter(Run.submitted < old):
            logging.info(f'removing run {run.id}')
            rundir = basedir / str(run.id)
            if rundir.exists():
                logging.debug(f'deleting directory {rundir}')
                try:
                    shutil.rmtree(rundir)
                except OSError as e:
                    logging.error(f"Error: {rundir} : {e}")
            db.session.delete(run)
            db.session.commit()


if __name__ == '__main__':
    main()
