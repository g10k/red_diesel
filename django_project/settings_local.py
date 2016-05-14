DEBUG = True
ADMINS = []


DATABASES = {
    'default': {
        # 'ENGINE': 'django.db.backends.postgresql_psycopg2',
        # 'ENGINE': 'django.db.backends.sqlite3',
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'rd',
        'USER': 'root',
        'PASSWORD': '0123',
        'HOST': 'localhost',
        'PORT': '',
    }
}