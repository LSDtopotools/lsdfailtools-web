from .application import db
import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--init-db', action='store_true',
                        default=False, help="initialise database")

    args = parser.parse_args()

    if args.init_db:
        db.create_all()


if __name__ == '__main__':
    main()
