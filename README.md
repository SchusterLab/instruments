# instruments

## Important

- This module should have only external dependency on publicly available modules. For example, no dependency on private Schuster Lab packages.
- Each instrument should be inside a sub folder. This makes it easy to attach a `README.md` for that instrument.
- Each instrument should have a `<instrument_name>_test.py` file.
   - this test file should have a function called `api_test(instrument_instance)` that tests the low-level apis.
   - behavioral tests should be in a second function, and should be separate from the low-level api tests.
   - a test `instrument.cfg` file is included in each folder, and excluded from version control in `.gitignore`, to allow developers to have their own instrument.cfg during development.
- Each instrument should have a `README.md` file. It should be sweet and useful.

## How to Use

There are two ways to install this instrument driver collection.

### 1. from github

do: `pip install git+git://github.com/SchusterLab/instruments.git@master`
![pip install from git](pip_install_from_git.png)

### 2. from pip

do `pip install instruments`

### 3. for local development

- First, clone this repository with
   ```shell
   git clone https://github.com/SchusterLab/instruments.git
   ```

- Then inside your github `instruments` folder, do `pip install -e .`. The `.` at the end tells `pip` that you are passing the entire local folder in. This is equivalent to `python setup.py develop`. See here: [stackoverflow](http://stackoverflow.com/questions/2087148/can-i-use-pip-instead-of-easy-install-for-python-setup-py-install-dependen).

## To Contribute:

The benefit of building instrument drivers this way, is that it allows us to have a README for each driver, and a consistent testing convention.

To help fix bugs and create new drivers, and help make everyone's life easier in the lab, I ask you the following:

1. Always write tests for your code.
2. Write up the README nicely, so that the first-year in your lab knows how to use this.

### How to Run Test?

to run test, just use the PyCharm integration and run the test file in each folder.

Many thanks to you future contributors in advance!

Ge Yang