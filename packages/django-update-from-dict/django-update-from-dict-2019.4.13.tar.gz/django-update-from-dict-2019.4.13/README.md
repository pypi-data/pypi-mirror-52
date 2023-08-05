<!--
https://pypi.org/project/readme-generator/
https://pypi.org/project/python-readme-generator/
https://pypi.org/project/django-readme-generator/
-->

[![](https://img.shields.io/pypi/pyversions/django-update-from-dict.svg?longCache=True)](https://pypi.org/project/django-update-from-dict/)

#### Installation
```bash
$ [sudo] pip install django-update-from-dict
```

#### Classes
class|`__doc__`
-|-
`django_update_from_dict.UpdateFromDictMixin` |Update Django model from dictionary

#### Functions
function|`__doc__`
-|-
`django_update_from_dict.update_from_dict(instance, attrs, commit)` |Update Django model from dictionary

#### Examples
Mixin:
```python
from django.db import models
from django_update_from_dict import update_from_dict, UpdateFromDictMixin

class ClassName(UpdateFromDictMixin,models.Model):
    ...

instance = ClassName()
instance.update_from_dict(attrs,commit=True)
```

function:
```python
from django_update_from_dict import update_from_dict

update_from_dict(instance,attrs,commit=True)
```

<p align="center">
    <a href="https://pypi.org/project/django-readme-generator/">django-readme-generator</a>
</p>