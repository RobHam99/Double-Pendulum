import numpy as np
import pygame

def acc1(theta_1, theta_2, mass1, mass2, length1, length2, omega_1, omega_2, g):

    """
    This function is the differential equation for the acceleration of the first mass.
    Each variable is a bit of the equation added together in the return statement,
    as the equation is very long.
    """

    t1_1 = -g * (2 * mass1 + mass2) * np.sin(theta_1)
    t1_2 = -mass2 * g * np.sin(theta_1 - 2 * theta_2)
    t1_3 = -2 * np.sin(theta_1 - theta_2)
    t1_4 = mass2 * ((omega_2 * omega_2) * length2 + (omega_1 * omega_1) * length1 * np.cos(theta_1 - theta_2))
    t1_d = length1 * (2 * mass1 + mass2 - mass2 * np.cos(2 * theta_1 - 2 * theta_2))

    return (t1_1 + t1_2 + (t1_3 * t1_4)) / t1_d


def acc2(theta_1, theta_2, mass1, mass2, length1, length2, omega_1, omega_2, g):

    """
    This function is the differential equation for the acceleration of the second mass.
    Each variable is a bit of the equation added together in the return statement,
    as the equation is very long.
    """

    t2_1 = 2 * np.sin(theta_1 - theta_2)
    t2_2 = (omega_1 * omega_1) * length1 * (mass1 + mass2) + g * (mass1 + mass2) * np.cos(theta_1)
    t2_3 = (omega_2 * omega_2) * length2 * mass2 * np.cos(theta_1 - theta_2)
    t2_d = length2 * (2 * mass1 + mass2 - mass2 * np.cos(2 * theta_1 - 2 * theta_2))

    return (t2_1 * (t2_2 + t2_3)) / t2_d


class pendulum:
    def __init__(self, angle_1, angle_2, mass_1, mass_2, length_1, length_2, velocity_1, velocity_2, gravity):
        self.angle_1 = angle_1
        self.angle_2 = angle_2
        self.mass_1 = mass_1
        self.mass_2 = mass_2
        self.length_1 = length_1
        self.length_2 = length_2
        self.velocity_1 = velocity_1
        self.velocity_2 = velocity_2
        self.gravity = gravity

    def calculate(self):

        """
        This function returns the new position of each x and y point for both masses.
        It also returns the acceleration, velocity and angle for each mass respectively.
        """

        acc_1 = acc1(self.angle_1, self.angle_2, self.mass_1, self.mass_2, self.length_1, self.length_2, self.velocity_1, self.velocity_2, self.gravity)
        acc_2 = acc2(self.angle_1, self.angle_2, self.mass_1, self.mass_2, self.length_1, self.length_2, self.velocity_1, self.velocity_2, self.gravity)

        change_x = self.length_1 * np.sin(self.angle_1) + origin_x
        change_y = self.length_1 * np.cos(self.angle_1) + origin_y

        change_x2 = change_x + self.length_2 * np.sin(self.angle_2)
        change_y2 = change_y + self.length_2 * np.cos(self.angle_2)

        self.velocity_1 += acc_1
        self.velocity_2 += acc_2
        self.angle_1 += self.velocity_1
        self.angle_2 += self.velocity_2


        return change_x, change_y, change_x2, change_y2, acc_1, acc_2, self.velocity_1, self.velocity_2, self.angle_1, self.angle_2

    def display(self):

        """
        This function uses PyGame GUI to draw lines from the adjusted origin to each mass.
        """

        change_x, change_y, change_x2, change_y2, acc_1, acc_2, v1, v2, a1, a2 = self.calculate()

        pygame.draw.line(screen, color, (origin_x, origin_y), (change_x, change_y), 6)
        pygame.draw.circle(screen, color, (int(change_x), int(change_y)), 15)
        pygame.draw.line(screen, color, (change_x, change_y), (change_x2, change_y2), 6)
        pygame.draw.circle(screen, color, (int(change_x2), int(change_y2)), 15)
        pygame.display.update()

        return v1, v2, a1, a2


# Setting up initial stuff
pygame.init()
screen = pygame.display.set_mode((800, 600))
w, h = pygame.display.get_surface().get_size()
screen.fill((255, 255, 255))
pygame.display.set_caption('Double Pendulum Simulation')
clock = pygame.time.Clock()
color = (0, 0, 0)

# Adjust origin because PyGame origin starts at top left and we need middle top
# Pendulum top can be lowered or raised by adjusting origin_y
# e.g. origin_y = 0 will set it to the very top of the screen, I like origin_y = 100
origin_x = w / 2
origin_y = 100

# Initial parameters and counter
mass_1 = 40
mass_2 = 40
length_1 = 200
length_2 = 200

# Sim spins out of control at g = 9.8, maybe because no damping factors?
# Not sure to be honest.

gravity = 2

angle_1 = np.radians(90)
angle_2 = np.radians(90)

velocity_1 = 0
velocity_2 = 0
acc_1 = 0
acc_2 = 0

i = 0

running = True
while running:
    clock.tick(30)
    screen.fill((255, 255, 255))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()

    # The if statement is needed because the class needs to be defined once based on initial variables
    # but every time after it needs the updated variables from the previous loop
    if i == 0:
        sim = pendulum(angle_1, angle_2, mass_1, mass_2, length_1, length_2, 0, 0, 2)
        v1, v2, a1, a2 = sim.display()

    else:
        sim = pendulum(a1, a2, mass_1, mass_2, length_1, length_2, v1, v2, gravity)
        v1, v2, a1, a2 = sim.display()

    i += 1



