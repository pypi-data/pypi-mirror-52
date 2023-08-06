import pytest
from django_kck.cache import Cache
from django_kck.models import DataProduct


@pytest.mark.django_db
class BaseCacheTest(object):
    @pytest.fixture
    def f_cache(self):
        return lambda: Cache.get_instance(new_instance=True)

    def simulate_cache_entry(self, cache_entry):
        DataProduct(**cache_entry).save()

    def assert_current_cache_entry_value(self, cache, key, value):
        cache_entry = cache.get(key)
        assert cache_entry['value'] == value
