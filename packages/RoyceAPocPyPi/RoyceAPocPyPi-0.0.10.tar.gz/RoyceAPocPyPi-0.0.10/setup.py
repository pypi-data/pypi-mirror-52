from setuptools import setup, find_packages
from setuptools.command.install import install
import distutils.cmd
import distutils.log   
import subprocess

class PostInstallCommand(install):
    """Post-installation for installation mode."""
    def run(self):
        print("PRINT ROYCE ASSOCIATES HVA")
        subprocess.check_call(["echo", "ROYCE ASSOCIATES HVA"])
        install.run(self)

setup_args = dict(
    cmdclass={'install': PostInstallCommand,},
    name='RoyceAPocPyPi',
    version='0.0.10',
    description='HVA',
    license='MIT',
    packages=find_packages(),
    author='Daniel van den Bosch',
    author_email='daniel-vd-bosch@hotmail.com',
    keywords=['test'],
)

if __name__ == '__main__':
    setup(**setup_args)
