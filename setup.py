from setuptools import setup, find_packages

with open('README.md', 'r') as f:
    LONG_DESCRIPTION = f.read()

VERSION = '1.0.1' 
DESCRIPTION = 'Python package to interact with Houseparty\'s API.'

setup(
        name='houseparty', 
        version=VERSION,
        author='Miles Rack',
        author_email='milesr4@protonmail.com',
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        long_description_content_type='text/markdown',
        url='https://github.com/milesrack/houseparty',
        license='MIT',
        packages=find_packages(),
        install_requires=['requests'],
        keywords=['python', 'houseparty', 'api', 'houseparty-app'],
        classifiers=[
            'Intended Audience :: Developers',
            'Programming Language :: Python',
            'Programming Language :: Python :: 3.9',
        ]
)
