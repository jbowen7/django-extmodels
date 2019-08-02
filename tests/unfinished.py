from django.db import models

from django_extmodels.models import ExtModel
from django_extmodels.settings import ext_settings


class ControlBasic(models.Model):
	enabled = models.BooleanField(default=True)


class ControlAbstract(models.Model):
	enabled = models.BooleanField(default=True)

	class Meta:
		abstract = True
		ordering = ['enabled']


class ControlReal(ControlAbstract):
	name = models.CharField(default='john', max_length=255)


class ControlProxy(ControlReal):
	class Meta:
		proxy = True
		ordering = ['name']


class Basic(ExtModel):
	enabled = models.BooleanField(default=True)


class Abstract(ExtModel):
	enabled = models.BooleanField(default=True)

	class Meta:
		abstract = True

	class ExtMeta:
		prefer_cached_count = True
		cached_count_timeout = 100


class Real(Abstract):
	name = models.CharField(default='john', max_length=255)


class Proxy(Real):
	class Meta:
		proxy = True

	class ExtMeta:
		prefer_cached_count = False
		cached_count_timeout = 300


# Control Tests
assert hasattr(ControlBasic, 'Meta') is False
assert hasattr(ControlBasic, '_meta')

assert hasattr(ControlAbstract, 'Meta')
assert hasattr(ControlAbstract, '_meta')
assert ControlAbstract.Meta.ordering[0] == 'enabled'
assert ControlAbstract._meta.ordering[0] == 'enabled'

assert hasattr(ControlReal, 'Meta')
assert hasattr(ControlReal, '_meta')
assert ControlReal.Meta.ordering[0] == 'enabled'
assert ControlReal._meta.ordering[0] == 'enabled'

assert hasattr(ControlProxy, 'Meta')
assert hasattr(ControlProxy, '_meta')
# Interestingly on Proxy models the class Meta is removed and is referenced through the ABC
# And there for has the value of the Abstract class and not the one it assigned during declaration
assert id(ControlProxy.Meta) == id(ControlAbstract.Meta)
assert ControlProxy.Meta.ordering[0] == 'enabled'
assert ControlProxy._meta.ordering[0] == 'name'
assert ControlProxy._meta.ordering[0] == 'name'

# Real Tests
assert hasattr(Basic, 'ExtMeta') is False
assert hasattr(Basic, '_extmeta')
assert Basic._extmeta.prefer_cached_count == ext_settings.EXT_MODEL['DEFAULT_META']['prefer_cached_count']
assert Basic._extmeta.cached_count_timeout == ext_settings.EXT_MODEL['DEFAULT_META']['cached_count_timeout']
assert Basic._extmeta._model is Basic

assert hasattr(Abstract, 'ExtMeta')
assert hasattr(Abstract, '_extmeta')
assert Abstract._extmeta.prefer_cached_count is True
assert Abstract._extmeta.cached_count_timeout == 100
assert Abstract.ExtMeta.prefer_cached_count is True
assert Abstract.ExtMeta.cached_count_timeout == 100
assert Abstract._extmeta._model is Abstract

assert hasattr(Real, 'ExtMeta')
assert hasattr(Real, '_extmeta')
assert id(Real.ExtMeta) == id(Abstract.ExtMeta)
assert Real._extmeta.prefer_cached_count is True
assert Real._extmeta.cached_count_timeout == 100
assert Real.ExtMeta.prefer_cached_count is True
assert Real.ExtMeta.cached_count_timeout == 100
assert Real._extmeta._model is Real

assert hasattr(Proxy, 'ExtMeta')
assert hasattr(Proxy, '_extmeta')
assert id(Proxy.ExtMeta) != id(Real.ExtMeta)
assert Proxy._extmeta.prefer_cached_count is False
assert Proxy._extmeta.cached_count_timeout == 300
assert Proxy.ExtMeta.prefer_cached_count is False
assert Proxy.ExtMeta.cached_count_timeout == 300
assert Proxy._extmeta._model is Proxy
