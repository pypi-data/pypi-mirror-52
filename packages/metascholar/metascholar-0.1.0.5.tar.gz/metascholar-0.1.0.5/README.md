# metascholar
A Package to retrieve Scholarly Metadata


Before merging the code and creating the package, make sure you run the main function to execute the tests. 


## How to create/update a pip packages

- update setup.py to increase the version of package
- Run "python setup.py sdist" to create the package
- Run "twine upload -r pypi dist/{package name}" to upload the package. Enter your credentials to upload to pip
- Once uploaded to pip, upload to the Github site