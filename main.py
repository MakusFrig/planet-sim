#main file for physics simulation

#some imports
import pygame
import sys
import math
import os
from PIL import Image
import glob
import random

gravity_cof = 6*10**-11

os.makedirs("frames", exist_ok=True)
os.makedirs("frames/xy", exist_ok=True)
os.makedirs("frames/xz", exist_ok=True)
os.makedirs("frames/yz", exist_ok=True)

class Planet:

	def __init__(self, name, pos=(0, 0, 0), vel=(0,0,0), acc=(0,0,0), mass=1, radius=1, color=(255, 255, 255)):

		self.name = name

		self.x, self.y, self.z = pos

		self.v_x, self.v_y, self.v_z = vel

		self.a_x, self.a_y, self.a_z = acc

		self.mass = mass

		self.radius = radius

		self.color = color

		self.previous_positions = []

	def update_position(self, time_step):

		#start by updating the velocities

		self.v_x += self.a_x * time_step

		self.v_y += self.a_y * time_step

		self.v_z += self.a_z * time_step

		#now update the positions

		self.x += self.v_x * time_step

		self.y += self.v_y * time_step

		self.z += self.v_z * time_step

		"""self.x = min(max(self.x, bounds[0]), bounds[1])
		
		self.y = min(max(self.y, bounds[2]), bounds[3])"""



def solve_component_acc(x1, x2, y1, y2, z1, z2, mass1, mass2):

	dx = x2-x1 #this is so the positive negative is correct

	dy = y2-y1

	dz = z2-z1

	d = math.sqrt(dx**2 + dy**2 + dz**2)

	if d == 0:

		return 0



	acc = min(gravity_cof * mass2 / d**2, 10)

	acc_x =  acc *dx/d

	acc_y = acc * dy/d

	acc_z = acc * dz/d

	return acc_x, acc_y, acc_z

#needed a function for drawing an axis onto the screen
def draw_axis_watermark(screen, vertical, horizontal):
    # Position of the origin
    origin = (60, screen.get_height() - 60)

    # Length of the axes
    length = 35

    # Colors
    x_color = (255, 80, 80)    # Red
    y_color = (80, 255, 80)    # Green
    white = (255, 255, 255)

    # Draw X axis
    pygame.draw.line(
        screen,
        x_color,
        origin,
        (origin[0] + length, origin[1]),
        2
    )

    # Draw Y axis
    pygame.draw.line(
        screen,
        y_color,
        origin,
        (origin[0], origin[1] - length),
        2
    )

    # Arrowheads
    pygame.draw.polygon(
        screen,
        x_color,
        [
            (origin[0] + length, origin[1]),
            (origin[0] + length - 7, origin[1] - 4),
            (origin[0] + length - 7, origin[1] + 4)
        ]
    )

    pygame.draw.polygon(
        screen,
        y_color,
        [
            (origin[0], origin[1] - length),
            (origin[0] - 4, origin[1] - length + 7),
            (origin[0] + 4, origin[1] - length + 7)
        ]
    )

    # Labels
    font = pygame.font.Font(None, 22)

    x_text = font.render(horizontal, True, x_color)
    y_text = font.render(vertical, True, y_color)

    screen.blit(
        x_text,
        (origin[0] + length + 5, origin[1] - 10)
    )

    screen.blit(
        y_text,
        (origin[0] - 6, origin[1] - length - 20)
    )


#Initialize Pygame
pygame.init()

#Set up the Screen Dimensions
SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 800
screen = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))

#define some variables for translating the coordinates
half_x = SCREEN_WIDTH/2
half_y = SCREEN_HEIGHT/2

#create the bounds for the screen so that planets dont go off screen
bounds = [-half_x, half_x, -half_y, half_y]

#Create a Clock to manage frame rates (FPS)


# Define Colors (RGB format)
BACKGROUND_COLOR = (30, 30, 40)    # Dark gray
PLAYER_COLOR = (0, 255, 128)        # Mint green
sun_color = (255, 165, 0) #orange for sun
p2_color = (255, 180, 180) #star with a tint
p3_color = (180, 255, 180) #light blue
p4_color = (180, 180 , 255) #light green


#from here lets create a systems

planet1 = Planet("earth", (0,0,100*10**6),(0,0,0), (0,0,0), 6*10**24, 10, sun_color)
planet2 = Planet("moon", (200*10**6, 0, 0), (0, 1100, 100), (0,0,0), 5*10**22, 3, p2_color)
planet3 = Planet("new_moon", (0, 200*10**6, 0), (-1000, 0,0), (0,0,0), 2*10**22, 3, p3_color)
planet4 = Planet("new_moon_2", (0,-250*10**6, -150*10**6), (1050, 0, 0), (0,0,0), 2*10**22, 3, p4_color)

planets = [planet1, planet2, planet3, planet4]

#from here lets generate some random small planets

for i in range(4):

	temp_planet = Planet(
		f"mp{i}",
		(random.randint(100*10**6, 300*10**6)*random.choice([-1, 1]), random.randint(100*10**6, 300*10**6)*random.choice([-1, 1]), random.randint(100*10**6, 300*10**6)*random.choice([-1, 1])), #starting position
		(random.randint(500, 750)*random.choice([-1, 1]), random.randint(500, 750)*random.choice([-1, 1]),random.randint(500, 750)*random.choice([-1, 1])), #velocity
		(0,0,0), #acceleration
		random.randint(10**20, 10**22), #mass
		2, #radius
		(random.randint(180, 255), random.randint(180, 255), random.randint(180, 255)) #color
	)

	planets.append(temp_planet)



