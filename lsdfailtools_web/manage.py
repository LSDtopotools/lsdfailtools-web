from .application import db
from .config import Config
import argparse
from pathlib import Path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--init-db', action='store_true',
                        default=False, help="initialise database")

    args = parser.parse_args()
    basedir = Path(Config.BASEDIR)

    if not basedir.exists():
        basedir.mkdir(parents=True)

    if args.init_db:
        db.create_all()


if __name__ == '__main__':
    main()
