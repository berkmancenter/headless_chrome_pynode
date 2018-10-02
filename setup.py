from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
        name='headlesschrome',
        version='0.2.0',
        description='A tiny wrapper around a node module for screenshotting and HAR capturing',
        packages=find_packages(),
        )
