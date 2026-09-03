#main file for physics simulation

#some imports
import pygame
import sys
import math


gravity_cof = 6*10**-11

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

		"""self.x = min(max(self.x, bounds[0]), bounds[1])
		
		self.y = min(max(self.y, bounds[2]), bounds[3])"""



def solve_component_acc(x1, x2, y1, y2, mass1, mass2):

	dx = x2-x1 #this is so the positive negative is correct

	dy = y2-y1

	d = math.sqrt(dx**2 + dy**2)

	if d == 0:

		return 0



	acc = min(gravity_cof * mass2 / d**2, 10)

	acc_x =  acc *dx/d

	acc_y = acc * dy/d

	return acc_x, acc_y


"""def solve_component_acc(d1, d2, mass1, mass2):

	d = d2-d1 #this is for the correct +- of the thing



	if d == 0:

		return 0

	cof = -1 if d < 0 else 1

	acc = min(gravity_cof * mass2 / d**2, 10)

	print(acc)

	return acc * cof
"""


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
p3_color = (0, 0, 255) #blue


#from here lets create a systems

planet1 = Planet("earth", 0, 0, 0, 0, 0, 0, 6*10**24, 10, p1_color)
planet2 = Planet("moon", 200*10**6, 0, 0, 1200, 0, 0, 5*10**22, 2, p2_color)
#planet3 = Planet("planet3", 25, -50, 0, 0, 0, 0, 400, 5, p3_color)

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

			planets[solve_planet].a_x, planets[solve_planet].a_y = solve_component_acc(x1, x2, y1, y2, mass1, mass2)

			

	#from here all the accelerations are updated

	for each_planet in planets:

		

		if each_planet.name == "earth":
			#just because earth is our reference point
			continue

		for i in range(20):

			each_planet.update_position(time_step=60, bounds=bounds)






	# --- Drawing/Rendering ---
	# Fill the background to wipe away drawings from the last frame
	#screen.fill(BACKGROUND_COLOR)

	#from here we want to draw the planets

	for each_planet in planets:

		#from here need to figure out how to translate x,y to the pygame screen

		new_x = half_x + min(max(int(each_planet.x*10**-6), bounds[0]), bounds[1])

		new_y = half_y - min(max(int(each_planet.y*10**-6), bounds[2]), bounds[3])

		pygame.draw.circle(screen, each_planet.color, (new_x, new_y), each_planet.radius, width=0)



	# Refresh the display with everything drawn this frame
	pygame.display.flip()

	# Cap the frame rate at 60 FPS
	clock.tick(60)

# 6. Cleanly close everything down
pygame.quit()
sys.exit()
