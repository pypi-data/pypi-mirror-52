# -*- coding: utf-8 -*-

import hashlib
from unittest import TestCase
from mock import patch, Mock

from django2_manager_cache.mixins import (
    CacheKeyMixin,
    CacheInvalidateMixin
)
from django2_manager_cache.model_cache_sharing.types import ModelCacheInfo
from .models import Manufacturer


@patch('django2_manager_cache.mixins.model_cache_backend')
@patch.object(CacheKeyMixin, 'sql')
class CacheKeyMixinTests(TestCase):
    """
    Tests for django2_manager_cache.mixins.CacheKeyMixin
    """

    def setUp(self):
        self.mixin = CacheKeyMixin()
        self.mixin.model = Manufacturer()
        self.mixin.db = 'db'

    def test_consistent_key_generation(self, mock_sql, mock_model_cache):
        """
        Mixin generates identical keys for repeated calls when sql and model are the same.
        """
        mock_sql.return_value = 'sql'
        key1 = self.mixin.generate_key()
        key2 = self.mixin.generate_key()
        self.assertEquals(key1, key2)

    def test_key_generation_with_non_ascii_unicode(self, mock_sql, mock_model_cache):
        """
        When the query_key is unicode containing non-ascii characters, hashlib.md5 should not error out
        """
        mock_sql.return_value = u'\xf1'

        try:
            self.mixin.generate_key()
        except UnicodeEncodeError:
            self.fail("CacheKeyMixin.gernerate_key() raised a UnicodeEncodeError!")

    @patch('django2_manager_cache.mixins.uuid')
    def test_new_key_generation(self, mock_uuid, mock_sql, mock_model_cache):
        """
        Mixin broadcasts key for the model when it is newly created
        """
        mock_model_cache.retrieve_model_cache_info.return_value = None
        mock_uuid4 = Mock(hex='unique_id')
        mock_uuid.uuid4.return_value = mock_uuid4
        self.mixin.generate_key()
        model_cache_info = ModelCacheInfo(table_name=u'tests_manufacturer', table_key='unique_id')
        mock_model_cache.share_model_cache_info.assert_called_once_with(model_cache_info)

    def test_key_components(self, mock_sql, mock_model_cache):
        """
        Ensure key created by mixin is a hash of model_key, sql query and database name
        """
        mock_sql.return_value = 'sql'
        mock_model_cache.retrieve_model_cache_info.return_value = ModelCacheInfo(table_name=u'tests_manufacturer', table_key='unique_id')
        expected_key_value = hashlib.md5(u'unique_idsqldb'.encode('utf-8')).hexdigest()
        self.assertEquals(expected_key_value, self.mixin.generate_key())

    def test_get_or_create_model_key(self, mock_sql, mock_model_cache):
        """
        get_or_create_model_key returns existing key when one exists
        """
        mock_model_cache.retrieve_model_cache_info.return_value = ModelCacheInfo(table_name=u'tests_manufacturer', table_key='unique_id')
        key, created = self.mixin.get_or_create_model_key()
        self.assertFalse(created)
        self.assertEquals(key, 'unique_id')

    @patch('django2_manager_cache.mixins.uuid')
    def test_get_or_create_model_key_creates(self, mock_uuid, mock_sql, mock_model_cache):
        """
        get_or_create_model_key creates a new key for model when it does not exist
        """
        mock_model_cache.retrieve_model_cache_info.return_value = None
        mock_uuid4 = Mock(hex='uuid')
        mock_uuid.uuid4.return_value = mock_uuid4
        key, created = self.mixin.get_or_create_model_key()
        self.assertEquals(True, created)
        self.assertEquals(key, 'uuid')


@patch('django2_manager_cache.models.model_cache_backend')
class CacheInvalidateMixinTests(TestCase):
    """
    Tests for django2_manager_cache.mixins.CacheInvalidateMixin
    """

    def setUp(self):
        self.mixin = CacheInvalidateMixin()
        self.mixin.model = Manufacturer()

    @patch('django2_manager_cache.models.uuid')
    def test_invalidate_model_cache(self, mock_uuid, mock_model_cache):
        """
        Mixin broadcasts new model cache info when a model is invalidated
        """
        mock_uuid4 = Mock(hex='unique_id')
        mock_uuid.uuid4.return_value = mock_uuid4
        self.mixin.invalidate_model_cache()
        self.assertEquals(mock_model_cache.share_model_cache_info.call_count, 2)
