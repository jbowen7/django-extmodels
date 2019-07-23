from django.db.models import Manager

from django_extmodels.query import ExtQuerySet


class ExtManager(Manager.from_queryset(ExtQuerySet)):
	"""
	A subclassable Manager
	"""
	pass
