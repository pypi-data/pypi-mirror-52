# coding: utf-8

"""
    Felix' Website mit Blog
    The api of my blog.

    Contact: felix@felix-scholz.org
"""


from setuptools import setup, find_packages

import website_python_client

NAME = 'felix-scholz-website-python-client'
VERSION = website_python_client.__version__

setup(
    name=NAME,
    version=VERSION,
    license='MIT',
    description="Felix Website - Api-Client",
    author='Felix Scholz',
    author_email="felix@felix-scholz.org",
    url="http://www.felix-scholz.com/",
    keywords=['API', 'Website', 'Felix', 'Scholz', 'REST', 'Client'],
    install_requires=[
        "certifi==2019.9.11",
        "chardet==3.0.4",
        "idna==2.8",
        "python-dateutil==2.8.0",
        "requests==2.22.0",
        "six==1.12.0",
        "urllib3==1.25.3"],
    packages=find_packages(exclude=['test', '*.test', 'test.*', '*.test.*']),
    include_package_data=True,
    long_description="""\
    The python api client for my website.
    """
)
