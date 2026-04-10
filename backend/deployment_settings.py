import os
import dj_database_url
from .settings import BASE_DIR

ALLOWED_HOST = [os.environ.get('RENDER_EXTERNAL_HOSTNAME')]
CSRF_TRUSTED_ORGINS = ['https://'+os.environ.get('RENDER_EXTERNAL_HOSTNAME')]

DEBUG = False
SECRET_KEY = os.environ.get('SECRET_KEY')

# CORS_ALLOWED_ORGINS =[
#     'http://localhost:5173'
# ]

STORAGES ={
    "default":{
        "BACKEND" :"django.core.files.storage.FilesSystemStorage"
    },
    "staticfiles":{
        "BACKEND" :"whitenoise.storage.CompressedStaticFilesStorage",
    }
}

DATABASES ={
    "default" : dj_database_url.config(
        default= os.environ['DATABASE_URL'],
        conn_max_age=600
    )
}