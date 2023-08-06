# Django Restricted Paths

## Description

Restricts access to specific urls to staff only by responding with a specific view or raising a 404.

## Installation

```python
pip install django-restricted-paths
```

## Usage

in settings.py:

```python
RESTRICTED_PATHS = {
  "ENABLED": not DEBUG,
  "PATHS": ("/admin",),
  "VIEW": "path.to.view.class.ViewClass",
}

MIDDLEWARE = (
    ...
    "restricted_paths.middleware.RestrictedPathsMiddleware"
)
```
