from setuptools import setup, find_packages

setup(
    name='MarketVisor',
    version='0.1.0',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'marketvisor = marketvisor.main:main'
        ]
    },
    install_requires=[
        'yfinance',
        'rich',
        'argparse',
        'pandas'
    ],
    author='Nexusrev',
    author_email='nramirez@arkadiaanalytics.com',
    description='A simple CLI tool to fetch and display stock data using yfinance.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/nexusrev/MarketVisor',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
)
