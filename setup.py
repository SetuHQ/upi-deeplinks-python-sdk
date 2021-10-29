from setuptools import setup

with open("README.md", "r") as fh:
    README = fh.read()

setup(
    name='setu',
    version='0.7.0',
    url='https://github.com/SetuHQ/setu-python-sdk',
    author='Setu',
    author_email='dev.support@setu.co',
    description="SDK to help Pythonistas integrate with Setu's APIs",
    long_description=README,
    long_description_content_type="text/markdown",
    license='MIT',
    install_requires=[
        "requests==2.26.0",
        "PyJWT==2.3.0",
    ],
    packages=['setu'],
    zip_safe=False,
)
