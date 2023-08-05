# PSU-Infotext
Reusable Django app specifically for PSU's custom-built web applications.  
Provides the ability to include user-editable text in any site using the psu_base plugin.  
Includes:
-  Template tags for editable text
-  WYSIWYG interface for editing the text

## Quick Start

### Dependencies
The following dependency is REQUIRED and must be installed in your app:
- [psu-base](https://pypi.org/project/psu-base/)

### Installation
```shell script
pip install psu-infotext
```

### Configuration
1. Configure [psu-base](https://pypi.org/project/psu-base/) in your Django app
1. Add PSU-Infotext to your INSTALLED_APPS in `settings.py`:
    ```python
    INSTALLED_APPS = [
       ...
       'psu_base',
       'psu_infotext',
    ]
    ```
1. Configure your app's top-level `urls.py` to include Infotext views:
    ```python
    urlpatterns = [
        ...
        path('infotext/', include(('psu_infotext.urls', 'psu_infotext'), namespace='infotext')),
    ]

## Usage
Usage of the psu-infotext app is documented in 
[Confluence](https://portlandstate.atlassian.net/wiki/spaces/WDT/pages/713523250/Django+Infotext).

## For Developers
The version number must be updated for every PyPi release.
The version number is in `psu_infotext/__init__.py`

### Document Changes
Record every change in [docs/CHANGELOG.txt](docs/CHANGELOG.txt)
Document new features or significant changes to existing features in [Confluence](https://portlandstate.atlassian.net/wiki/spaces/WDT/pages/713162905/Reusable+Django+Apps+The+Django+PSU+Plugin).

### Publishing to PyPi
1. Create accounts on [PyPi](https://pypi.org/account/register/) and [Test PyPi](https://test.pypi.org/account/register/)
1. Create `~/.pypirc`
    ```
    [distutils]
    index-servers=
        pypi
        testpypi
    
    [testpypi]
    repository: https://test.pypi.org/legacy/
    username: mikegostomski
    password: pa$$w0rd
    
    [pypi]
    username: mikegostomski
    password: pa$$w0rd
    ```
1. Ask an existing developer to add you as a collaborator - [test](https://test.pypi.org/manage/project/psu-infotext/collaboration/) and/or [prod](https://pypi.org/manage/project/psu-infotext/collaboration/)
1. `python setup.py sdist bdist_wheel --universal`
1. `twine upload --repository testpypi dist/*`
1. `twine upload dist/*`
1. Tag the release in Git.  Don't forget to push the tag!
Example:
```shell script
git tag 0.1.2
git push origin 0.1.2 
```