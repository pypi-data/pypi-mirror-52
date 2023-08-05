# -*- coding: utf-8 -*-
import hashlib
import logging
import uuid

import django
import django.core.cache

from django.conf import settings
from django.db.models.fields.related import RelatedField

from .model_cache_sharing.types import ModelCacheInfo
from .model_cache_sharing import model_cache_backend
from .models import update_model_cache


_cache_name = getattr(settings, 'django2_manager_cache.cache_backend', 'django2_manager_cache.cache_backend')
logger = logging.getLogger(__name__)


class CacheKeyMixin(object):

    def generate_key(self):
        """
        Generate cache key for the current query. If a new key is created for the model it is
        then shared with other consumers.
        """
        sql = self.sql()
        key, created = self.get_or_create_model_key()
        if created:
            db_table = self.model._meta.db_table
            logger.debug('created new key {0} for model {1}'.format(key, db_table))
            model_cache_info = ModelCacheInfo(db_table, key)
            model_cache_backend.share_model_cache_info(model_cache_info)
        query_key = u'{model_key}{qs}{db}'.format(model_key=key,
                                                  qs=sql,
                                                  db=self.db)
        key = hashlib.md5(query_key.encode('utf-8')).hexdigest()
        return key

    def sql(self):
        """
        Get sql for the current query.
        """
        clone = self.query.clone()
        sql, params = clone.get_compiler(using=self.db).as_sql()
        return sql % params

    def get_or_create_model_key(self):
        """
        Get or create key for the model.

        Returns
        ~~~~~~~
        (model_key, boolean) tuple

        """
        model_cache_info = model_cache_backend.retrieve_model_cache_info(self.model._meta.db_table)
        if not model_cache_info:
            return uuid.uuid4().hex, True
        return model_cache_info.table_key, False


class CacheInvalidateMixin(object):

    def invalidate_model_cache(self):
        """
        Invalidate model cache by generating new key for the model.
        """
        logger.info('Invalidating cache for table {0}'.format(self.model._meta.db_table))
        if django.VERSION >= (1, 8):
            related_tables = set(
                [f.related_model._meta.db_table for f in self.model._meta.get_fields()
                 if ((f.one_to_many or f.one_to_one) and f.auto_created)
                 or f.many_to_one or (f.many_to_many and not f.auto_created)])
        else:
            related_tables = set([rel.model._meta.db_table for rel in self.model._meta.get_all_related_objects()])
            # temporary fix for m2m relations with an intermediate model, goes away after better join caching
            related_tables |= set([field.rel.to._meta.db_table for field in self.model._meta.fields if issubclass(type(field), RelatedField)])

        logger.debug('Related tables of model {0} are {1}'.format(self.model, related_tables))
        update_model_cache(self.model._meta.db_table)
        for related_table in related_tables:
            update_model_cache(related_table)


class CacheBackendMixin(object):

    @property
    def cache_backend(self):
        """
        Get the cache backend

        Returns
        ~~~~~~~
        Django cache backend

        """
        if not hasattr(self, '_cache_backend'):
            if hasattr(django.core.cache, 'caches'):
                self._cache_backend = django.core.cache.caches[_cache_name]
            else:
                self._cache_backend = django.core.cache.get_cache(_cache_name)

        return self._cache_backend
