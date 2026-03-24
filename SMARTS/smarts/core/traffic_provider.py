                                                                        
 
                                                                              
                                                                               
                                                                              
                                                                           
                                                                       
                                                          
 
                                                                            
                                                     
 
                                                                            
                                                                          
                                                                             
                                                                        
                                                                               
                                                                           
               


from typing import Optional

from shapely.geometry import Polygon

from .provider import Provider
from .road_map import RoadMap


class TrafficProvider(Provider):
    """A TrafficProvider is a Provider that controls/owns a (sub)set of vehicles
    that all share the same action space."""

    def reserve_traffic_location_for_vehicle(
        self,
        vehicle_id: str,
        reserved_location: Polygon,
    ):
        """Reserve an area around a location where vehicles cannot spawn until a given vehicle
        is added.
        Args:
            vehicle_id: The vehicle to wait for.
            reserved_location: The space the vehicle takes up.
        """
        raise NotImplementedError

    def vehicle_collided(self, vehicle_id: str):
        """Called when a vehicle this provider manages is detected to have
        collided with any other vehicles in the scenario."""
        raise NotImplementedError

    def update_route_for_vehicle(self, vehicle_id: str, new_route: RoadMap.Route):
        """Set a new route for the given vehicle."""
        raise NotImplementedError

    def vehicle_dest_road(self, vehicle_id: str) -> Optional[str]:
        """Get the final road_id in the route of the given vehicle."""
        raise NotImplementedError

    def route_for_vehicle(self, vehicle_id: str) -> Optional[RoadMap.Route]:
        """Gets the current Route for the specified vehicle, if known."""
        return None

    def destroy(self):
        """Clean up any connections/resources."""
        raise NotImplementedError
