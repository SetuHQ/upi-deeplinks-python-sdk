import pathlib
from setuptools import setup

HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()

setup(name='setu',
      version='0.4.2',
      url='https://github.com/SetuHQ/setu-python-sdk',
      author='Gandharva B',
      author_email='gandharva@setu.co',
      description="SDK to help Pythonistas integrate with Setu's APIs",
      long_description=README,
      long_description_content_type="text/markdown",
      license='MIT',
      install_requires=["requests", "uuid", "PyJWT"],
      packages=['setu'],
      zip_safe=False)
