# django-extmodels
Extending the usage of Django Models

### Install
```
pip install django_extmodels
```

### Models
 ##### ExtModel:
 - FooModel._extmeta: It's usually not a good idea to put stuff in `FooModel._meta`. Inheriting from ExtModel gives your models a new property `FooModel._extmeta` where you can store arbitrary information.
 - FooModel.objects.cached_count(): if a cache backend is defined a count will be cached and retrieved there first.
 
 

### Usage

#### ExtModel
```
#file: app/models.py
from django_extmodels.models import ExtModel

Person(ExtModel):
  pass

Computer(ExtModel):
  ExtMeta:
    biomechanical = False

```
```
#file: settings.py
EXT_MODEL = {
  'META': {
    'biomechanical': True,
  }
}
  
```

```
