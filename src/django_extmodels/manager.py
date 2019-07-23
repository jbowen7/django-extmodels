from django.db.models.manager import BaseManager

from django_extmodels.query import ExtQuerySet


class ExtManager(BaseManager.from_queryset(ExtQuerySet)):
	"""
	A subclassable Manager
	"""
	pass
