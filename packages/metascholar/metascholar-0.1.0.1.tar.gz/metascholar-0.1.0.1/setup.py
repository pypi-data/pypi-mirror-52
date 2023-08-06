from setuptools import setup, find_packages

setup(
    name='metascholar',
    version='0.1.0.1',
    packages=find_packages(exclude=['tests*']),
    license='GNU',
    description='A package to retrieve Scholarly Metadata',
    long_description=open('README.md').read(),
    install_requires=['numpy'],
    url='https://github.com/ameyakarnad/metascholar',
    author='Edlab',
    author_email='ak4251@columbia.edu'
)