planets_len = range(len(planets))


last_time = 0
last_time_frame = 0
frame=0

#from here create the simulation loop outside of the pygame thing
time_step = 60 #60 seconds or 1 minute
time_steps = 12*24*30 #each time step is approximatley 20 minutes, so *3 is one hour, 24 is day and 30 is  amonth
for t in range(time_steps):

	#from here update the system, generate the plots

	#first we want to update the accelerations of the planets based on one another

	for solve_planet in planets_len:

		planets[solve_planet].a_x = 0
		planets[solve_planet].a_y = 0
		planets[solve_planet].a_z = 0

		for other_planet in planets_len:

			if other_planet == solve_planet:

				continue #because these are the same planet and does not affect each other

			#otherwise solve for the component accelerations

			#start with x

			p1 = planets[solve_planet]
			p2 = planets[other_planet]

			x1 = p1.x
			y1 = p1.y
			z1 = p1.z

			x2 = p2.x
			y2 = p2.y
			z2 = p2.z

			mass1 = p1.mass
			mass2 = p2.mass

			
			new_a_x, new_a_y, new_a_z = solve_component_acc(x1, x2, y1, y2, z1, z2, mass1, mass2)
			planets[solve_planet].a_x += new_a_x
			planets[solve_planet].a_y += new_a_y
			planets[solve_planet].a_z += new_a_z

	#from here all the accelerations are updated

	for each_planet in planets:



		for i in range(5):

			each_planet.update_position(time_step=time_step)

	#now things are updated we need to check if we add to the trail

	if t - last_time >= 6: #basically every two hours of simulation it adds the new position

		last_time = t #reset the last time

		for each_planet in planets:

			each_planet.previous_positions.append([each_planet.x, each_planet.y, each_planet.z])

			if len(each_planet.previous_positions) > 50: #make sure the trail isnt too long

				each_planet.previous_positions.pop(0)

	if t - last_time_frame >= 36: #basically generate a snapshot every 12 hours

		last_time_frame = t

		#now we have the trail setup lets generate images at this time

		#start with the x, y

		screen.fill((0,0,0))
		draw_axis_watermark(screen, vertical="Y", horizontal="X")

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

		#from here save it

		filename = f"frames/xy/frame_{frame:05d}.png"

		frame += 1 #basically take a frame every second

		pygame.image.save(screen, filename)

		print(f"Saved {filename}")

		#now do the same for the xz axis

		screen.fill((0,0,0))
		draw_axis_watermark(screen, vertical="Z", horizontal="X")

		for each_planet in planets:

			#from here need to figure out how to translate x,y to the pygame screen

			new_x = half_x + min(max(int(each_planet.x*10**-6), bounds[0]), bounds[1])

			new_y = half_y - min(max(int(each_planet.z*10**-6), bounds[2]), bounds[3])

			pygame.draw.circle(screen, each_planet.color, (new_x, new_y), each_planet.radius, width=0)

			#now from here print the past positions

			for i in each_planet.previous_positions:

				new_x = half_x + min(max(int(i[0]*10**-6), bounds[0]), bounds[1])

				new_y = half_y - min(max(int(i[2]*10**-6), bounds[2]), bounds[3])

				pygame.draw.circle(screen, each_planet.color, (new_x, new_y), 1, width=0)

		#from here save it

		filename = f"frames/xz/frame_{frame:05d}.png"

		frame += 1 #basically take a frame every second

		pygame.image.save(screen, filename)

		print(f"Saved {filename}")

		#now from here do the yz axis

		screen.fill((0,0,0))
		draw_axis_watermark(screen, vertical="Z", horizontal="Y")

		for each_planet in planets:

			#from here need to figure out how to translate x,y to the pygame screen

			new_x = half_x + min(max(int(each_planet.y*10**-6), bounds[0]), bounds[1])

			new_y = half_y - min(max(int(each_planet.z*10**-6), bounds[2]), bounds[3])

			pygame.draw.circle(screen, each_planet.color, (new_x, new_y), each_planet.radius, width=0)

			#now from here print the past positions

			for i in each_planet.previous_positions:

				new_x = half_x + min(max(int(i[1]*10**-6), bounds[0]), bounds[1])

				new_y = half_y - min(max(int(i[2]*10**-6), bounds[2]), bounds[3])

				pygame.draw.circle(screen, each_planet.color, (new_x, new_y), 1, width=0)

		#from here save it

		filename = f"frames/yz/frame_{frame:05d}.png"

		frame += 1 #basically take a frame every second

		pygame.image.save(screen, filename)

		print(f"Saved {filename}")


#Cleanly close everything down
pygame.quit()

#from here create the video from the frames

files = sorted(glob.glob("frames/xy/*.png"))

images = [Image.open(file) for file in files]

images[0].save(
    "simulationxy.gif",
    save_all=True,
    append_images=images[1:],
    duration=50,  # milliseconds per frame
    loop=0
)

print("GIF created!")

files = sorted(glob.glob("frames/xz/*.png"))

images = [Image.open(file) for file in files]

images[0].save(
    "simulationxz.gif",
    save_all=True,
    append_images=images[1:],
    duration=50,  # milliseconds per frame
    loop=0
)

print("GIF created!")

files = sorted(glob.glob("frames/yz/*.png"))

images = [Image.open(file) for file in files]

images[0].save(
    "simulationyz.gif",
    save_all=True,
    append_images=images[1:],
    duration=50,  # milliseconds per frame
    loop=0
)

print("GIF created!")


sys.exit()
