# A_VOID
# BY: avan

# FONT SOURCE:  https://www.1001fonts.com

# FONT STYLE: Good Times Regular by Raymond Larabie

# NEW PHYSICS COLLISION
"""
MUSIC:
"Odyssey"
Kevin MacLeod (incompetech.com)
Licensed under Creative Commons: By Attribution 3.0
http://creativecommons.org/licenses/by/3.0/
"""


import pygame
import sys 
import random
import time
import math
import json
import os

from pygame.locals import *

pygame.init()
pygame.mixer.init()

def find_data_file(filename):
    if getattr(sys, 'frozen', False):
        datadir = os.path.dirname(sys.executable)
    else:
        datadir = os.path.dirname(__file__)
    return os.path.join(datadir, filename)


WINDOW_WIDTH = 1100
WINDOW_HEIGHT = 650
WINDOW_COLOR = (25, 33, 40)
WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
WINDOW.set_alpha(None)

pygame.display.set_caption("avan")

FONT_COLOR = (255, 255, 255)


file_path = find_data_file("a_void_data.json")
with open(file_path, 'r') as user_data:
	topscorers_data = json.load(user_data)["topscorers"]

score = "0"
username = "ENTER NAME AND SECTION"

font_file_path = find_data_file("good_times_rg.ttf")
font_obj = pygame.font.Font(font_file_path, 15)
big_font_obj = pygame.font.Font(font_file_path, 30)

menu_text_surface = font_obj.render('CLICK TO PLAY',
	False, FONT_COLOR)
menu_surface_rect = menu_text_surface.get_rect()
menu_surface_rect.center = (WINDOW_WIDTH/2.0, WINDOW_HEIGHT/2.0)

title_text_surface = big_font_obj.render('A VOID',
	False, FONT_COLOR)
title_surface_rect = title_text_surface.get_rect()
title_surface_rect.center = (menu_surface_rect.centerx, menu_surface_rect.top - 50)

score_text_surface = font_obj.render('SCORE: ' + score,
	False, FONT_COLOR)
score_surface_rect = score_text_surface.get_rect()
score_surface_rect.bottomleft = (10, WINDOW_HEIGHT - 10)

username_input_rect = pygame.Rect(menu_surface_rect.left - 100,
	menu_surface_rect.bottom + 10, menu_surface_rect.width + 200,
	menu_surface_rect.height + 10)

username_text_surface = font_obj.render(username, False, FONT_COLOR)
username_surface_rect = username_text_surface.get_rect()
username_surface_rect.topleft = (username_input_rect.left + 40,
	username_input_rect.top + 5)


for player in topscorers_data:
	topscorers_data[player]["font_obj"] = font_obj.render(topscorers_data[player]["name"] + 
		" : " + topscorers_data[player]["score"], False, FONT_COLOR)

	topscorers_data[player]["font_rect"] = topscorers_data[player]["font_obj"].get_rect()
	topscorers_data[player]["font_rect"].bottomleft = (10, WINDOW_HEIGHT - 10 - (30*(5-int(player))))

FPS = 60

dead = True
no_of_antimatters = 10
no_of_stars = 15
antimatter_max_radius = 30

music_file_path = find_data_file("odyssey.ogg")
pygame.mixer.music.load(music_file_path)
pygame.mixer.music.play(-1, 12)


