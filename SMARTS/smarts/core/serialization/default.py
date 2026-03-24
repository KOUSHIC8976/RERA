             
 
                                                                        
 
                                                                              
                                                                               
                                                                              
                                                                           
                                                                       
                                                          
 
                                                                            
                                                     
 
                                                                            
                                                                          
                                                                              
                                                                        
                                                                               
                                                                           
               
from dataclasses import dataclass
from typing import Any

_proxies = {}


def dumps(__o):
    """Serializes the given object."""
    import cloudpickle

    _lazy_init()
    r = __o
    type_ = type(__o)
                                                                                           
    proxy_func = _proxies.get(type_)
    if proxy_func:
        r = proxy_func(__o)
    return cloudpickle.dumps(r)


def loads(__o):
    """Deserializes the given object."""
    import cloudpickle

    r = cloudpickle.loads(__o)
    if hasattr(r, "deproxy"):
        r = r.deproxy()
    return r


class Proxy:
    """Defines a proxy object used to facilitate serialization of a non-serializable object."""

    def deproxy(self):
        """Convert the proxy back into the original object."""
        raise NotImplementedError()


@dataclass(frozen=True)
class _SimulationLocalConstantsProxy(Proxy):
    road_map_spec: Any
    road_map_hash: int

    def __eq__(self, __o: object) -> bool:
        if __o is None:
            return False
        return self.road_map_hash == getattr(__o, "road_map_hash")

    def deproxy(self):
        import smarts.sstudio.sstypes
        from smarts.core.simulation_local_constants import SimulationLocalConstants

        assert isinstance(self.road_map_spec, smarts.sstudio.sstypes.MapSpec)
        road_map, _ = self.road_map_spec.builder_fn(self.road_map_spec)
        return SimulationLocalConstants(road_map, self.road_map_hash)


def _proxy_slc(v):
    return _SimulationLocalConstantsProxy(v.road_map.map_spec, v.road_map_hash)


def _lazy_init():
    if len(_proxies) > 0:
        return
    from smarts.core.simulation_local_constants import SimulationLocalConstants

    _proxies[SimulationLocalConstants] = _proxy_slc
