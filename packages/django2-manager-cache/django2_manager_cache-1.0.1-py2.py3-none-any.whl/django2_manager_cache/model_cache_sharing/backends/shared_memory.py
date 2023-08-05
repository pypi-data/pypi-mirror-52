# -*- coding: utf-8 -*-
import logging
import django
import django.core.cache

from django.conf import settings

from .base import BaseSharing

_cache_name = getattr(settings, 'django2_manager_cache.cache_backend', 'django2_manager_cache.cache_backend')
logger = logging.getLogger(__name__)


class SharedMemory(BaseSharing):
    "Processes implicitly communicate by using a shared memory "

    # could use a different cache namespace
    def share_model_cache_info(self, model_cache_info, **kwargs):
        logger.info(u'Updating model cache {0}'.format(model_cache_info))
        self.cache_backend.set(model_cache_info.table_name, model_cache_info)

    def retrieve_model_cache_info(self, key, **kwargs):
        model_cache_info = self.cache_backend.get(key)
        return model_cache_info

    @property
    def cache_backend(self):
        if not hasattr(self, '_cache_backend'):
            if hasattr(django.core.cache, 'caches'):
                self._cache_backend = django.core.cache.caches[_cache_name]
            else:
                self._cache_backend = django.core.cache.get_cache(_cache_name)

        return self._cache_backend
