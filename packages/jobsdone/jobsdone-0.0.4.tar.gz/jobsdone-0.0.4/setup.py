import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "jobsdone",
    version = "0.0.4",
    author = "Tyler Williams",
    author_email = "williams.tyler@gmail.com",
    description = ("A little helper to send you a push when your job"
                                   " finishes running."),
    license = "MIT",
    keywords = "alert commandline tool",
    url = "http://packages.python.org/jobsdone",
    packages=['jobsdone'],
    scripts=['jobsdone/jd'],
    long_description=read('README.md'),
    long_description_content_type="text/markdown",
    install_requires=[
      'appdirs',
      'requests',
    ],
    python_requires=">=3.3",
)
