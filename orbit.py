#Goal of this program is for the cpu to find a way to send the trajectory into orbit

#Essentially we want the tangietal velocity of the object to be within 1% tolerance of the orbit velocity

from main import *

class Projectile:

	def __init__(self, name, pos, vel, acc, color):

		self.name = name

		self.x, self.y, self.z = pos

		self.v_x, self.v_y, self.v_z = vel

		self.a_x, self.a_y, self.a_z = acc

		self.color = color

	def update_position(self, time_step):

		self.v_x += self.a_x * time_step

		self.v_y += self.a_y * time_step

		self.v_z += self.a_z * time_step

		#now update the positions

		self.x += self.v_x * time_step

		self.y += self.v_y * time_step

		self.z += self.v_z * time_step


def get_distance(coords1, coords2):

	total = 0

	for i in range(len(coords1)):

		total += (coords1[i]-coords2[i])**2

	return math.sqrt(total)


def get_orbit_velocity(planet_coords, projectile_coords):

	

def main():


	#start by making two planets

	start_planet = Planet("start", (0,0,0),(0,0,0), (0,0,0), 6*10**24, 10, (0, 255, 0))



	#target_planet = Planet("target", (250*10**6,0,0),(0,0,0), (0,0,0), 6*10**24, 10, (255, 0 ,0))

	#now with the two planets need to give the projectile an initial velocity vector

	rocket = Projectile("rocket", (6*10**6, 0, 0), (0, 0,0), (0, 0, 0), (240, 240, 240)) #have the projectile start on the surface

	rocket.v_x = 9999 #give the rocket some starting thrust

	planets = [start_planet, target_planet]

	projectiles = [rocket]

	simulated_days = 1

	time_step = 15#seconds

	time_steps = int(time_step * 24 * 3600 / time_step)

	last_check = -60

	running = True

	for t in range(time_steps):

		#need to simulate the movement of the projectile

		for each_projectile in projectiles:

			each_projectile.a_x = 0
			each_projectile.a_y = 0
			each_projectile.a_z = 0

			for each_planet in planets:

				#form here calculate the 

				p1 = each_projectile
				p2 = each_planet

				x1 = p1.x
				y1 = p1.y
				z1 = p1.z

				x2 = p2.x
				y2 = p2.y
				z2 = p2.z


				mass2 = p2.mass

				new_a_x, new_a_y, new_a_z = solve_component_acc(x1, x2, y1, y2, z1, z2, mass2, t)

				each_projectile.a_x += new_a_x
				each_projectile.a_y += new_a_y
				each_projectile.a_z += new_a_z

		#now from here need to update the projectile
		for each_projectile in projectiles:

			each_projectile.update_position(time_step)

			#now from here we want to check if its on the target planet

			for each_planet in planets:

				if each_planet.name == "target":

					#now check if the distance of the coordinates are close

					if get_distance((each_planet.x, each_planet.y, each_planet.z), (each_projectile.x, each_projectile.y, each_projectile.z)) < 20*10**6:

						#then its landed


						land_time = t * time_step

						days = int(land_time/(24*3600))

						land_time -= days * 24*3600

						hours = int(land_time/3600)

						land_time -= hours * 3600

						minutes = int(land_time/60)

						land_time -= minutes * 60

						seconds = land_time

						print(f"Projectile Contacted Target Planet\nFlight Time {days} Days, {hours} Hours, {minutes} Minutes, {seconds} Seconds")

						running = False

				elif each_planet.name != "target":

					if get_distance((each_planet.x, each_planet.y, each_planet.z), (each_projectile.x, each_projectile.y, each_projectile.z)) < 6*10**6:

						#in this case its made contact with another planet

						print(f"Mission Failed, Crashed into {each_planet.name}")

						running = False




		if t - last_check > 60000: #basically to check the location

			last_check = t

			for each_projectile in projectiles:

				print(f"{each_projectile.x:,}")

				print(each_projectile.v_x)

				print(each_projectile.a_x)

		if not running:

			break








	return

if __name__ == "__main__":

	main()