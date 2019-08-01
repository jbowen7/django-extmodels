from django.db import models

from django_extmodels.manager import ExtManager
from django_extmodels.options import ExtOptions
from django_extmodels.settings import ext_settings

META_CLASS_NAME = ext_settings['META_NAME']
META_ATTR_NAME = ext_settings['META_ATTR']


class ExtModelBase(models.base.ModelBase):
	def __new__(cls, name, bases, attrs):
		super_new = super().__new__

		# If this isn't a subclass of Model, don't bother with initilization
		parents = [b for b in bases if isinstance(b, ExtModelBase)]
		if not parents:
			return super_new(cls, name, bases, attrs)

		# If new class overrides ExtMeta pop here to add later
		attr_meta = attrs.get(META_CLASS_NAME, None)

		# Create class
		new_class = super_new(cls, name, bases, attrs)

		# Most recent declaration of `class ExtMeta:` (if not inheritted, None is used)
		meta = attr_meta or getattr(new_class, META_CLASS_NAME, None)

		# Check for _extmeta on the parent class, which will be used for merging
		base_meta = getattr(new_class, META_ATTR_NAME, None)

		# Update options with meta if it was passed or inherited
		options = ExtOptions(base_meta)
		if meta:
			options._merge_options(meta)

		# Add ExtMeta
		setattr(new_class, META_ATTR_NAME, options)

		return new_class


class ExtModel(models.Model, metaclass=ExtModelBase):
	objects = ExtManager()

	class Meta:
		abstract = True
