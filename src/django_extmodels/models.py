from django.db import models

from django_extmodels.manager import ExtManager
from django_extmodels.options import ExtOptions
from django_extmodels.settings import ext_settings


class ExtModelBase(models.base.ModelBase):
	def __new__(cls, name, bases, attrs):
		super_new = super().__new__

		# If this isn't a subclass of Model, don't bother with initilization
		parents = [b for b in bases if isinstance(b, ExtModelBase)]
		if not parents:
			return super_new(cls, name, bases, attrs)

		# Add Extended Meta options to the new class
		ext_meta = attrs.get(ext_settings['META_NAME'], None)
		attrs[ext_settings['META_ATTR']] = ExtOptions(ext_meta)

		return super_new(cls, name, bases, attrs)


class ExtModel(models.Model, metaclass=ExtModelBase):
	objects = ExtManager()

	class Meta:
		abstract = True
