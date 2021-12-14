#
# Regular cron jobs for the lsdfailtools-web package
#
0 4	* * *	root	[ -x /usr/bin/lsdfailtools-web_maintenance ] && /usr/bin/lsdfailtools-web_maintenance
