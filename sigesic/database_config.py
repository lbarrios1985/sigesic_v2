# coding=utf-8
DATABASES_CONFIG = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
<<<<<<< HEAD
        'NAME': 'sigesic_v2',
        'USER': 'postgres',
        'PASSWORD': 'admin8080',
=======
        'NAME': '<DB_NAME>',
        'USER': '<DB_USER>',
        'PASSWORD': '<DB_PASSWORD>',
>>>>>>> e5d8860b544215e3b22c67b63195ca1747ea208a
        'HOST': 'localhost',
        'PORT': '5432',
        'ATOMIC_REQUESTS': True, # Crea transacciones en cada peticion de la vista
    }
}