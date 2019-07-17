import hashlib

from django.core.cache import cache
from django.db import models

from django_extmodels.utils import generate_count_query, get_extmeta


class ExtQuerySet(models.QuerySet):
	def cached_count(self):
		# Key to use for cache
		query = generate_count_query(self.query)
		key = f"{query}; using={self.db}"
		hashed_key = hashlib.sha1(key.encode()).hexdigest()

		# get/set cache
		count = cache.get(hashed_key, None)
		if count is None:
			count = self.count(force=True)
			timeout = get_extmeta(self.model).cached_count_timeout
			cache.set(hashed_key, count, timeout)

		assert isinstance(count, int)
		return count

	def count(self, force=False):
		if force:
			return super().count()

		if get_extmeta(self.model).prefer_cached_count:
			return self.cached_count()

		return super().count()
