cd `pwd`
export PYTHONPATH=..:.:$PYTHONPATH
export DJANGO_SETTINGS_MODULE=ianalyse.settings
django-admin.py runserver --noreload
