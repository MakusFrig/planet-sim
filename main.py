#main file for physics simulation

#some imports
import pygame
import sys
import math
import os
from PIL import Image
import glob

gravity_cof = 6*10**-11

os.makedirs("frames", exist_ok=True)

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

		self.previous_positions = []

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





#Initialize Pygame
pygame.init()

#Set up the Screen Dimensions
SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 800
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Planet Simulation")

#define some variables for translating the coordinates
half_x = SCREEN_WIDTH/2
half_y = SCREEN_HEIGHT/2

#create the bounds for the screen so that planets dont go off screen
bounds = [-half_x, half_x, -half_y, half_y]

#Create a Clock to manage frame rates (FPS)
clock = pygame.time.Clock()
last_time = pygame.time.get_ticks() #this is for measuring real display time
last_time_frame = 0

# Define Colors (RGB format)
BACKGROUND_COLOR = (30, 30, 40)    # Dark gray
PLAYER_COLOR = (0, 255, 128)        # Mint green
p1_color = (255, 165, 0) #orange for sun
p2_color = (255, 180, 180) #star with a tint
p3_color = (180, 255, 180) #blue
p4_color = (180, 180 , 255)


#from here lets create a systems

planet1 = Planet("earth", 0, 0, 0, 0, 0, 0, 6*10**24, 10, p1_color)
planet2 = Planet("moon", 200*10**6, 0, 0, 1200, 0, 0, 5*10**22, 3, p2_color)
planet3 = Planet("new_moon", 0, 300*10**6, -1100, 0, 0, 0, 2*10**22, 3, p3_color)
planet4 = Planet("new_moon_2", 0, -250*10**6, 1150, 0, 0, 0, 2*10**22, 3, p4_color)

planets = [planet1, planet2, planet3, planet4]

planets_len = range(len(planets))

t = 0

#Main Game Loop
running = True
while running:
	# --- Event Handling (Inputs) ---
	t+= 1 #make sure to increment
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

	#first we want to update the accelerations of the planets based on one another

	for solve_planet in planets_len:

		planets[solve_planet].a_x = 0
		planets[solve_planet].a_y = 0

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

			
			new_a_x, new_a_y = solve_component_acc(x1, x2, y1, y2, mass1, mass2)
			planets[solve_planet].a_x += new_a_x
			planets[solve_planet].a_y += new_a_y
			

	#from here all the accelerations are updated

	for each_planet in planets:

		

		"""if each_planet.name == "earth":
									#just because earth is our reference point
									continue"""

		for i in range(20):

			each_planet.update_position(time_step=60, bounds=bounds)






	# --- Drawing/Rendering ---
	# Fill the background to wipe away drawings from the last frame
	screen.fill((0,0,0))

	#from here we want to draw the planets

	for each_planet in planets:

		#from here need to figure out how to translate x,y to the pygame screen

		new_x = half_x + min(max(int(each_planet.x*10**-6), bounds[0]), bounds[1])

		new_y = half_y - min(max(int(each_planet.y*10**-6), bounds[2]), bounds[3])

		pygame.draw.circle(screen, each_planet.color, (new_x, new_y), each_planet.radius, width=0)

		#now from here print the past positions

		for i in each_planet.previous_positions:

			new_x = half_x + min(max(int(i[0]*10**-6), bounds[0]), bounds[1])

			new_y = half_y - min(max(int(i[1]*10**-6), bounds[2]), bounds[3])

			pygame.draw.circle(screen, each_planet.color, (new_x, new_y), 1, width=0)





	# Refresh the display with everything drawn this frame
	pygame.display.flip()

	# Cap the frame rate at 60 FPS
	clock.tick(60)

	current_time = pygame.time.get_ticks()



	if current_time - last_time > 50: #1000ms have passed in real time

		last_time = current_time

		for each_planet in planets:

			each_planet.previous_positions.append([each_planet.x, each_planet.y])

			if len(each_planet.previous_positions) > 50:

				each_planet.previous_positions.pop(0)

	#from here we want to check if we want to add this to the frame

	if int((current_time-last_time_frame)/1000 ) > last_time_frame:

		

		filename = f"frames/frame_{last_time_frame:05d}.png"

		last_time_frame += 1 #basically take a frame every second

		pygame.image.save(screen, filename)

		print(f"Saved {filename}")

	if t > 20*60:

		running = False

#Cleanly close everything down
pygame.quit()

#from here create the video from the frames

files = sorted(glob.glob("frames/*.png"))

images = [Image.open(file) for file in files]

images[0].save(
    "simulation.gif",
    save_all=True,
    append_images=images[1:],
    duration=250,  # milliseconds per frame
    loop=0
)

print("GIF created!")


sys.exit()
