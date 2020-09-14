import os

DEBUG = False

SECRET_KEY = os.environ['DJANGO_SECRET_KEY']

#with open('/secret_key.txt') as f:
#    SECRET_KEY = f.read().strip()
