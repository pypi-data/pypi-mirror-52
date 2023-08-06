## About 
This repo is for practicing package creating and publishing on pypi


## Install Locally 

### Install Editable 
``` bash
pip install -e . 
```
This command will search the setup.py in the current folder and install it. <br/>
"-e" means it will not copy the source but create a link to the package. Therefore, if there is any change in source, the installed package will simultaneously be changed.

### Install Tar.gz
```bash
pip install <path/to/the/tar.gz>
```
This command will install package using tar.gz file. It is the way how `pip` installs global package under the hood. 

## Create Distribution
### Create tar.gz 
``` bash
python setup.py sdist 
```
### Create Wheel
``` bash
python setup.py bdist_wheel 
```

## Upload to Pypi
Here we need third-party library `twine` to help on this part. <br/>
The twine documentation: https://pypi.org/project/twine/

### Step 1. Install Twine
``` bash
pip install twine
```
### Step 2. Upload 
```
twine upload --repository-url <url_to_upload> <the_distributions_files>
```
* `<url_to_upload>` can either be the official pypi: https://upload.pypi.org/legacy/ or pypi for testing: https://test.pypi.org/legacy/. <br/>
Please be aware that pypi for testing need different pypi account.

* `<the_distribution_files>` can usually be "dist/*" 

## Delete Package On Pypi
login to the Pypi.org and use website interface.

## make CLI 
please reference: https://python-packaging.readthedocs.io/en/latest/command-line-scripts.html

Making long story short, there are two ways to do it. It is recommended to use `console_script` entry point because the other way may cause error on Window system.
