export PYTHONPATH=..:.:$PYTHONPATH
export DJANGO_SETTINGS_MODULE=ianalyse.settings
echo "please type the non-loopback(not 127.0.0.1 or 0.0.0.0) ip address of your machine:"
read ip
django-admin.py runserver --noreload $ip:8000
