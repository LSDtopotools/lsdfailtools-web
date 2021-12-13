export FLASK_APP=lsdfailtools_web
export MAIL_SERVER=localhost
export MAIL_PORT=8025
. secret.sh

flask run --cert=adhoc
