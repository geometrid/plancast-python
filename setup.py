from distutils.core import setup

try:
    import simplejson
except ImportError:
    import json

long_description = open('README.markdown').read()

setup(
    name='plancast',
    version='0.1',
    py_modules=['plancast'],
    description='A Python wrapper for the Plancast API.',
    author='Bartek Ciszkowski',
    author_email='bart.ciszk@gmail.com',
    license='BSD License',
    url='http://github.com/bartek/plancast-python',
    long_description=long_description,
    platforms=["any"],
)
