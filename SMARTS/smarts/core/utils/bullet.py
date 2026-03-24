                                                                        
 
                                                                              
                                                                               
                                                                              
                                                                           
                                                                       
                                                          
 
                                                                            
                                                     
 
                                                                            
                                                                          
                                                                              
                                                                        
                                                                               
                                                                           
               

from typing import NamedTuple, Tuple

import numpy as np

from smarts.core.coordinates import Pose
from smarts.core.utils import pybullet


class ContactPoint(NamedTuple):
    """Contact result between a shape and another shape."""

    bullet_id: str
    """The id of the other shape."""
    contact_point: Tuple[float, float, float]
    """The contact point of the query shape."""
    contact_point_other: Tuple[float, float, float]
    """The contact point of the collided shape."""


class JointInfo(NamedTuple):
    """Details about a bullet joint."""

    index: int
    type_: int
    lower_limit: float
    upper_limit: float
    max_force: float
    max_velocity: float


class JointState(NamedTuple):
    """Physics state information about a joint."""

    position: Tuple[float, ...]
    velocity: Tuple[float, ...]


class BulletBoxShape:
    """A bullet box."""

    def __init__(self, bbox, bullet_client):
        self._client = bullet_client

        length, width, height = bbox
        collision_box = bullet_client.createCollisionShape(
            shapeType=pybullet.GEOM_BOX,
            halfExtents=(width * 0.5, length * 0.5, height * 0.5),
        )

        self._height = height
                                                       
        self._bullet_id = self._client.createMultiBody(1, collision_box)

    def reset_pose(self, pose: Pose):
        """Resets the box to the given pose. Only call this before it needs to do anything
        physics-wise
        """
        position, orientation = pose.as_bullet()
        self._client.resetBasePositionAndOrientation(
            self._bullet_id,
            np.sum([position, [0, 0, self._height * 0.5]], axis=0),
            orientation,
        )

    def teardown(self):
        """Cleans up bullet resource handles."""
        self._client.removeBody(self._bullet_id)
        self._bullet_id = None


class BulletPositionConstraint:
    """A "half"-spring constraint that pulls the attached shape to a pose. This allows motion
    through forces rather than disrupting the simulation by moving the shape without forces.
    """

    def __init__(self, bullet_shape, bullet_client):
        self._client = bullet_client

        self._bullet_shape = bullet_shape
        self._bullet_cid = None

    def _make_constraint(self, pose: Pose):
        self._bullet_shape.reset_pose(pose)
        relative_pos = [0, 0, 0]
        relative_ori = [0, 0, 0, 1]
        self._bullet_cid = self._client.createConstraint(
            self._bullet_shape._bullet_id,
            -1,
            -1,
            -1,
            self._client.JOINT_FIXED,
            [0, 0, 0],
            [0, 0, -self._bullet_shape._height * 0.5],
            relative_pos,
            relative_ori,
        )

    def move_to(self, pose: Pose):
        """Moves the constraint to the given pose. The attached shape will attempt to follow."""
        if not self._bullet_cid:
            self._make_constraint(pose)
        position, orientation = pose.as_bullet()
                                                                    
                                                                
        ground_position = position + [0, 0, 0.2]
        self._client.changeConstraint(self._bullet_cid, ground_position, orientation)

    def teardown(self):
        """Clean up unmanaged resources."""
        if self._bullet_cid is not None:
            self._client.removeConstraint(self._bullet_cid)
        self._bullet_cid = None
