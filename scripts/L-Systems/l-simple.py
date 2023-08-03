import pygame
import math
import argparse
import xml.etree.ElementTree as ET
import os
import logging 

#---------------------------------------------------------------------------------------------------
#                                           GLOBALS 
#---------------------------------------------------------------------------------------------------
BG_COLOR = (50, 50, 50)
BLACK = (0, 0, 0)
DEFAULT_RULES = {'F': 'FFF+[+F-F+F]-[-F+FF+F]' }

#---------------------------------------------------------------------------------------------------
#                                          LOGGING 
#---------------------------------------------------------------------------------------------------
logger = logging.getLogger()
iprint = logger.info
wprint = logger.warning
eprint = logger.error

def setup_logger(dataset_path, output_file='console_output.txt'):
    log_formatter = logging.Formatter('%(message)s')

    logfile_path = os.path.join(dataset_path, output_file)
    file_handler = logging.FileHandler(logfile_path)
    file_handler.setFormatter(log_formatter)
    logger.addHandler(file_handler)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(log_formatter)
    logger.addHandler(console_handler)

    logger.setLevel(logging.INFO)


#---------------------------------------------------------------------------------------------------
#                                   LINDENMAYER SYSTEM 
#---------------------------------------------------------------------------------------------------
class LSystem:

    def __init__(self, rules, axiom):
        self.rules = rules
        self.sequence = list(axiom)

    def step(self):
        # If there is no rule use identity rule
        self.sequence = (self.rules.get(element, element) for element in self.sequence)


def lsystem_rule_string(txt):
    entires = txt.split(';')
    rules = {}
    for entry in entires:
        base, target = entry.split('->')
        rules[base] = target
    return rules

def draw_tree(window, axiom, initial_length, angle, starting_point, angle_step):
    stack = []
    position = starting_point
    length = initial_length

    for char in axiom:
        if char == 'F':
            new_x = position[0] + length * math.cos(math.radians(angle))
            new_y = position[1] - length * math.sin(math.radians(angle))
            pygame.draw.line(window, BLACK, position, (new_x, new_y), 2)
            position = (new_x, new_y)
        elif char == 'f':
            new_x = position[0] + length * math.cos(math.radians(angle))
            new_y = position[1] - length * math.sin(math.radians(angle))
            position = (new_x, new_y)
        elif char == '+':
            angle -= angle_step 
        elif char == '-':
            angle += angle_step
        elif char == '[':
            stack.append((position, angle))
        elif char == ']':
            position, angle = stack.pop()

    pygame.display.update()
#---------------------------------------------------------------------------------------------------
#                                      MAIN FUNCTION 
#---------------------------------------------------------------------------------------------------
DEFAULT_AXIOM = 'F'
DEFAULT_ANGLE_STEP = 90.0

def integer_pair(txt):
    values = txt.split('x')
    return (int(values[0]), int(values[1]))

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--window_size', type=integer_pair, default=(800, 600),
                        help='Size of display window.')
    parser.add_argument('--starting_point', type=integer_pair, default=(400, 300),
                        help='Point at which tree root will appear.')
    parser.add_argument('-r', '--rules', type=lsystem_rule_string, default=DEFAULT_RULES,
                        help='Rules of Lindenmayer system writtne as BASE1->TARGET1;BASE2->TARGET2')
    parser.add_argument('-a', '--axiom', type=str, default=DEFAULT_AXIOM,
                        help='Axiom from which model will be grown')
    parser.add_argument('--angle_step', type=float, default=DEFAULT_ANGLE_STEP,
                        help='Angle at which drawing will move angle')
    parser.add_argument('--g', '--generations', type=int, default=5,
                        help='Number of generation for which Lsystem will be ran.')
    return parser.parse_args()


def main(args):
    window = pygame.display.set_mode(args.window_size)
    pygame.display.set_caption("Lindenmayer Tree")


    l_system = LSystem(args.rules, args.axiom)

    for _ in range(5):
        l_system.step()

    window.fill(BG_COLOR)
    draw_tree(window, l_system.sequence, 10, 0, args.starting_point, args.angle_step)

    # Keep the window open until the user closes it
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    pygame.quit()


if __name__ == '__main__':
    args = parse_arguments()
    main(args)




