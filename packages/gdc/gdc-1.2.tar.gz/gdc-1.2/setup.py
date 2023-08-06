from setuptools import setup
from os.path import join

setup(name="gdc",
version="1.2",
description="Skills management software for french secondary teachers",
url="https://bitbucket.org/chpalmann/gdc",
author="Christophe Palmann",
author_email="cpn.math@gmail.com",
license="BSD-2-Clause",
packages = ['gdc'],
package_data = {'gdc':["logo.png"]},
install_requires=['cycler==0.10.0','kiwisolver==1.1.0','matplotlib==3.1.1','numpy==1.17.0','Pillow==6.1.0','pyparsing==2.4.2','PyPDF2==1.26.0','python-dateutil==2.8.0','reportlab==3.5.23','six==1.12.0','xlrd==1.2.0'],
entry_points={'console_scripts': ['gdc=gdc.__main__:main']},
zip_safe=False)
