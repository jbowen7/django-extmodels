from django.db.models.aggregates import Count

from django_extmodels.settings import ext_settings


def get_extmeta(model):
	"""
	returns the ExtMeta property of a model that subclasses ExtModel
	"""
	assert hasattr(model, ext_settings['META_ATTR'])
	return getattr(model, ext_settings['META_ATTR'])


def generate_count_query(query):
	"""
	given a Query instance, remove all sql syntax that has no affect on a query count

	Example:
	Foo.objects.filter(id__lt=10000).order_by('-id').select_related('bar').only('id','bar', 'name').count()
	becomes =>
	SELECT COUNT(*) AS `__count` FROM `app_foo` WHERE `app_foo`.`id` < 10000
	"""
	query = query.clone()
	query.select = ()
	query.default_cols = False
	query._extra = {}
	query.clear_ordering(True)
	query.clear_limits()
	query.select_for_update = False
	query.select_related = False
	query.add_annotation(Count('*'), alias='__count', is_summary=True)
	return query
