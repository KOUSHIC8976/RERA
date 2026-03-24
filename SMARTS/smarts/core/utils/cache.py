                                                                        
 
                                                                              
                                                                               
                                                                              
                                                                           
                                                                       
                                                          
 
                                                                            
                                                     
 
                                                                            
                                                                          
                                                                              
                                                                        
                                                                               
                                                                           
               
import functools
from threading import RLock
from types import FunctionType
from typing import Any

_CACHE_KEY_PREFIX = "_cache_decorator"


                                 
class _HashedSeq(list):
    """This class guarantees that hash() will be called no more than once per
    element.  This is important because the lru_cache() will hash the key multiple
    times on a cache miss.
    """

    __slots__ = "hashvalue"

    def __init__(self, tup, hash=hash):
        self[:] = tup
        self.hashvalue = hash(tup)

    def __hash__(self):
        return self.hashvalue


                                 
def _make_key(
    args,
    kwds,
    typed=False,
    kwd_mark=(object(),),
    fasttypes={int, str},
    tuple=tuple,
    type=type,
    len=len,
):
    """Make a cache key from optionally typed positional and keyword arguments. The key
    is constructed in a way that is flat as possible rather than as a nested structure
    that would take more memory. If there is only a single argument and its data type
    is known to cache its hash value, then that argument is returned without a wrapper.
    This saves space and improves lookup speed.
    """
                                                                              
                                                                           
                                                                         
                                                                     
    key = args
    if kwds:
        key += kwd_mark
        for item in kwds.items():
            key += item
    if typed:
        key += tuple(type(v) for v in args)
        if kwds:
            key += tuple(type(v) for v in kwds.values())
    elif len(key) == 1 and type(key[0]) in fasttypes:
        return key[0]
    return _HashedSeq(key)


                                                                                                        
class _CacheCallable:
    def __init__(self, cache_key: str, method: FunctionType, instance: Any):
        self._method = method
        self._instance = instance
        self._cache = instance.__dict__
        self._cache_key = cache_key
        self._lock = RLock()

    def __call__(self, *args, **kwargs) -> Any:
        cached = self._cache.get(self._cache_key, {})

        key = _make_key(args, kwargs)
        if key not in cached:
            with self._lock:
                                                                            
                cached = self._cache.get(self._cache_key, {})
                if key not in cached:
                    cached[key] = self._method(self._instance, *args, **kwargs)
                    self._cache[self._cache_key] = cached

        return cached[key]

    def clear_cache(self):
        """Clear the instance cache."""
        _CacheCallable.external_clear_cache(self._instance, self._cache_key)

    @staticmethod
    def external_clear_cache(instance, cache_key):
        """Clears the cache on the given instance."""
        setattr(instance, cache_key, {})


class cache:
    """A caching decorator."""

    def __init__(self, method: FunctionType):
        self._method = method
        self._cache_key = f"{_CACHE_KEY_PREFIX}_{method.__name__}"

    def __get__(self, instance: Any, _):
        assert instance, "Method must be called on an object"
        return _CacheCallable(self._cache_key, self._method, instance)


def clear_cache(func):
    """A decorator that clears `@cache` type caches."""

    def _clear_caches(self):
        for key in self.__dict__:
            if key.startswith(_CACHE_KEY_PREFIX):
                _CacheCallable.external_clear_cache(self, key)

    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        _clear_caches(self)
        return func(self, *args, **kwargs)

    return wrapper
