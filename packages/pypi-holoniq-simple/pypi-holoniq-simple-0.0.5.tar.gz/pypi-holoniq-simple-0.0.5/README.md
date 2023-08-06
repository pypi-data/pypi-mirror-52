# pypi-holoniq-simple

This is a simple python `PyPi` package template. The goal is to create and maintain 
a minimal project template that supports:

* VSCODE debugging
  
* Testing with pytest
  
* Painless publishing on [PyPi][pypi-home] with version management.

* Continuous integration with [Travis][travis-home]


There are many [cookiecutter][cookiecutter] template projects to choose from. The one
I used most prior to creating this template 
was [cookiecutter-pypackage-minimal][cookiecutter-pypackage-minimal]. Some templates have every conceivable 
option covered. My problem when using these is I find the vast number of questions 
daunting. I'm never quite sure which are important and those were the default option is OK. One false 
move and ... start all over again. Finally, when the cookiecutter spits out a project I've no
clue what all these files do and how they relate to the questions I've just
answered.

This template is simple, it covers the same ground as `cookiecutter-pypackage-minimal` but with 
the addition of support for versioning. You customise the template by making changes with simple 
edits. In doing so you take ownership, understand more about the distribution process and 
stay in control.

## Usage

    pip install -r requirements.txt
    python usage.py
    pytest

To modify the template for your project perform the following:

1. Change the package name in `setup.py`
   
        name="pypi-holoniq-simple",

2. Rename the `helloworld` package folder.
3. Edit the package reference in `usage.py`
4. Edit the package reference in `tests/test_helloworld.py`

As a sanity check, run:

    python usage.py
    pytest

Your done, well sort off. `Setup.py` has a stack of
ancillary fields, the following definitely need updating: `description`, `author`, 
`author_email`, `url`. You also need to change the the LICENSE file `Copyright (c) ...`

If you change the licence [type](https://choosealicense.com/), then in `setup.py` update the `license` 
and the License [classifier]((https://pypi.org/classifiers/)) fields:

```
    classifiers=[
        'License :: OSI Approved :: MIT License',
    ],
    ...
    license='MIT',
```

The `long_description` field in `setup.py` is the source for the project 
description that appears on PyPi. The template reads the contents
of `landing-page.md` into the long_description field. Landing-page.md can be as
long or as short as you want. Another option would be to read the long_description
from the projects `README.md`. If you want do this delete landing-page.md and
edit `setup.py`:

        long_description=read("README.md"),


You now have a publishable package. As a final sanity check build a PyPi source 
distribution manually:

    python setup.py sdist

This will list all the files that will be uploaded to PyPi and 
create a `tar.gz` distribution file in the `dist` folder. Examine the `tar.gz` 
distribution. You may need to create create a `MANIFEST.in` file if some 
files have been missed out. Have a read of [Adding Non-Code Files](https://python-packaging.readthedocs.io/en/latest/non-code-files.html) if you need to do this.

If all is well perform your first PyPi release, **[see below](#pypi-release)**.

## Testing

Add your tests to the `tests` folder. To run the tests:

    pytest

To debug the tests, add breakpoints and single step, launch the
tests in the `VSCODE` debugger using the `2. PyTest` launch configuration.

### Travis

A potential user will be more inclined to use your package if they can see it 
has tests and that these tests pass. [Travis][travis-home] is free for open source 
projects and easy to integrate into your development cycle. 

The file `travis.yaml` contains a [default](https://docs.travis-ci.com/user/languages/python/#default-build-script) Travis configuration for Python. Signing up with your gitHub account should be all that's 
needed. If you have no interest in Travis just delete this file.

## PyPi Release

Releasing the code is managed by the [invoke][invoke-home] script in `tasks.py` The
prerelease/release cycle bumps version tags to the git repository 
and PyPi release. On PyPi your project will hve a release history the looks something like
this: [history](https://pypi.org/project/dash-bootstrap-components/#history)

### Credentials

The release script will update gitHub and PyPi. In order to do this git will need
your gitHub credentials. Check you are able to issue git commands to gitHub from
the command line. If you're having problems have a look at:

* [gitcredentials ](https://git-scm.com/docs/gitcredentials)
* [Git does not remember username and password on Windows](https://snede.net/git-does-not-remember-username-password/)

Uploading to PyPi uses [twine](https://pypi.org/project/twine/). To register your credentials with
twine/keyring do the following:

    keyring set https://test.pypi.org/legacy/ your-username

And again

    keyring set https://test.pypi.org/legacy/ your-username

This doesn't appear to work on Windows, an alternative is to set your PyPi name & password 
using the environmental variables `TWINE_USERNAME` and `TWINE_PASSWORD`, [see](https://pypi.org/project/twine/).


### Prerelease

If you are aiming to release version `0.0.1`, the prerelease version will be `0.0.1-rc1`. This will 
automatically bump the version number and upload the release to PyPi.

    invoke prerelease 0.0.1-rc1

 In a clean virtual env, verify that you can install the new version and that it 
 works correctly with: 
 
    pip install pypi-holoniq-simple==0.0.1-rc1

If the manual installation tests failed, fix the issue and repeat the previous steps 
with `rc2` etc. If installing worked, proceed to the next step.

### Release

To create a release, push it to PyPi and add a tag on current git master.

    invoke prerelease 0.0.1

 On a clean virtual machine, verify that you can install the new version and that it 
 works correctly with: 
 
    pip install pypi-holoniq-simple==0.0.1

Finally run 

    invoke postrelease 0.0.1 
        
This will change the version numbers back to a `-dev` version.


## Acknowledgments

The template in based on the tutorial [How To Publish A Package On PyPI](https://2018.pycon-au.org/talks/44349-how-to-publish-a-package-on-pypi/). Also a big thankyou to the [dash-bootstrap-components](https://github.com/facultyai/dash-bootstrap-components)
team. This templates release script is a simplified version of the one developed by them.

[pypi-home]: https://pypi.org
[invoke-home]: http://www.pyinvoke.org
[travis-home]: https://travis-ci.org
[cookiecutter]: http://cookiecutter-templates.sebastianruml.name/
[cookiecutter-pypackage-minimal]: https://github.com/kragniz/cookiecutter-pypackage-minimal
