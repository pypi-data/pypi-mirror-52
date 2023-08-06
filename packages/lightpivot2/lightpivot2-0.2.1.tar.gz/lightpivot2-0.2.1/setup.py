from setuptools import find_packages, setup, Extension
import pathlib
# The directory containing this file

setup(name='lightpivot2',
      version='0.2.1',
      description='light pivot feature engineer',
      url='http://github.com/fe/lightpivot2',
      author='fefly',
      author_email='fefly@gmail.com',
      license='MIT',
      include_package_data=True,
      packages=['lightpivot2'],
      zip_safe=False)
