import pathlib
from setuptools import setup

HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()

setup(name='setu',
      version='0.4.1',
      url='https://gitlab.com/setu-lobby/seu-pypi',
      author='Gandharva B',
      author_email='gandharva@setu.co',
      description="Setu's own SDK for faster integration",
      long_description=README,
      long_description_content_type="text/markdown",
      license='MIT',
      install_requires=["requests", "uuid", "PyJWT"],
      packages=['setu'],
      zip_safe=False)