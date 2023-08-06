from setuptools import setup

def readme():
    with open('README.md') as f:
        return f.read()

# The text of the README file
README = (open("README.md")).read()

setup(name='pymoondb',
      version='0.1.rc1',
      description='A python module to access the MoonDB, the geochemical and petrological lunar sample database',
      url='https://www.ict.inaf.it/gitlab/alessandro.frigeri/pymoondb',
      author='Alessandro Frigeri',
      author_email='Alessandro.Frigeri@inaf.it',
      long_description=README,
      long_description_content_type="text/markdown",
      license='MIT',
      packages=['moondb'],
      install_requires=[
          'markdown',
          'requests',
          'urllib3'
      ],
      zip_safe=False)
