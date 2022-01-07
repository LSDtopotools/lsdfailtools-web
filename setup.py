from setuptools import setup, find_packages


name = 'lsdfailtools-web'
version = '0.1'
release = '0.1.0'
author = 'Magnus Hagdorn'

setup(
    name=name,
    packages=find_packages(),
    version=release,
    include_package_data=True,
    install_requires=[
        "sqlalchemy",
        "flask>=1.0",
        "flask_sqlalchemy",
        "flask-login",
        "oauthlib",
        "pyOpenSSL"
    ],
    extras_require={
        'lint': [
            'flake8>=3.5.0',
        ],
    },
    entry_points={
        'console_scripts': [
            'lsdfailtools-manage=lsdfailtools_web.manage:main',
        ]
    },
    author=author,
    description="web application for running lsdfailtools",
)
