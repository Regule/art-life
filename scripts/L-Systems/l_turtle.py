from math import cos, sin
import pygame as pg

#===================================================================================================
#                                               TURTLE CODE
#===================================================================================================
class TurtlePosition:

    def __init__(self, x, y, angle):
        self.x = x
        self.y = y
        self.angle = angle

    
    def update(self, velocity, dt):
       distance = velocity.linear * dt
       turn = velocity.angular * dt
       print(f'D={distance} T={turn}')
       self.x += distance * cos(self.angle)
       self.y += distance * sin(self.angle)
       self.angle += turn


class TurtleVelocity:

    def __init__(self, linear=0.0, angular=0.0):
        self.linear = linear
        self.angular = angular

class TurtleControler:

    def __init__(self):
        pass

    def update(self):
        return TurtleVelocity(50,7)

class Turtle:

    def __init__(self, position):
        self.position = position
        self.velocity = TurtleVelocity()
        self.max_velocity = TurtleVelocity(10, 3)
        self.controler = TurtleControler()

    def update(self, dt):
        self.position.update(self.velocity, dt)
        self.velocity = self.controler.update()

#===================================================================================================
#                                              PYGAME CODE 
#===================================================================================================

class Display:
    
    BACKGROUND_BRIGHTNESS = 50
    MAX_BRIGHTNESS = 255
    BRIGHTNESS_RANGE = MAX_BRIGHTNESS-BACKGROUND_BRIGHTNESS
    TRAIL_ALPHA = 80
    TRAIL_SIZE = 10

    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)

    def __init__(self, window_size):
        self.window_size = window_size
        self.screen = None

    def init(self):
        self.screen = pg.display.set_mode(self.window_size)
        pg.display.set_caption('L-TURTLE')
        self.trail_surface = pg.Surface(self.window_size)
        self.trail_surface.set_alpha(Display.TRAIL_ALPHA)

    def update(self, turtle_position):
        pg.draw.ellipse(self.trail_surface,
                        Display.RED, 
                        (turtle_position.x - Display.TRAIL_SIZE// 2,
                         turtle_position.y - Display.TRAIL_SIZE // 2, 
                         Display.TRAIL_SIZE, Display.TRAIL_SIZE
                         )
                        )
        self.screen.fill(Display.BLACK)
        self.screen.blit(self.trail_surface, (0, 0))
    
    def flip(self):
        pg.display.flip() 

class KeyboardHandler:

    def __init__(self, simulation_engine):
        self.simulation_engine = simulation_engine

    def handle_event(self, event):
        if event.key == ord('q'):
            self.simulation_engine.state.running = False
        elif event.key == ord('p'):
            self.simulation_engine.state.toggle_pause()


class SimulationState:

    MILLISECOND_TO_SECOND_RATIO = 1000

    def __init__(self):
        self.running = False
        self.paused = False
        self.clock = pg.time.Clock()

    def init(self):
        self.running = True
        self.clock.tick()

    def toggle_pause(self):
        self.paused = not self.paused

    def tick(self):
        if not self.paused:
            return self.clock.tick()/SimulationState.MILLISECOND_TO_SECOND_RATIO
        return 0

class SimulationEngine:

    def __init__(self):
        self.state = SimulationState()
        self.display = Display((800,800))
        self.keyboard = KeyboardHandler(self)
        init_position = TurtlePosition(400.0, 400.0, 0.0)
        self.turtle = Turtle(init_position)

    def init(self):
        pg.init()
        self.state.init()
        self.display.init()


    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.state.running = False
            elif event.type == pg.KEYDOWN:
                self.keyboard.handle_event(event)

    def run(self):
        while self.state.running:
            self.display.update(self.turtle.position)
            self.display.flip()
            self.handle_events()
            dt = self.state.tick()
            self.turtle.update(dt)

#===================================================================================================
#                                         MAIN FUNCTION 
#===================================================================================================

def main():
    engine = SimulationEngine()
    engine.init()
    engine.run()

if __name__ == '__main__':
    main()

