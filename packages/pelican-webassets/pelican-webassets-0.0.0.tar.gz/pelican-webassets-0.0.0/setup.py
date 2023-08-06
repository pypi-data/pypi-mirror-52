from setuptools import setup
from io import open
import os

pwd = os.path.abspath(os.path.dirname(__file__))

description = open(os.path.join(pwd, 'readme.rst'), encoding='utf-8').read()

setup(
    name='pelican-webassets',
    packages=['pelican_webassets'],

    version=os.environ.get('CI_COMMIT_TAG', '0.0.0'),
    url='https://gitlab.com/bryanbrattlof/pelican-webassets',

    description="A Pelican plugin so you can use webassets",
    long_description=description,

    author='Bryan Brattlof',
    author_email='hello@bryanbrattlof.com',

    license='MIT',

    install_requires=['webassets'],

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 4 - Beta',

        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',

        'Framework :: Pelican',
        'Framework :: Pelican :: Plugins',

        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',

        'Natural Language :: English',
    ],
)
