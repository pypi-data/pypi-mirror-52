import os
from setuptools import find_packages, setup

readme_file = os.path.join(os.path.dirname(__file__), 'README.md')
with open(readme_file) as readme:
    README = readme.read()

os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-squirrel',
    version='0.2.9',
    packages=find_packages(),
    include_package_data=True,
    license='BSD License',  # TODO: Read about..
    description='Background workers based on rabbit-mq integration.',
    long_description=README,
    long_description_content_type='text/markdown',
    url='https://gitlab.com/jo-salgado/django-squirrel',
    author='Jose Salgado',
    author_email='jose.salgado.wrk@gmail.com',
    install_requires=['jsonschema',
                      'requests',
                      'Django',
                      'pika',
                      'arrow',
                      ],
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 2.2',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',  # TODO: Read about..
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
