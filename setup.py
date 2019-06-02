from setuptools import setup

setup(
    name='django_vega',
    author='Jaco du Plessis',
    author_email='jaco@jacoduplessis.co.za',
    description='Work with Vega in your Django project.',
    url='https://github.com/jacoduplessis/django-vega',
    keywords='django vega altair',
    package_data={
        'django_vega': [
            'static/django_vega/*.js',
            'templates/django_vega/*.html'
        ]
    },
    version='0.1.0',
    packages=['django_vega'],
    install_requires=[
        'websockets',
        'altair',
    ],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
)
