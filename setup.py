import os
import sys
from setuptools import setup, find_packages

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

def runtests(args):
    "Run tests"
    import django
    from django.conf import settings
    from django.core.management import execute_from_command_line
    
    if not settings.configured:
        INSTALLED_APPS = [
            'django.contrib.auth',
            'django.contrib.admin',
            'django.contrib.sessions',
            'django.contrib.contenttypes',
            'django.contrib.messages',
            'tagulous',
            'tests',
        ]
        
        if django.VERSION < (1, 7):
            try:
                import south
            except ImportError:
                import warnings
                warnings.warn(
                    "south not installed, needed for tests for Django %s" % (
                        '.'.join(str(v) for v in django.VERSION)
                    ),
                    ImportWarning
                )
            else:
                INSTALLED_APPS += ['south']
        
        settings.configure(
            DATABASES={
                'default': {
                    'ENGINE': 'django.db.backends.sqlite3',
                }
            },
            INSTALLED_APPS=INSTALLED_APPS,
            MIDDLEWARE_CLASSES=[
                'django.middleware.common.CommonMiddleware',
                'django.contrib.sessions.middleware.SessionMiddleware',
                'django.contrib.auth.middleware.AuthenticationMiddleware',
                'django.contrib.messages.middleware.MessageMiddleware',
            ],
            ROOT_URLCONF='tests.tagulous_tests_app.urls',
        )
    
    execute_from_command_line(args[:1] + ['test'] + (args[2:] or ['tests']))


if len(sys.argv) > 1 and sys.argv[1] == 'test':
    runtests(sys.argv)
    sys.exit()

setup(
    name = "django-tagulous",
    version = "0.7.0",
    author = "Richard Terry",
    author_email = "code@radiac.net",
    description = ("A flexible tagging application for Django"),
    license = "BSD",
    keywords = "django tag tagging",
    url = "http://radiac.net/projects/django-tagulous/",
    long_description=read('README.rst'),
    classifiers=[
        'Development Status :: 4 - Beta',
        #'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Framework :: Django',
        'Framework :: Django :: 1.4',
        'Framework :: Django :: 1.5',
        'Framework :: Django :: 1.6',
    ],
    extras_require = {
        'dev':  ['tox', 'jasmine'],
        'i18n': ['unidecode'],
    },
    zip_safe=True,
    packages=find_packages(exclude=('tests*',))
)
