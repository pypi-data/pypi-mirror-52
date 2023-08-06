"""Package definition for bb2cc."""

from distutils.core import setup

setup(
    name='bb2cc',
    version='0.4.0',
    url='https://bitbucket.org/dtao/bb2cc',
    license='MIT',
    author='Dan Tao',
    author_email='dtao@atlassian.com',
    description='Bitbucket to Confluence Cloud',
    py_modules=['bb2cc', 'cc'],
    scripts=['bin/bb2cc'],
    install_requires=[
        'requests==2.22.0',
        'mistune==0.8.4'
    ],
)
