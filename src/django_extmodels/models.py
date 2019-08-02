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

		# Preserve ExtOptions inherited by most recent parent
		base_meta = None
		for base in bases:
			base_meta = getattr(base, META_ATTR_NAME, None)
			if base_meta: break  # noqa

		# Contribute to attrs before super constructor
		attrs[META_ATTR_NAME] = ExtOptions(base_meta)

		# If new_class declared `class ExtMeta` this will override the parent options
		meta = attrs.get(META_CLASS_NAME, None)
		if meta:
			attrs.get(META_ATTR_NAME)._merge_options(meta)

		return super_new(cls, name, bases, attrs)


class ExtModel(models.Model, metaclass=ExtModelBase):
	objects = ExtManager()

	class Meta:
		abstract = True
