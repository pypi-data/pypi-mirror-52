from setuptools import setup, find_packages

setup(name='secret-manager',
      version='0.0.2',
      license='MIT',
      author='Praveen Kumar',
      author_email='praveen.k@blackbuck.com',
      url="https://github.com/BLACKBUCK-LABS/secret-manager-python",
      description='Secret Manager AWS',
      packages=find_packages(exclude=['tests']),
      long_description=open('README.md').read(),
      zip_safe=False)
