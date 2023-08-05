from setuptools import setup

setup(
    name='dpflow',
    version='110',
    description='',
    url='',
    author='lixzcisb',
    author_email='lixzcisb@outlook.com',
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
    packages=['dpflow'],
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
