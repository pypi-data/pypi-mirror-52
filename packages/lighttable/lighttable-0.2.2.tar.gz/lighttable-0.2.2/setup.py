from setuptools import find_packages, setup, Extension
import pathlib
# The directory containing this file

setup(name='lighttable',
      version='0.2.2',
      description='light pivot feature engineer',
      url='http://github.com/fe/lightpivot2',
      author='fefly',
      author_email='fefly@gmail.com',
      license='MIT',
      include_package_data=True,
      packages=['lighttable'],
      zip_safe=False)
