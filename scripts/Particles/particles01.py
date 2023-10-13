import sys
import pygame as pg
import numpy as np

#===================================================================================================
#                                                GLOBALS 
#===================================================================================================
VARIANT_COUNT = 3
VARIANT_RELATIONS = np.array([[0.1, -0.1, 0.0],
                              [0.0, 0.1, -0.1],
                              [-0.1, 0.0, 0.1]
                              ])
WINDOW_SIZE = (600, 600)
SIMULATION_SIZE = np.array(WINDOW_SIZE, dtype=np.float64)
PARTICLE_COUNT = 100
PARTICLE_COLORS = [[255,0,0],
                   [0,255,0],
                   [0,0,255]
                   ]
PARTICLE_RADIUS = 3
TIME_SCALING = 0.001
CUTOFF_DISTANCE  = 100.0
VISCOSITY = 0.3

particles = []

#===================================================================================================
#                                            PARTICLE MODEL
#===================================================================================================
class Particle:

    last_id = 0

    def __init__(self, 
                 variant=0,
                 position=np.array([0.0, 0.0]),
                 velocity=np.array([0.0, 0.0]),
                 acceleration=np.array([0.0, 0.0])
                 ):
        self.id = Particle.last_id
        Particle.last_id += 1
        self.position = position
        self.velocity = velocity
        self.acceleration = acceleration
        self.variant = variant

    def __eq__(self, other):
        return self.id == other.id

def fill_with_random_particles(particle_count):
    for _ in range(particle_count):
        variant = np.random.randint(VARIANT_COUNT)
        position = np.random.rand(2) * SIMULATION_SIZE
        particles.append(Particle(variant, position))


def update_particles(dt):
    for target in particles:
        total_force = [0.0, 0.0]
        for source in particles:
            if target == source:
                continue
            distance = np.linalg.norm(source.position-target.position)
            if distance > CUTOFF_DISTANCE:
                continue
            distance_x = target.position[0] - source.position[0]
            distance_y = target.position[1] - source.position[1]
            force = distance * VARIANT_RELATIONS[source.variant, target.variant]
            force_x = force * distance_x / distance
            force_y = force * distance_y / distance
            total_force[0] += force_x
            total_force[1] += force_y
        velocity = np.linalg.norm(target.velocity)
        dampening = velocity * VISCOSITY
        if total_force[0] > 0:
            total_force[0] =  total_force[0] - dampening
            if total_force[0] < 0:
                total_force[0] = 0
        if total_force[1] > 0:
            total_force[1] =  total_force[0] - dampening
            if total_force[1] < 0:
                total_force[1] = 0
        if total_force[0] < 0:
            total_force[0] =  total_force[0] + dampening
            if total_force[0] > 0:
                total_force[0] = 0
        if total_force[1] < 0:
            total_force[1] =  total_force[0] + dampening
            if total_force[1] > 0:
                total_force[1] = 0
        
        target.acceleration = np.array(total_force)
    
    for particle in particles:
        particle.velocity = particle.velocity + particle.acceleration * dt
        particle.position = particle.position + particle.velocity * dt
        while particle.position[0] < 0:
            particle.position[0] = particle.position[0] + SIMULATION_SIZE[0]
        while particle.position[0] > SIMULATION_SIZE[0]:
            particle.position[0] = particle.position[0] - SIMULATION_SIZE[0]
        while particle.position[1] < 0:
            particle.position[1] = particle.position[1] + SIMULATION_SIZE[1]
        while particle.position[1] > SIMULATION_SIZE[1]:
            particle.position[1] = particle.position[1] - SIMULATION_SIZE[1]


#===================================================================================================
#                                           USER INTERFACE 
#===================================================================================================

def draw_particle(screen, particle):
   pg.draw.circle(screen,
                  PARTICLE_COLORS[particle.variant],
                  np.array(particle.position, dtype=np.int64).tolist(),
                  PARTICLE_RADIUS
                  ) 

def ui_initialize():
    pg.init()
    return pg.display.set_mode(WINDOW_SIZE)

def ui_loop(screen):
    timer = pg.time.Clock()
    running = True
    while running:
        dt = timer.tick()*TIME_SCALING
        screen.fill([0,0,0])
        for particle in particles:
            draw_particle(screen, particle)
        update_particles(dt)
        for event in pg.event.get():
            if event.type == pg.QUIT:
               running = False 
        pg.display.flip() 


def ui_main():
    screen = ui_initialize()
    ui_loop(screen)


if __name__ == '__main__':
    fill_with_random_particles(PARTICLE_COUNT)
    ui_main()
