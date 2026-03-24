             
 
                                                                        
 
                                                                              
                                                                               
                                                                              
                                                                           
                                                                       
                                                          
 
                                                                            
                                                     
 
                                                                            
                                                                          
                                                                              
                                                                        
                                                                               
                                                                           
               
import os

import numpy as np
import pytest

from smarts.sstudio.graphics.heightfield import HeightField


@pytest.fixture
def map_data():
    with open(os.path.join(os.path.dirname(__file__), "heightfield.binary"), "rb") as f:
        data = np.frombuffer(f.read(), dtype=np.uint8)
        return data.reshape((256, 256))


@pytest.fixture
def map_image():
    return np.array([[[0], [1], [0]], [[0], [1], [0]], [[2], [1], [2]]], dtype=np.uint8)


@pytest.fixture
def map_image2():
    return np.array(
        [
            [[0], [1], [0], [1], [0]],
            [[0], [1], [0], [0], [0]],
            [[2], [1], [2], [0], [0]],
        ],
        dtype=np.uint8,
    )


@pytest.fixture
def kernel() -> np.ndarray:
    return np.array(
        [
            [1.0, 1.0, 0.5, 1.0, 1.0],
            [1.0, 0.0, 0.0, 0.0, 1.0],
            [0.5, 0.0, -80, 0.0, 0.5],
            [1.0, 0.0, 0.0, 0.0, 1.0],
            [1.0, 0.5, 0.5, 1.0, 1.0],
        ],
        dtype=np.float64,
    )


def test_heightfield_from_map(map_data):
    heighfield = HeightField(map_data, (100, 100))
    assert np.all(heighfield.data == map_data)


def test_heighfield_from_image(map_image):
    heighfield = HeightField(map_image, (100, 100))
    assert np.all(heighfield.data == np.squeeze(map_image, axis=2))


def test_heightfield_kernel(map_data, kernel):
    heightfield = HeightField(map_data, (100, 100))
    field = heightfield.apply_kernel(kernel)
    assert isinstance(field, HeightField)


def test_heightfield_inverted(map_image):
    hf = HeightField(data=map_image, size=(3, 3))
    ihf: HeightField = hf.inverted()

    assert np.all(hf.data == ihf.inverted().data)
