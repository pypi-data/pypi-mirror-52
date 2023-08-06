from setuptools import setup

def readme():
    with open('README.md') as f:
        return f.read()


setup(name='pymoondb',
      version='0.1',
      description='Accessing the MoonDB lunar sample database',
      url='https://www.ict.inaf.it/gitlab/alessandro.frigeri/pymoondb',
      author='Alessandro Frigeri',
      author_email='Alessandro.Frigeri@inaf.it',
      license='MIT',
      packages=['moondb'],
      install_requires=[
          'markdown',
          'requests',
          'urllib3'
      ],
      zip_safe=False)
