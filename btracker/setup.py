"""Setup configuration for Transaction Fraud Service"""

from setuptools import setup, find_packages

setup(
    name='btracker',
    version='1.0',
    description='Betting tracker',
    author='Jonas V',
    license='MIT',
    packages=find_packages(),
    package_data={
        '': ['*.yaml', '*.yml'],
    },
    install_requires=[],
    entry_points={
        'console_scripts': [
            'run-deploy = app:run_deploy',
            'run-local = app:run_local'
        ]
    }
)
