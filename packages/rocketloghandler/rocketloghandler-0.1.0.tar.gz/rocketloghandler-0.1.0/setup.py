from setuptools import setup

setup(
    name='rocketloghandler',
    version='0.1.0',
    packages=['rocketloghandler'],
    url='https://mygit.th-deg.de/fwahl/rocketloghandler',
    license='MIT',
    author='Florian Wahl',
    author_email='florian.wahl@gmail.com',
    description='Send python logs to RocketChat server.',
    install_requires = ["rocketchat-API>=0.6.34"]
)
