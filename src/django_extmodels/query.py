import hashlib

from django.core.cache import cache
from django.db import models

from django_extmodels.utils import generate_count_query, get_extmeta

#TODO:jbowen7 the cache to use should be determined from settings

class ExtQuerySet(models.QuerySet):
	def cached_count(self, recount=False):
		"""
		Like self.count(), except, it first checks the cache.
		If the value is not found, a SELECT COUNT() is performed
		and that value is stored in the cache.

		:param recount: if True then perform count and update cache with `SELECT COUNT()`
		:returns: number of records as an integer
		"""
		# Key to use for cache
		query = generate_count_query(self.query)
		key = f"{query}; using={self.db}"
		hashed_key = hashlib.sha1(key.encode()).hexdigest()

		# get/set cache if cache not found or recount required
		count = cache.get(hashed_key, None)
		if count is None or recount:
			count = self.count()
			timeout = get_extmeta(self.model).cached_count_timeout
			cache.set(hashed_key, count, timeout)

		assert isinstance(count, int)
		return count
