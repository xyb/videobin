# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4
# Written 2009 by j@mailb.org

import os
from os.path import join
from django.conf import global_settings 

PROJECT_ROOT = os.path.normpath(os.path.dirname(__file__))

# Django settings for videobin project.

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'dev.sqlite',
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/Berlin'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = join(PROJECT_ROOT, 'media')
STATIC_ROOT = join(PROJECT_ROOT, 'static')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/media/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/admin/media/'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    #'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
)

ROOT_URLCONF = 'videobin.urls'

TEMPLATE_DIRS = (
    join(PROJECT_ROOT, 'templates'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.humanize',
    'south',

    'videobin.bin',
    'videobin.video',
    'videobin.session',
)

FILE_UPLOAD_PERMISSIONS=0644

SESSION_COOKIE_NAME = "vbk"
SESSION_COOKIE_AGE = 86400000

#videobin related settings
CONTACT_EMAIL="feedback@videobin.org"
ANNOUNCE_URL="udp://tracker.openbittorrent.com:80"
TORRENT_COMMENT='http://videobin.org'

TRANSMISSON_HOST='localhost'
TRANSMISSON_PORT=9091
TRANSMISSON_USER='transmission'
TRANSMISSON_PASSWORD='transmission'

SHARE_RAW_TORRENT = True
SEED_RAW_TORRENT = False

XACCELREDIRECT = False
XSENDFILE = False

#overwrite default settings with local settings
try:
    from local_settings import *
except ImportError:
    pass

# Make this unique, creates random key first at first time.
#SECRET_KEY = '245on223al1=87lg9kf%%m1%pwky&bu8so6r&az)l076gdftg4'
try:
    SECRET_KEY
except NameError:
    SECRET_FILE = os.path.join(PROJECT_ROOT, 'secret.txt')
    try:
        SECRET_KEY = open(SECRET_FILE).read().strip()
    except IOError:
        try:
            from random import choice
            SECRET_KEY = ''.join([choice('abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)') for i in range(50)])
            secret = file(SECRET_FILE, 'w')
            secret.write(SECRET_KEY)
            secret.close()
        except IOError:
            Exception('Please create a %s file with random characters to generate your secret key!' % SECRET_FILE)

