from setuptools import setup, find_packages

def readme():
    with open('README.md') as f:
        return f.read()

setup(
    name="padivinanza",
    version="0.2",
    description="Una adivinanza",
    url='http://github.com/julvez/padivinanza',
    long_description=readme(),
    packages=find_packages(),
    entry_points={
        'console_scripts': ['adivinanza=padivinanza.adivina:main']
    },
    author="Jorge Julvez",
    author_email="julvez@unizar.es",
    license="GNU GENERAL PUBLIC LICENSE",
    keywords="advinanzas riddles",
)
