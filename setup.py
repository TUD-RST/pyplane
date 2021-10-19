import os
import platform
from setuptools import setup, find_packages

with open("requirements.txt") as requirements_file:
    requirements = requirements_file.read()

if platform.system() == 'Linux':    
    setup(
        name='PyPlane',
        version='2.0.0',
        license='GPLv3',
        url='https://github.com/TUD-RST/pyplane',
        author='Klemens Fritzsche, Jan Winkler, Carsten Knoll',
        author_email='firstname.lastname@tu-dresden.de',
        description='Tool for phase plane analysis of second order dynamical systems (Qt-based)',
        packages=find_packages(),
        include_package_data=True,
        install_requires=requirements,
        entry_points={'console_scripts': ['pyplane=pyplane.app:run']},
        data_files=['packaging/linux/pyplane.desktop',
                    'packaging/linux/pyplane.metainfo.xml'
        ]
    )
else:
    setup(
        name='PyPlane',
        version='2.0.0',
        license='GPLv3',
        url='https://github.com/TUD-RST/pyplane',
        author='Klemens Fritzsche, Jan Winkler, Carsten Knoll',
        author_email='firstname.lastname@tu-dresden.de',
        description='Tool for phase plane analysis of second order dynamical systems (Qt-based)',
        packages=find_packages(),
        include_package_data=True,
        install_requires=requirements,
        entry_points={'console_scripts': ['pyplane=pyplane.app:run']},
        data_files=[]
    )
