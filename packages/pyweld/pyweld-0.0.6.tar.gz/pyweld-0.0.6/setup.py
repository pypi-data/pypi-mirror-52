import os
import platform
import shutil
import subprocess

import setuptools.command.build_ext as _build_ext
from setuptools import setup, Distribution
from setuptools.command.develop import develop
from setuptools.extension import Extension

is_develop_command = False
class build_ext(_build_ext.build_ext):
    def run(self):
        pass

    def move_file(self, filename, directory):
        source = filename
        dir, name = os.path.split(source)        
        destination = os.path.join(self.build_lib + "/" + directory + "/", name)
        shutil.copy(source, destination)

class Develop(develop):
    def run(self):
        global is_develop_command
        is_develop_command = True
        develop.run(self)

    def move_file(self, filename, directory):
        source = filename
        dir, name = os.path.split(source)
        destination = os.path.join(directory + "/", name)
        print("Copying {} to {}".format(source, destination))
        shutil.copy(source, destination)

class BinaryDistribution(Distribution):
    def has_ext_modules(self):
        return True

setup(name='pyweld',
      version='0.0.6',
      packages=['weld'],
      cmdclass={"build_ext": build_ext, "develop": Develop},
      distclass=BinaryDistribution,
      url='https://github.com/weld-project/weld',
      author='Weld Developers',
      author_email='weld-group@lists.stanford.edu')
