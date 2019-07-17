"""
Settings for ExtModel are all namespaced in the EXT_MODEL variable.
For example you project's `settings.py` file might have:

EXT_MODEL = {
	'META_NAME': 'ExtMeta',
	'META_ATTR': '_ext_meta',
	'DEFAULT_META': {
		'prefer_cached_count': False,
		'cached_count_timeout': 300,
		'random_foo': 'specific_bar',
	}
}

Settings:
 - META_NAME: the class name that is declared on the model
 - META_ATTR: the attr that extmeta is accessable through
 - prefer_cached_count: if true count() trys cache first
 - cached_count_timeout: time in seconds cache persists

"""
from django.conf import settings

DEFAULT_SETTINGS = {
	'META_NAME': 'ExtMeta',
	'META_ATTR': '_extmeta',
	'DEFAULT_META': {
		'prefer_cached_count': False,
		'cached_count_timeout': 300,
	}
}


ext_settings = DEFAULT_SETTINGS.copy()
ext_settings.update(getattr(settings, 'EXT_MODEL', {}))

# Validate settings
assert isinstance(ext_settings['META_NAME'], str)
assert isinstance(ext_settings['META_ATTR'], str)
assert ext_settings['META_NAME'].isidentifier(), "META_NAME must be a valid variable"
assert ext_settings['META_ATTR'].isidentifier(), "META_ATTR must be a valid variable"

assert isinstance(ext_settings['DEFAULT_META'], dict)
assert isinstance(ext_settings['DEFAULT_META']['prefer_cached_count'], bool)
assert isinstance(ext_settings['DEFAULT_META']['cached_count_timeout'], int)
