             
 
                                                                        
 
                                                                              
                                                                               
                                                                              
                                                                           
                                                                       
                                                          
 
                                                                            
                                                     
 
                                                                            
                                                                          
                                                                              
                                                                        
                                                                               
                                                                           
               
import numpy as np

from smarts.core.utils.core_math import (
    combination_pairs_with_unique_indices,
    position_to_ego_frame,
    world_position_from_ego_frame,
)


def test_egocentric_conversion():
    p_start = [1, 2, 3]
    pe = [1, -5, 2]
    he = -3

    pec = position_to_ego_frame(p_start, pe, he)

    assert np.allclose([-0.9878400564190705, -6.929947476203118, 1.0], pec)

    p_end = world_position_from_ego_frame(pec, pe, he)

    assert np.allclose(p_end, p_start)


def test_combination_pairs_with_unique_indices():

    assert not tuple(combination_pairs_with_unique_indices("", ""))
    assert tuple(combination_pairs_with_unique_indices("a", "")) == (("a", None),)
    assert tuple(
        combination_pairs_with_unique_indices("abc", "12", second_group_default=4)
    ) == (
        (("a", "1"), ("b", "2"), ("c", 4)),
        (("a", "1"), ("b", 4), ("c", "2")),
        (("a", "2"), ("b", "1"), ("c", 4)),
        (("a", "2"), ("b", 4), ("c", "1")),
        (("a", 4), ("b", "1"), ("c", "2")),
        (("a", 4), ("b", "2"), ("c", "1")),
    )
    assert tuple(combination_pairs_with_unique_indices("ab", "123")) == (
        (("a", "1"), ("b", "2")),
        (("a", "1"), ("b", "3")),
        (("a", "2"), ("b", "1")),
        (("a", "2"), ("b", "3")),
        (("a", "3"), ("b", "1")),
        (("a", "3"), ("b", "2")),
    )
