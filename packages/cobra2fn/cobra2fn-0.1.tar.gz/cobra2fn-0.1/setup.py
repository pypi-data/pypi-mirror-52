from setuptools import setup, find_packages

def readme():
    with open('README.md') as f:
        return f.read()

setup(
    name="cobra2fn",
    version="0.1",
    description="Transform a cobra model into a flexible net",
    url='https://bitbucket.org/Julvez/cobra2fn',
    long_description=readme(),
    packages=find_packages(),
    author="Jorge Julvez",
    author_email="fnyzer@unizar.es",
    license="GNU GENERAL PUBLIC LICENSE",
    keywords="cobra sbml flexible nets",
)
