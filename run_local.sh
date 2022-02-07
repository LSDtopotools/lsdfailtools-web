export FLASK_APP=lsdfailtools_web
export WORK_END_ENDPOINT=https://foresee.cloudev.it/api/integration/ed/finish/work/
export OAUTH_ENDPOINT=https://foresee-auth.cloudev.it/auth/realms/Foresee/protocol/openid-connect/userinfo

flask run --cert=adhoc
