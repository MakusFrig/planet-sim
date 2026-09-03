#main file for physics simulation

#some imports
import pygame
import sys

gravity_cof = 0.15

class Planet:

	def __init__(self, name, x, y, v_x, v_y, a_x, a_y, mass, radius, color):

		self.name = name

		self.x = x

		self.y = y

		self.v_x = v_x

		self.v_y = v_y

		self.a_x = a_x

		self.a_y = a_y

		self.mass = mass

		self.radius = radius

		self.color = color

	def update_position(self, time_step, bounds):

		#start by updating the velocities

		self.v_x += self.a_x * time_step

		self.v_y += self.a_y * time_step

		#now update the positions

		self.x += self.v_x * time_step

		self.y += self.v_y * time_step

		self.x = min(max(self.x, bounds[0]), bounds[1])

		self.y = min(max(self.y, bounds[2]), bounds[3])




def solve_component_acc(d1, d2, mass1, mass2):

	d = d2-d1 #this is for the correct +- of the thing

	if d == 0:

		return 0

	cof = -1 if d < 0 else 1

	acc = min(gravity_cof * mass2 / d**2, 0.01)

	return acc * cof



# 1. Initialize Pygame
pygame.init()

# 2. Set up the Screen Dimensions
SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 800
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Planet Simulation")

#define some variables for translating the coordinates
half_x = SCREEN_WIDTH/2
half_y = SCREEN_HEIGHT/2

#create the bounds for the screen so that planets dont go off screen
bounds = [-half_x, half_x, -half_y, half_y]

# 3. Create a Clock to manage frame rates (FPS)
clock = pygame.time.Clock()

# Define Colors (RGB format)
BACKGROUND_COLOR = (30, 30, 40)    # Dark gray
PLAYER_COLOR = (0, 255, 128)        # Mint green
p1_color = (255, 0, 0) #red
p2_color = (0, 255, 0) #green


#from here lets create a systems

planet1 = Planet("planet1", -50, 0, 0, 0.1, 0, 0, 300, 10, p1_color)
planet2 = Planet("planet2", 50, 50, 0, -0.2, 0, 0, 200, 4, p2_color)

planets = [planet1, planet2]

planets_len = range(len(planets))

# 5. Main Game Loop
running = True
while running:
	# --- Event Handling (Inputs) ---
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

	#first we want to update the accelerations of the planets based on one another

	for solve_planet in planets_len:

		for other_planet in planets_len:

			if other_planet == solve_planet:

				continue #because these are the same planet and does not affect each other

			#otherwise solve for the component accelerations

			#start with x

			p1 = planets[solve_planet]
			p2 = planets[other_planet]

			x1 = p1.x
			y1 = p1.y

			x2 = p2.x
			y2 = p2.y

			mass1 = p1.mass
			mass2 = p2.mass

			planets[solve_planet].a_x = solve_component_acc(x1, x2, mass1, mass2)

			planets[solve_planet].a_y = solve_component_acc(y1, y2, mass1, mass2)

	#from here all the accelerations are updated

	for each_planet in planets:

		each_planet.update_position(time_step=10, bounds=bounds)






	# --- Drawing/Rendering ---
	# Fill the background to wipe away drawings from the last frame
	screen.fill(BACKGROUND_COLOR)

	#from here we want to draw the planets

	for each_planet in planets:

		#from here need to figure out how to translate x,y to the pygame screen

		new_x = half_x + each_planet.x

		new_y = half_y - each_planet.y

		pygame.draw.circle(screen, each_planet.color, (new_x, new_y), each_planet.radius, width=0)



	# Refresh the display with everything drawn this frame
	pygame.display.flip()

	# Cap the frame rate at 60 FPS
	clock.tick(60)

# 6. Cleanly close everything down
pygame.quit()
sys.exit()
