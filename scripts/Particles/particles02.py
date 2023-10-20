import argparse
import pygame as pg
import numpy as np

#===================================================================================================
#                                                GLOBALS 
#===================================================================================================


DEFAULT_VARIANT_RELATIONS = np.array([[0.1, -0.1, 0.0],
                              [0.0, 0.1, -0.1],
                              [-0.1, 0.0, 0.1]
                              ])

PARTICLE_COLORS = [[255,0,0],
                   [0,255,0],
                   [0,0,255]
                   ]


#===================================================================================================
#                                                PHYSICS 
#===================================================================================================

class ParticleModelConfiguration:

    DEFAULT_SIMULATION_SIZE = (500,500)
    MINIMUM_SIMULATION_SIZE = 100
    MAX_VARIANT_COUNT = 3
    DEFAULT_PARTICLE_COUNT = 100

    def __init__(self,
                 simulation_size=DEFAULT_SIMULATION_SIZE,
                 variaton_relations=DEFAULT_VARIANT_RELATIONS,
                 particle_count=DEFAULT_PARTICLE_COUNT):
        try:
            if (len(simulation_size) != 2 or
                simulation_size[0] < self.MINIMUM_SIMULATION_SIZE or
                simulation_size[1] < self.MINIMUM_SIMULATION_SIZE
                ):
                raise ValueError(f'Simulation size must be tuple with two values larger than {self.MINIMUM_SIMULATION_SIZE} while it is given as {simulation_size}')
            self.simulation_size = simulation_size

            if type(variaton_relations) != np.ndarray:
                raise TypeError(f'Variation relations must be a numpy array however it is set to {type(variaton_relations).__name__}')
            if len(variaton_relations.shape) !=2 or variaton_relations.shape[0] != variaton_relations.shape[1]:
                raise ValueError(f'Variaton relations must be a square matrix however matrix of size {variaton_relations.shape} was given.')
            if variaton_relations.shape[0] > self.MAX_VARIANT_COUNT:
                raise ValueError(f'Maximum number of variants is {self.MAX_VARIANT_COUNT} however {variaton_relations.shape[0]} variants were given.')
            self.variaton_relations = variaton_relations.copy()
            
            if particle_count < 1:
                raise ValueError(f'Particle count must be 1 or greater, however value {particle_count} was given.')
            self.particle_count = particle_count


        except Exception as e:
            exception_type = type(e)
            raise exception_type(f'During initialization of particle model configuration exception occured {type(e).__name__} -> {e}')

    def get_variant_count(self):
        return self.variaton_relations.shape[0]

class ParticleModel:

    def __init__(self, cfg=ParticleModelConfiguration()):
        try:
            self.cfg = cfg
            self.variants = np.random.randint(low=0, high=cfg.get_variant_count(), size=cfg.particle_count)
            positions_x = np.random.rand(1,cfg.particle_count)*cfg.simulation_size[0]
            positions_y = np.random.rand(1,cfg.particle_count)*cfg.simulation_size[1]
            other_values = np.zeros([4,cfg.particle_count])
            self.state = np.vstack([positions_x,positions_y,other_values])
            print(self.state)

        except Exception as e:
            exception_type = type(e)
            raise exception_type(f'During initialization of particle model exception occured {type(e).__name__} -> {e}')

try:
    cfg = ParticleModelConfiguration(particle_count=3)
    model = ParticleModel(cfg)
except Exception as e:
    print(e)
