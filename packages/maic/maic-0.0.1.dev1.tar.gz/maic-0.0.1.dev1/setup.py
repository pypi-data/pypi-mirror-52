from setuptools import setup

setup(
    name='maic',
    version='0.0.1.dev1',
    description='Test framework for ee-book',
    url='https://bitbucket.org/ee-book/maic',
    author='knarfeh',
    author_email='knarfeh@outlook.com',
    license='MIT',

    classifiers=[
        'Development Status :: 3 - Alpha',

        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    keywords='E2E Test SQLAlchemy',
    packages=['maic'],
    install_requires=[
        'psycopg2',
        'simplejson',
        'SQLAlchemy',
        'requests-futures',
        'requests',
        'futures',
        'pytz'
    ]
)
