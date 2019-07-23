from django.db import models

from django_extmodels.query import ExtQuerySet


class ExtManager(models.Manager):
	def get_queryset(self):
		return ExtQuerySet(self.model, using=self._db)

	def cached_count(self, *args, **kwargs):
		"""
		Like self.count(), except, it first checks the cache.
		If the value is not found, a SELECT COUNT() is performed
		and that value is stored in the cache.

		:param recount: if True then perform count and update cache with `SELECT COUNT()`
		:returns: number of records as an integer
		"""
		return self.get_queryset().cached_count(*args, **kwargs)
