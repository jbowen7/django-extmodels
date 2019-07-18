import hashlib

from django.core.cache import cache
from django.db import models

from django_extmodels.utils import generate_count_query, get_extmeta


class ExtQuerySet(models.QuerySet):
	def cached_count(self, recount=False):
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
