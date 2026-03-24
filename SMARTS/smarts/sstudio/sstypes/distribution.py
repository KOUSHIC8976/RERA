             
 
                                                                        
 
                                                                              
                                                                               
                                                                              
                                                                           
                                                                       
                                                          
 
                                                                            
                                                     
 
                                                                            
                                                                          
                                                                              
                                                                        
                                                                               
                                                                           
               


import random
from dataclasses import dataclass


@dataclass(frozen=True)
class Distribution:
    """A gaussian distribution used for randomized parameters."""

    mean: float
    """The mean value of the gaussian distribution."""
    sigma: float
    """The sigma value of the gaussian distribution."""

    def sample(self):
        """The next sample from the distribution."""
        return random.gauss(self.mean, self.sigma)


@dataclass
class UniformDistribution:
    """A uniform distribution, return a random number N
    such that a <= N <= b for a <= b and b <= N <= a for b < a.
    """

    a: float
    b: float

    def __post_init__(self):
        if self.b < self.a:
            self.a, self.b = self.b, self.a

    def sample(self):
        """Get the next sample."""
        return random.uniform(self.a, self.b)
