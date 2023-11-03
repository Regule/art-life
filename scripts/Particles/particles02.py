import sys
import argparse
import pygame as pg
import numpy as np
from scipy.spatial import distance_matrix

#===================================================================================================
#                                                GLOBALS 
#===================================================================================================

# FIXME: SUPER UGLY
np.seterr(divide='ignore')

DEFAULT_VARIANT_RELATIONS = np.array([[0.1, -0.0, 0.0],
                                      [0.0, 0.1, -0.0],
                                      [-0.0, 0.0, 0.1],
                                      ])

PARTICLE_COLORS = [[255,0,0],
                   [0,255,0],
                   [0,0,255],
                   [0,255,255],
                   [255,0,255],
                   [255,255,0]
                   ]


#===================================================================================================
#                                                PHYSICS 
#===================================================================================================

class ParticleModelConfiguration:

    DEFAULT_SIMULATION_SIZE = (500,500)
    MINIMUM_SIMULATION_SIZE = 100
    MAX_VARIANT_COUNT = 6
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
            self.force_base = np.zeros((self.variants.shape[0], self.variants.shape[0]), dtype=np.float64)
            for y in range(self.variants.shape[0]):
                for x in range(self.variants.shape[0]):
                    self.force_base =  self.cfg.variaton_relations[self.variants[y]][self.variants[x]]

        except Exception as e:
            exception_type = type(e)
            raise exception_type(f'During initialization of particle model exception occured {type(e).__name__} -> {e}')

    def update_model(self, dt):
        self.apply_external_forces()
        self.update_inertial_model(dt)

    def update_inertial_model(self, dt):
        transformation_matrix = np.array([[1.0, 0.0, dt, 0.0, dt*dt, 0.0],
                                         [0.0, 1.0, 0.0, dt, 0.0, dt*dt],
                                         [0.0, 0.0, 1.0, 0.0, dt, 0.0],
                                         [0.0, 0.0, 0.0, 1.0, 0.0, dt],
                                         [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                                         [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]])
        self.state = transformation_matrix @ self.state
        self.state[0,:] = np.remainder(self.state[0,:], self.cfg.simulation_size[0])
        self.state[1,:] = np.remainder(self.state[1,:], self.cfg.simulation_size[1])

    def apply_external_forces(self):
        position_vector = self.state[:2,:].transpose()
        distance = distance_matrix(position_vector, position_vector)
        force = np.divide(self.force_base,
                          distance
                          )
        force = np.where(force==np.Inf, 0.0, force)
        force = force.sum(axis=0)
        self.state[-2:,:] = force


#===================================================================================================
#                                            USER INTERFACE 
#===================================================================================================

class UserInterfaceConfig:

    MINIMUM_PARTICLE_RADIUS = 3
    DEFAULT_TIME_SCALING = 0.001
    DEFAULT_BG_COLOR = [0, 0, 0]

    def __init__(self, particle_radius=MINIMUM_PARTICLE_RADIUS, time_scaling=DEFAULT_TIME_SCALING,
                 bg_color=DEFAULT_BG_COLOR):
        try:
            if particle_radius < self.MINIMUM_PARTICLE_RADIUS:
                raise ValueError(f'Particle radius must be larger than {self.MINIMUM_PARTICLE_RADIUS} however value {particle_radius} was given')
            self.particle_radius = particle_radius

            if time_scaling <= 0:
                raise ValueError(f'Time scaling must be larger than 0 (suggested values in range 0 to 1).')
            self.time_scaling = time_scaling

            # FIXME: CHECK COLOR RANGE
            if len(bg_color) != 3:
                raise ValueError(f'Color value must be a three dimensional integer vector with values in range from 0 to 255 however value {bg_color} was given.')
            self.bg_color = bg_color

        except Exception as e:
            exception_type = type(e)
            raise exception_type(f'During initialization of UI config exception occured {type(e).__name__} -> {e}')


class UserInterface:

    def __init__(self, cfg=UserInterfaceConfig(), model=ParticleModel()):
        try:
            self.model = model
            pg.init()
            self.screen = pg.display.set_mode(model.cfg.simulation_size)
            self.timer = pg.time.Clock()
            self.cfg = cfg
            self.running = False
        except Exception as e:
            exception_type = type(e)
            raise exception_type(f'During initialization of user interface exception occured {type(e).__name__} -> {e}')
        
    def loop(self):
        self.running = True
        while self.running:
            self.clear_screen()
            self.draw_particles()
            pg.display.flip() 
            self.handle_events()
            dt = self.timer.tick()*self.cfg.time_scaling
            self.model.update_model(dt)
    
    def clear_screen(self):
        self.screen.fill(self.cfg.bg_color)

    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
               self.running = False 

    def draw_particles(self):
        for i in range(self.model.cfg.particle_count):
            particle_position = np.array(self.model.state[0:2,i], dtype=np.int64).tolist()
            pg.draw.circle(self.screen,
                           PARTICLE_COLORS[self.model.variants[i]],
                           particle_position,
                           self.cfg.particle_radius) 

#===================================================================================================
#                                         MAIN FUNCTION 
#===================================================================================================

def main():
    model_cfg = ParticleModelConfiguration(particle_count=100)
    model = ParticleModel(model_cfg)
    cfg = UserInterfaceConfig(particle_radius=3, time_scaling=0.01)
    ui = UserInterface(cfg=cfg, model=model)
    ui.loop()

if __name__ == '__main__':
    main()
    
