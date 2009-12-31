cd `pwd`
set PYTHONPATH=..;.;$PYTHONPATH
set DJANGO_SETTINGS_MODULE=ianalyse.settings
python c:\python26\scripts\django-admin.py  syncdb
python c:\python26\scripts\django-admin.py runserver
