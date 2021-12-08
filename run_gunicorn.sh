export FLASK_APP=lsdfailtools_web
export SCRIPT_NAME=/lsdfailtools
export FLASK_ENV=development

. secret.sh

gunicorn --log-level debug --bind 0.0.0.0:5000 lsdfailtools_web:app

