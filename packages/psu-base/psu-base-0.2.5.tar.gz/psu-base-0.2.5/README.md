# PSU-Base

Reusable Django app specifically for PSU's custom-built web applications.  
It encapsulates the common functionality that we would otherwise need to program into each application we build.
Features include:
-  PSU Single Sign-On (SSO)
-  Authentication and authorization features
-  Feature toggles
-  Template tags for our static content server

## Quick Start
### Dependencies
The following dependencies may be REQUIRED in your system:
- `libpq-dev`
    ```sh
    sudo apt install libpq-dev
    ```

### Installation
```sh
pip install psu-base
```

### Configuring Your App
1. Add PSU-Base and its two required apps to INSTALLED_APPS in `settings.py`:
    ```python
    INSTALLED_APPS = [
       ...
       'django_cas_ng',
       'crequest',
       'psu_base',
    ]
    ```

1. Copy `docs/app_settings_template.py` to your app, name it `app_settings.py` and 
update the values as needed.  

1. Copy `docs/local_settings_template.py` to your app, name it `local_settings.py` and 
update the values as needed.  

1. Import your app and local settings files at the end of your settings.py file:
`settings.py`
```python
    # Get app-specific settings
    from .app_settings import *
    
    # Override settings with values for the local environment
    from .local_settings import *
```

1. Run `python manage.py migrate` to create the PSU-Base models in your development database

1. <a name="configureyourapp4"></a>Configure your app's top-level `urls.py` to include PSU URLs
    ```python
    # my_app/urls.py
    from django.conf import settings
    from django.conf.urls import url
    from django.urls import path, include
    ...
    urlpatterns = [
        ...
        # PSU and CAS views are defined in psu_base app
        url(settings.URL_CONTEXT+'/psu/', include(('psu_base.urls', 'psu_base'), namespace='psu')),
        url(settings.URL_CONTEXT+'/accounts/', include(('psu_base.urls', 'psu_base'), namespace='cas')),
    ]
    ```

## Usage
Usage of the psu-base app is documented in 
[Confluence](https://portlandstate.atlassian.net/wiki/spaces/WDT/pages/713162905/Reusable+Django+Apps+The+Django+PSU+Plugin).

## For Developers
The version number must be updated for every PyPi release.
The version number is in `psu_base/__init__.py`

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
1. Ask an existing developer to add you as a collaborator - [test](https://test.pypi.org/manage/project/psu-base/collaboration/) and/or [prod](https://pypi.org/manage/project/psu-base/collaboration/)
1. `python setup.py sdist bdist_wheel --universal`
1. `twine upload --repository testpypi dist/*`
1. `twine upload dist/*`
1. Tag the release in Git.  Don't forget to push the tag!
Example:
```shell script
git tag 0.1.2
git push origin 0.1.2 
```