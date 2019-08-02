from django_extmodels.settings import ext_settings


class ExtOptions:
	DEFAULT_OPTIONS = ext_settings['DEFAULT_META']

	def __init__(self, extmeta=None):
		"""
		ExtOptions must be declared in settings

		:param extmeta: must have __dict__
		"""
		# Set later by descriptor
		self._model = None
		self._name = None

		# Set the defaults defined in django.conf.settings
		for attr, value in self.DEFAULT_OPTIONS.items():
			setattr(self, attr, value)

		if extmeta:
			self._merge_options(extmeta)

	def _merge_options(self, extmeta):
		"""
		Merge options from another object into this one

		:param extmeta: must have __dict__
		"""
		meta_attrs = extmeta.__dict__.copy()
		for name, value in meta_attrs.items():
			if name in self.DEFAULT_OPTIONS:
				setattr(self, name, value)
			elif name.startswith('_'):
				continue
			else:
				raise TypeError(f"'class {ext_settings['META_NAME']}' got invalid attribute: {name}")

	def __set_name__(self, owner, name):
		self._model = owner
		self._name = name

	def __repr__(self):
		return f"<ExtOptions for {self._model.__name__}>"