class Stars(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)

		self.side = random.randrange(2,10)
		self.color = [random.randrange(150, 256),random.randrange(150, 256),
			random.randrange(150, 256), 150]
		self.sprite_surface = pygame.Surface((self.side * 2, self.side * 2),
			pygame.SRCALPHA, 32).convert_alpha()
		self.sprite_surface.fill(self.color)
		self.rect = self.sprite_surface.get_rect()
		self.rect.topleft = (random.randrange(WINDOW_WIDTH),
			random.randrange(WINDOW_HEIGHT))
		self.speed = 1

	def move(self):
		self.rect.top = self.rect.top + self.speed

	def reset(self, dead):
		self.color = [random.randrange(150, 256),random.randrange(150, 256),
			random.randrange(150, 256), 255]
		if dead:
			self.color[3] = 150
		self.side = random.randrange(2,10)

		self.rect.topleft = (random.randrange(WINDOW_WIDTH),
			random.randrange(-4 * self.side, -2 * self.side))
		self.sprite_surface = pygame.Surface((self.side * 2, self.side * 2),
			pygame.SRCALPHA, 32).convert_alpha()
		self.sprite_surface.fill(self.color)

	def change_color(self):
		if self.color[3] == 255:
			self.color[3] = 150
		else:
			self.color[3] = 255
		self.sprite_surface.fill(self.color)

class Antimatter(pygame.sprite.Sprite):
	def __init__(self, coordinate, antimatter_max_radius, no_of_antimatters):

		pygame.sprite.Sprite.__init__(self)
		self.antimatter_max_radius = antimatter_max_radius
		self.no_of_antimatters = no_of_antimatters
		self.radius = random.randrange(25, self.antimatter_max_radius)
		self.color = (250, 177, 160, 128)
		self.sprite_surface = pygame.Surface((self.radius * 2, self.radius * 2), 
			pygame.SRCALPHA, 32).convert_alpha()
		pygame.draw.circle(self.sprite_surface, self.color, (self.radius, 
			self.radius), self.radius)
		self.rect = self.sprite_surface.get_rect()
		self.rect.topleft = coordinate
		self.direction_x = random.choice((-1, 1))
		self.direction_y = random.choice((-1, 1))
		self.magnitude = 3
		self.speed = [self.direction_x * self.magnitude, \
			self.direction_y * self.magnitude]
	

	def move(self):
		self.speed = [self.direction_x * self.magnitude, \
			self.direction_y * self.magnitude]
		self.rect.topleft = (self.rect.left + self.speed[0], 
			self.rect.top + self.speed[1])

	def change_color(self, color):
		self.color = color
		pygame.draw.circle(self.sprite_surface, self.color, (self.radius, 
			self.radius), self.radius)

	def is_collided_with_others(self, group):
		collided = pygame.sprite.spritecollideany(self, group, pygame.sprite.collide_circle)
		return collided

	def is_collided_with_wall(self):
		if (self.rect.top < 0 or self.rect.left < 0 or 
				self.rect.right > WINDOW_WIDTH or 
				self.rect.bottom > WINDOW_HEIGHT):
			return True

	def change_direction(self, collided):
		if (self.rect.top < 0) or (self.rect.bottom > WINDOW_HEIGHT):
			self.direction_y = - self.direction_y
			if self.rect.top < 0:
				self.rect.top = 0
			else:
				self.rect.bottom = WINDOW_HEIGHT


		if ((self.rect.left < 0) or self.rect.right > WINDOW_WIDTH):
			self.direction_x = - self.direction_x
			if self.rect.left < 0:
				self.rect.left = 0
			else:
				self.rect.right = WINDOW_WIDTH

		if collided:
			temp_direction_x = self.direction_x
			temp_direction_y = self.direction_y
			self.direction_x = collided.direction_x
			self.direction_y = collided.direction_y
			collided.direction_x = temp_direction_x
			collided.direction_y = temp_direction_y

	def increase_speed(self):
		self.magnitude = self.magnitude + 0.005


class Matter(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)

		self.radius = 25
		self.color = (129, 236, 236, 128)
		self.sprite_surface = pygame.Surface((self.radius * 2, self.radius * 2), 
			pygame.SRCALPHA, 32).convert_alpha()
		pygame.draw.circle(self.sprite_surface, self.color, (self.radius, 
			self.radius), self.radius)
		self.rect = self.sprite_surface.get_rect()
		self.rect.center = (WINDOW_WIDTH/2.0, WINDOW_HEIGHT - 150)

	def move(self, mouse_pos):
		self.rect.center = mouse_pos

	def is_collided_with(self, other):
		if pygame.sprite.collide_circle(self, other):
			return True

	def change_color(self, color):
		self.color = color
		pygame.draw.circle(self.sprite_surface, self.color, (self.radius, 
			self.radius), self.radius)

