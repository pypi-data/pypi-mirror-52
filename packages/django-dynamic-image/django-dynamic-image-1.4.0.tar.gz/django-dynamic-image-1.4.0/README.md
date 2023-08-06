# Django Dynamic Image

## Description

A django ImageField whose upload_to value is generated from a model method.

## Installation

```python
pip install django-dynamic-image
```

## Usage

```python
from django.db import models
from dynamic_image.fields import DynamicImageField

class ExampleModel(models.Model):
    name = models.CharField(max_length=56)
    image = DynamicImageField()

    def get_upload_to(self, field_name):
        class_name = self.__class__.__name__.lower()
        instance_name = self.name
        return "{}/{}".format(class_name, instance_name)
```
