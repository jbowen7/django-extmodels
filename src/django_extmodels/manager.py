from django.db import models

from django_extmodels.query import ExtQuerySet


class ExtManager(models.Manager):
	def get_queryset(self):
		return ExtQuerySet(self.model, using=self._db)

	def cached_count(self):
		return self.get_queryset().cached_count()