stars  =  pygame.sprite.Group()
antimatters = pygame.sprite.Group()
matter_cont = pygame.sprite.GroupSingle()

display_score = False

def generate_stars(no_of_stars):
	for i in range(no_of_stars):
		star  =  Stars()
		stars.add(star)

def generate_coordinates(antimatter_radius, no_of_antimatters):
	prev_x = 0
	prev_y = 0
	x_interval = WINDOW_WIDTH / round((no_of_antimatters/2.0))
	y_interval = WINDOW_HEIGHT / 2.0
	coordinates = []
	for i in range(no_of_antimatters):
		x = random.randrange(prev_x, prev_x + x_interval - 
			2*antimatter_radius - 2)
		y = random.randrange(prev_y, prev_y + y_interval - 
			2*antimatter_radius - 2)
		prev_x = prev_x + x_interval
		if i == round(no_of_antimatters/2.0):
			prev_x = 0
			x = random.randrange(prev_x, prev_x + x_interval - 
				2*antimatter_radius - 2)
			prev_x = prev_x + x_interval
			prev_y = y_interval
			y = random.randrange(prev_y, prev_y + 
				y_interval - 2*antimatter_radius - 2)

		coordinates.append((x, y))
	return coordinates


def generate_antimatter(generate_coordinates):
	coordinates = generate_coordinates()
	no_of_antimatters = len(coordinates)
	for i in range(no_of_antimatters):
		antimatter = Antimatter(coordinates[i], antimatter_max_radius, 
			no_of_antimatters)
		antimatters.add(antimatter)

generate_stars(no_of_stars)
generate_antimatter(
	lambda: generate_coordinates(antimatter_max_radius, no_of_antimatters))

matter = Matter()
matter_cont.add(matter)


running = True
clock = pygame.time.Clock()
username_valid = False

