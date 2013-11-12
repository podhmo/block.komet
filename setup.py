from setuptools import setup, find_packages
import sys
import os

py3 = sys.version_info.major >= 3

version = '0.0'

requires = [
    "setuptools",
    "zope.interface",
]

tests_require = [
    "sqlalchemy",
    "pyramid",
]

long_description = "\n".join(open(f).read() for f in  ["README.rst", "CHANGES.txt"])


setup(name='block.komet',
      version=version,
      description="REST framework?",
      long_description=long_description,
      classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.3",
        "Framework :: Pyramid",
        ],
      keywords='',
      author='podhmo',
      url='',
      license='MIT',
      packages=find_packages('src'),
      package_dir = {'': 'src'},
      namespace_packages=['block'],
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      tests_require=tests_require,
      extras_require={
          "testing": tests_require,
      },
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
