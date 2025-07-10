# This is my setup.py file for the Interception project.
# It includes the necessary metadata and dependencies for the project.
from setuptools import setup, find_packages

setup(
    name='interception',
    version='0.1.0',
    author='Omar Haweel',
    packages=find_packages(),
    install_requires=[
        'numpy>=1.21.0',
        'matplotlib>=3.5.0',
        'scipy>=1.7.0',
        'pytest>=6.2.0',
        'bandit>=1.7.0',
        'safety>=1.10.0',
        'memory-profiler>=0.60.0',
        'psutil>=5.8.0',
        'pyinstaller>=5.0.0',
    ],
)