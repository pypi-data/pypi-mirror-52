from setuptools import setup

setup(
    name='pockethernet',
    version='0.1.1',
    packages=['pockethernet'],
    url='https://gitlab.com/MartijnBraam/pockethernet-protocol',
    license='MIT',
    author='Martijn Braam',
    author_email='martijn@brixit.nl',
    description='Library and command line client for the Pockethernet network tester',
    long_description=open("pockethernet/README.rst").read(),
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Operating System :: POSIX :: Linux',
    ],
    install_requires=[
        'cobs',
        'crc16'
    ],
    entry_points={
        'console_scripts': [
            'pockethernet=pockethernet.__main__:main'
        ]
    }
)
