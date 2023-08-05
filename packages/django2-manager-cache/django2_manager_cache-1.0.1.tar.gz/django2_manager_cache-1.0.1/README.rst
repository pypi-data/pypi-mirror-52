django2\_manager\_cache
=======================

-  Simple cache manager for Django 2 models that caches querysets for a model.
-  Cache manager will cache any query that has been seen for a model.
-  Model cache is evicted for any updates/deletes to the model.
-  This manager is useful for models that don't change often.

|Build Status| |Coverage Status| |PyPI version|

Installation
------------

-  pip install django2-manager-cache

Caching strategy
----------------

-  Cache results for a model on load.
-  Evict cache for model on update.

Usage
-----

Add to installed apps::


    INSTALLED_APPS = (
        ...
        'django2_manager_cache',
        ...
    )


Add the manager to a django model::

    from django2_manager_cache import CacheManager
    class MyModel(models.Model):

       # set cache manager as default
       objects = CacheManager()

       # to use this manager with as related manager
       # https://docs.djangoproject.com/en/2.2/topics/db/managers/#base-managers
       # class Meta:
       #    base_manager_name = 'objects'


Define cache backend for ``django2_manager_cache.cache_backend`` in
``settings.py``. The backend can be any cache backend that implements
django cache API.::


   CACHES = {
       'django2_manager_cache.cache_backend': {
           'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
           'LOCATION': '127.0.0.1:11211',
       }
   }


Django shell
------------

To run django shell with sample models defined in tests.::


    make shell


Sample models::


    from tests.models import Manufacturer
    from tests.models import Car
    from tests.models import Driver
    m = Manufacturer(name='Tesla')
    m.save()
    c = Car(make=m, model='Model S', year=2015)
    c.save()
    d = Driver(first_name ='ABC', last_name='XYZ')
    d.save()
    d.cars.add(c)
    drivers = Driver.objects.select_related('car', 'manufacturer').all()

Testing
-------

To run tests::


    make test


Supported Django versions
-------------------------

Supported - 1.5, 1.6, 1.7, 1.8, 1.9, 1.11, 2.0, 2.1, 2.2



.. |Build Status| image:: https://travis-ci.org/gabomasi/django2_manager_cache.svg?branch=master
   :target: https://travis-ci.org/gabomasi/django2_manager_cache


.. |Coverage Status| image:: https://coveralls.io/repos/github/gabomasi/django2_manager_cache/badge.svg?branch=master
   :target: https://coveralls.io/github/gabomasi/django2_manager_cache?branch=master


.. |PyPI version| image:: https://badge.fury.io/py/django2-manager-cache.svg
   :target: https://pypi.org/project/django2-manager-cache/
