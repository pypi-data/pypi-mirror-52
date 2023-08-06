from setuptools import setup, find_packages

with open('requirements.txt', 'r') as f:
    requirements = f.readlines()

setup(
    name = 'dialect',
    version = '0.1.4',
    author = 'Alex Covington',
    author_email = 'alex@covington.tech',
    url = 'https://github.com/ACov96/dialect/tree/master',
    packages = find_packages(),
    license = 'MIT',
    entry_points = {
        'console_scripts': [
            'dialect = dialect.__main__:main',
        ],
    },
    install_requires = requirements,
)
