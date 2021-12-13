export FLASK_APP=lsdfailtools_web
export SCRIPT_NAME=/lsdfailtools
export SERVER_NAME=www.geos.ed.ac.uk
export FLASK_ENV=development
export MAIL_SERVER=localhost
export MAIL_PORT=8025

. secret.sh

gunicorn --log-level debug --bind 0.0.0.0:5000 lsdfailtools_web:app