while running:
	clicked = pygame.mouse.get_pressed()
	pressed = pygame.key.get_pressed()
	pygame.mouse.set_visible(False)

	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit()

		if (event.type == pygame.KEYDOWN and dead):
			if event.key == pygame.K_BACKSPACE:
				if not username_valid:
					username = ""
				else:
					username_valid = True
					username = username[:-1]
					if len(username) == 0:
						username = "ENTER NAME AND SECTION"
						username_valid = False
			elif event.key == pygame.K_RETURN:
				pass
			else:
				if not username_valid:
					username = ""
					username_valid = True
				username = username + event.unicode
				username = username.upper()
				if username == "ENTER NAME AND SECTION":
					username_valid = False
	mouse_position = pygame.mouse.get_pos()
	matter.move(mouse_position)
	if matter.rect.top < 0:
		matter.rect.top = 0
	if matter.rect.left < 0:
		matter.rect.left = 0
	if matter.rect.bottom > WINDOW_HEIGHT:
		matter.rect.bottom = WINDOW_HEIGHT
	if matter.rect.right > WINDOW_WIDTH:
		matter.rect.right = WINDOW_WIDTH

	WINDOW.fill(WINDOW_COLOR)
	for star in stars:
		star.move()
		if star.rect.top > WINDOW_HEIGHT:
			star.reset(dead)
		WINDOW.blit(star.sprite_surface, star.rect)

	if dead:

		for antimatter in antimatters:
			antimatter.move()
			antimatters.remove(antimatter)
			collided = antimatter.is_collided_with_others(antimatters)
			if (collided or antimatter.is_collided_with_wall):
				antimatter.change_direction(collided)

			antimatters.add(antimatter)
			WINDOW.blit(antimatter.sprite_surface, antimatter.rect)
		
		WINDOW.blit(matter.sprite_surface, matter.rect)
		for player in topscorers_data:
			WINDOW.blit(topscorers_data[player]["font_obj"], topscorers_data[player]["font_rect"])

		username_text_surface = font_obj.render(username, False, 
			FONT_COLOR)
		username_surface_rect = username_text_surface.get_rect()
		username_surface_rect.center = username_input_rect.center

		WINDOW.blit(username_text_surface, username_surface_rect)

		WINDOW.blit(menu_text_surface, menu_surface_rect)

		if display_score:
			WINDOW.blit(score_text_surface, score_surface_rect)

		WINDOW.blit(title_text_surface, title_surface_rect)

		pygame.draw.rect(WINDOW, (255,255,255), username_input_rect, 2)

		if ((clicked[0] or pressed[K_RETURN]) and 
				username != "ENTER NAME AND SECTION" and username != ""):
			dead = False
			transaction_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
			start_time = pygame.time.get_ticks()
			WINDOW.fill((0,0,0,0))
			score = 0
			topscorer = False
			for antimatter in antimatters:
				antimatter.change_color((250, 177, 160))
			score_surface_rect.bottomleft = (10, WINDOW_HEIGHT - 10)

			matter.change_color((129, 236, 236))
			for star in stars:
				star.change_color()


	else:
		game_time = (pygame.time.get_ticks() - start_time)/1000.0
		score = str(int(game_time * 10))
		WINDOW.blit(matter.sprite_surface, matter.rect)
		for antimatter in antimatters:
			antimatter.move()
			antimatters.remove(antimatter)
			collided = antimatter.is_collided_with_others(antimatters)
			if (collided or antimatter.is_collided_with_wall):
				antimatter.change_direction(collided)

			antimatters.add(antimatter)

			if (math.floor(game_time) != 0  and 
					math.floor(game_time) % 4 == 0):
				antimatter.increase_speed()
			
			if matter.is_collided_with(antimatter):
				dead = True
				antimatters.empty()
				generate_antimatter(
					lambda: generate_coordinates(
						antimatter_max_radius, no_of_antimatters))

				antimatter.change_color((250, 177, 160, 128))
				matter.change_color((129, 236, 236, 128))
				display_score = True
				place = 10
				for player in topscorers_data:
					if int(score) >= int(topscorers_data[player]["score"]):
						if int(place) > int(player):
							place = player
							topscorer = True
				with open(file_path, "r") as user_data:
					user_data = json.load(user_data)
					if topscorer:
						for player in topscorers_data:
							if int(player) >= int(place) and int(player)+1 <= 5:
								user_data["topscorers"][str(int(player)+1)] = {
									"name": topscorers_data[player]["name"],
									"score": topscorers_data[player]["score"]
								}
						user_data["topscorers"][place] = {
							"name": username,
							"score": score
						}
						topscorers_data = user_data["topscorers"]

				user_data["history"][transaction_time] = {
					"name": username,
					"score": score
				}
				with open(file_path, "w") as new_data:
					json.dump(user_data, new_data, indent=4)


				for player in topscorers_data:
					topscorers_data[player]["font_obj"] = font_obj.render(
						topscorers_data[player]["name"] + 
						" : " + topscorers_data[player]["score"], False, 
						FONT_COLOR)

					topscorers_data[player]["font_rect"] = \
						topscorers_data[player]["font_obj"].get_rect()
					topscorers_data[player]["font_rect"].bottomleft = (10, 
						WINDOW_HEIGHT - 10 - (30*(5-int(player))))

				username = "ENTER NAME AND SECTION"
				username_valid = False

				score_surface_rect.midtop = (menu_surface_rect.centerx, 
					menu_surface_rect.top + 100)
				for star in stars:
					star.change_color()
				break
				
			WINDOW.blit(antimatter.sprite_surface, antimatter.rect)

		score_text_surface = font_obj.render('SCORE: ' + score,
			False, FONT_COLOR)

		WINDOW.blit(score_text_surface, score_surface_rect)

	pygame.display.update()
	clock.tick(FPS)