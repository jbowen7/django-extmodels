from django_extmodels.settings import ext_settings


class ExtOptions:
	def __init__(self, extmeta=None):
		# Set the defaults defined in django.conf.settings
		for attr, value in ext_settings['DEFAULT_META'].items():
			setattr(self, attr, value)

		# Override defaults (if passed in)
		if extmeta:
			meta_attrs = extmeta.__dict__.copy()
			for name, value in meta_attrs.items():
				if name.startswith('_'):
					continue
				elif name in self.__dict__:
					setattr(self, name, value)
				else:
					raise TypeError(f"'class {ext_settings['META_NAME']}' got invalid attribute: {name}")

	def __set_name__(self, owner, name):
		self.model = owner

	def __repr__(self):
		return f"<ExtOptions for {self.model.__name__}>"
