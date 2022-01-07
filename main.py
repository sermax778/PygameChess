# Программа создана студентом КПИ по имени Максим Шестак (17 лет)
# Я начинающий программист и на данный момент хочу достичь уровня Python Junior Developer
# По ходу своего обучения, я заметил, что одна из основополагающих программирования - ООП, остается
# для меня загадкой после всего просмотреного и прочитаного мной материала.
# Именно поэтому я взялся за этот проект - чтобы понять принципы ООП
# Я использовал только базовый ООП без его настоящий приимущиств, например наследственность,
# она бы мне сэкономила тонну времени и под две сотни строк :)

# Эта программа абсолютно не претендует на публикацию абсолютно нигде, это просто пример и хороший опыт
# в использовании библиотеки pygame и ООП

# Если же вы хотите что-то подчерпнуть для себя из этой программы, то есть несколько замечаний и идей
# Замечания:
# -В программе реализованы не самые оптимальные методы решения поставленых задач, но они все интуитивно понятные
#  и просты в обращении
# -Из-за моей неопытности присутствует обин сущетвенный баг, который ломает геймплей, если злоупотреблять этим
#  подробнее о баге см. ст-ки 1071-1077
# -Игра предусмотрена для игры на одном устройстве с одной мышкой, то есть по сетке с другом или с ИИ поиграть не получится
# 
# Идеи:
# -Добавить ход Рокировка, а то он так и не был реализован
# -Добавить список побитых фигур, например с помощью символов Unicode по бокам или снизу на рамке
# -Добавить список ходов, можно в реальном времени или же после партии в виде отдельного окна или файла, который можно скачать
# -Пофиксить баг:), если же вы это сделаете, то обязательно свяжитесь со мной и обьясните как вы это сделали, буду неимоверно благодарен
# -Ввести локальный мультиплеер, по сети (типа мессенджера), даже с примитивным написанием координат клеточек (А1, В2)
# -Добавить ИИ или просто алгоритм, который будет играть за вашего соперника.

# Мои контакты:
# Telegram: @maxflurry69


#Импорт модулей (не все из них используются)
import pygame
from pygame.locals import *
import os
import math
import time

#Инициализация пайгейм
pygame.init()

#Глобальные переменные. Размеры окна, создание окна
s_w = 700 #ширина
s_h = 700 #высота
FPS = 60 
sq = 664 #ширина игрового поля без рамок
one = sq/8 #ширина одной плитки
won = 0 #переменная для фиксации победы

screen = pygame.display.set_mode([s_w, s_h])


# функция фиксации победы
def win(x):
	global won
	if x == "W":
		won = 1
	else:
		won = 2


# порядок создания красных плиточек на поле у ладьи. нужно для того, чтобы ограничить создание красных плиток,
# если по этому направлению стоит другая фигура
def num_plates_rook(fig, moves):
	moves_left = [s for s in moves if s[0]<fig.rect.center[0] and s[1]==fig.rect.center[1]]
	moves_up = [s for s in moves if s[0]==fig.rect.center[0] and s[1]<fig.rect.center[1]]
	moves_down = [s for s in moves if s[0]==fig.rect.center[0] and s[1]>fig.rect.center[1]]
	moves_right = [s for s in moves if s[0]>fig.rect.center[0] and s[1]==fig.rect.center[1]]
	moves_left = moves_left[::-1]
	moves_up = moves_up[::-1]
	return moves_left, moves_up, moves_down, moves_right


# создание красных (черных/серых, далее красных) плиточек (варианты ходов для каждой фигуры)
def red_plate(x, y):
	surf1 = pygame.Surface((75, 75))
	surf1.set_alpha(70)
	surf1.fill((0, 0, 0))
	cent1 = x-37, y-36
	screen.blit(surf1, cent1)
	return cent1

# создание светлокрасных плиточек (когда наводишь мышку на красную плитку)
def light_red(x, y):
	surf1 = pygame.Surface((75, 75))
	surf1.set_alpha(40)
	surf1.fill((255, 0, 0))
	cent1 = x, y
	screen.blit(surf1, cent1)

# создание зеленых плиток - плиток сражений. вариант хода, со следующим уничтожением вражеской фигуры
def green_plate(x, y):
	surf1 = pygame.Surface((75, 75))
	surf1.set_alpha(70)
	surf1.fill((0, 255, 0))
	cent1 = x-37, y-36
	screen.blit(surf1, cent1)
	return cent1


# каждый класс в этой программе состоит из трех частей (функций)

# первая часть - инициация объекта
# дальше каждый класс принимает 6 значений: основная картинка, картинка выделения, центр по оси Ох,
# верхнее значение по оси Оу, цвет фигуры, название фигуры (название нужно только для короля, чтобы фиксировать победу)

# вторая часть - варианты хода. функция срабатывает после нажатия на фигуру и показывает серыми(красными) плитками
# куда может походить данная фигура
# код далеко не совершенен, поэтому для некоторых фигур варианты хода заполнены вручную, а для некоторых через циклы

# третья часть - обновление фигуры. функция срабатывает при нажатии на фигуру.
# именно в этой функции выполняется вся логика движений и боя.



# класс Короля
# после смерти одной из этих фигкр игра заканчивается
# в этой программе нету такого движения, как РОКИРОВКА
class King(pygame.sprite.Sprite):
	def __init__(self, image1, image2, centx1, top1, figcol, name):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load(image1)
		self.image1 = self.image
		self.image.set_colorkey((255, 255, 255))
		self.image2 = pygame.image.load(image2)
		self.rect = self.image.get_rect()
		self.rect.centerx = centx1
		self.rect.top = top1
		self.figcol = figcol
		self.plate_posx = []
		self.plate_posy = []
		self.name = name

	

	def red(self):
		self.plate_posx = []
		self.plate_posy = []
		moves = (
			(self.rect.center[0]+one, self.rect.center[1]+one),
			(self.rect.center[0]+one, self.rect.center[1]-one),
			(self.rect.center[0]-one, self.rect.center[1]+one),
			(self.rect.center[0]-one, self.rect.center[1]-one),
			(self.rect.center[0]+one, self.rect.center[1]),
			(self.rect.center[0]-one, self.rect.center[1]),
			(self.rect.center[0], self.rect.center[1]+one),
			(self.rect.center[0], self.rect.center[1]-one)
		)
		
		if self.figcol == "W":
			for n in moves:
				if n[0]<0 or n[1]<0 or n[0]>s_w or n[1]>s_h:
					pass
				elif n in white_sprites:
					pass
				elif n in black_sprites:
					green_plate(n[0], n[1])
					self.plate_posx.append(green_plate(n[0], n[1])[0])
					self.plate_posy.append(green_plate(n[0], n[1])[1])
				else:
					red_plate(n[0], n[1])
					self.plate_posx.append(red_plate(n[0], n[1])[0])
					self.plate_posy.append(red_plate(n[0], n[1])[1])
		else:
			for n in moves:
				if n[0]<0 or n[1]<0 or n[0]>s_w or n[1]>s_h:
					pass
				elif n in black_sprites:
					pass
				elif n in black_sprites:
					green_plate(n[0], n[1])
					self.plate_posx.append(green_plate(n[0], n[1])[0])
					self.plate_posy.append(green_plate(n[0], n[1])[1])
				else:
					red_plate(n[0], n[1])
					self.plate_posx.append(red_plate(n[0], n[1])[0])
					self.plate_posy.append(red_plate(n[0], n[1])[1])


	def update(self):
		
		if self in clicked_sprites:
			self.image = self.image2
			self.image.set_colorkey((255, 255, 255))
			self.red()
			for n in range(len(self.plate_posx)):
				w_cond = self.plate_posx[n]<=pygame.mouse.get_pos()[0]<=self.plate_posx[n]+75
				h_cond = self.plate_posy[n]<=pygame.mouse.get_pos()[1]<=self.plate_posy[n]+75
				if w_cond and h_cond:
					light_red(self.plate_posx[n], self.plate_posy[n])
					if pygame.mouse.get_pressed()[0]:
						self.rect.centerx = self.plate_posx[n]+37
						self.rect.top = self.plate_posy[n]-4
						if self.figcol == "W":
							if self.rect.center in black_sprites:
								for j in black_figures:
									if self.rect.center == j.rect.center:
										if j.name == "King":
											win("W")
										j.kill()
						else:
							if self.rect.center in white_sprites:
								for j in white_figures:
									if self.rect.center == j.rect.center:
										if j.name == "King":
											win("B")
										j.kill()
						global start
						start += 1
			
		else:
			self.image = self.image1
			self.image.set_colorkey((255, 255, 255))
		



# класс Пешки
# самый длинный класс через большую вариативность в движениях
# в этой программе пешка не может поменятся на какую-то фигуру, если она дошла до конца поля
class Pawn(pygame.sprite.Sprite):
	def __init__(self, image1, image2, centx1, top1, figcol, name):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load(image1)
		self.image1 = self.image
		self.image.set_colorkey((255, 255, 255))
		self.image2 = pygame.image.load(image2)
		self.rect = self.image.get_rect()
		self.rect.centerx = centx1
		self.rect.top = top1
		self.figcol = figcol
		self.plate_posx = []
		self.plate_posy = []
		self.name = name


	def red(self):
		self.plate_posx = []
		self.plate_posy = []
		moves = (
			(self.rect.center[0], self.rect.center[1]-one),
			(self.rect.center[0], self.rect.center[1]-2*one)
		)
		moves1 = ((self.rect.center[0], self.rect.center[1]-one),)
		moves2 = (
			(self.rect.center[0], self.rect.center[1]+one),
			(self.rect.center[0], self.rect.center[1]+2*one)
		)
		moves3 = ((self.rect.center[0], self.rect.center[1]+one),)
		fight_moves1 = (
			(self.rect.center[0]+one, self.rect.center[1]-one),
			(self.rect.center[0]-one, self.rect.center[1]-one)
			)
		fight_moves2 = (
			(self.rect.center[0]+one, self.rect.center[1]+one),
			(self.rect.center[0]-one, self.rect.center[1]+one)
			)

		if self.figcol == 'W':
			if self.rect.top==(s_w - sq)/2+6*(sq/8):
				for n in moves:
					if n[0]<0 or n[1]<0 or n[0]>s_w or n[1]>s_h:
						pass
					elif n in white_sprites:
						pass
					elif n in black_sprites:
						pass
					else:
						red_plate(n[0], n[1])
						self.plate_posx.append(red_plate(n[0], n[1])[0])
						self.plate_posy.append(red_plate(n[0], n[1])[1])
				for n in fight_moves1:
					if n[0]<0 or n[1]<0 or n[0]>s_w or n[1]>s_h:
						pass
					elif n in white_sprites:
						pass
					elif n in black_sprites:
						green_plate(n[0], n[1])
						self.plate_posx.append(green_plate(n[0], n[1])[0])
						self.plate_posy.append(green_plate(n[0], n[1])[1])
						
						
			else:
				for n in moves1:
					if n[0]<0 or n[1]<0 or n[0]>s_w or n[1]>s_h:
						pass
					elif n in white_sprites:
						pass
					elif n in black_sprites:
						pass
					else:
						red_plate(n[0], n[1])
						self.plate_posx.append(red_plate(n[0], n[1])[0])
						self.plate_posy.append(red_plate(n[0], n[1])[1])
				for n in fight_moves1:
					if n[0]<0 or n[1]<0 or n[0]>s_w or n[1]>s_h:
						pass
					elif n in white_sprites:
						pass
					elif n in black_sprites:
						green_plate(n[0], n[1])
						self.plate_posx.append(green_plate(n[0], n[1])[0])
						self.plate_posy.append(green_plate(n[0], n[1])[1])
						
						
		else:
			if self.rect.top==(s_w - sq)/2+(sq/8):
				for n in moves2:
					if n[0]<0 or n[1]<0 or n[0]>s_w or n[1]>s_h:
						pass
					elif n in black_sprites:
						pass
					elif n in white_sprites:
						pass
					else:
						red_plate(n[0], n[1])
						self.plate_posx.append(red_plate(n[0], n[1])[0])
						self.plate_posy.append(red_plate(n[0], n[1])[1])
				for n in fight_moves2:
					if n[0]<0 or n[1]<0 or n[0]>s_w or n[1]>s_h:
						pass
					elif n in black_sprites:
						pass
					elif n in white_sprites:
						green_plate(n[0], n[1])
						self.plate_posx.append(green_plate(n[0], n[1])[0])
						self.plate_posy.append(green_plate(n[0], n[1])[1])
						
						
			else:
				for n in moves3:
					if n[0]<0 or n[1]<0 or n[0]>s_w or n[1]>s_h:
						pass
					elif n in black_sprites:
						pass
					elif n in white_sprites:
						pass
					else:
						red_plate(n[0], n[1])
						self.plate_posx.append(red_plate(n[0], n[1])[0])
						self.plate_posy.append(red_plate(n[0], n[1])[1])
				for n in fight_moves2:
					if n[0]<0 or n[1]<0 or n[0]>s_w or n[1]>s_h:
						pass
					elif n in black_sprites:
						pass
					elif n in white_sprites:
						green_plate(n[0], n[1])
						self.plate_posx.append(green_plate(n[0], n[1])[0])
						self.plate_posy.append(green_plate(n[0], n[1])[1])
						
						



	def update(self):
	
		if self in clicked_sprites:
			self.image = self.image2
			self.image.set_colorkey((255, 255, 255))
			self.red()
			for n in range(len(self.plate_posx)):
				w_cond = self.plate_posx[n]<=pygame.mouse.get_pos()[0]<=self.plate_posx[n]+75
				h_cond = self.plate_posy[n]<=pygame.mouse.get_pos()[1]<=self.plate_posy[n]+75
				if w_cond and h_cond:
					light_red(self.plate_posx[n], self.plate_posy[n])
					if pygame.mouse.get_pressed()[0]:
						if self.figcol == 'W':
							self.rect.centerx = self.plate_posx[n]+37
							self.rect.top = self.plate_posy[n]-4
							if self.rect.center in black_sprites:
								for j in black_figures:
									if self.rect.center == j.rect.center:
										if j.name == "King":
											win("W")
										j.kill()
							
						else:
							self.rect.centerx = self.plate_posx[n]+37
							self.rect.top = self.plate_posy[n]-4
							if self.rect.center in white_sprites:
								for j in white_figures:
									if self.rect.center == j.rect.center:
										if j.name == "King":
											win("B")
										j.kill()
							
						global start
						start += 1

								
		else:
			self.image = self.image1
			self.image.set_colorkey((255, 255, 255))





# класс Коня
class Knight(pygame.sprite.Sprite):
	def __init__(self, image1, image2, centx1, top1, figcol, name):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load(image1)
		self.image1 = self.image
		self.image.set_colorkey((255, 255, 255))
		self.image2 = pygame.image.load(image2)
		self.rect = self.image.get_rect()
		self.rect.centerx = centx1
		self.rect.top = top1
		self.figcol = figcol
		self.plate_posx = []
		self.plate_posy = []
		self.name = name


	def red(self):
		self.plate_posx = []
		self.plate_posy = []
		moves = (
			(self.rect.center[0]+one, self.rect.center[1]+2*one),
			(self.rect.center[0]+2*one, self.rect.center[1]+one),
			(self.rect.center[0]+2*one, self.rect.center[1]-one),
			(self.rect.center[0]+one, self.rect.center[1]-2*one),
			(self.rect.center[0]-one, self.rect.center[1]-2*one),
			(self.rect.center[0]-2*one, self.rect.center[1]-one),
			(self.rect.center[0]-2*one, self.rect.center[1]+one),
			(self.rect.center[0]-one, self.rect.center[1]+2*one)
		)

		if self.figcol == "W":
			for n in moves:
				if n[0]<0 or n[1]<0 or n[0]>s_w or n[1]>s_h:
					pass
				elif n in white_sprites:
					pass
				elif n in black_sprites:
					green_plate(n[0], n[1])
					self.plate_posx.append(green_plate(n[0], n[1])[0])
					self.plate_posy.append(green_plate(n[0], n[1])[1])
				else:
					red_plate(n[0], n[1])
					self.plate_posx.append(red_plate(n[0], n[1])[0])
					self.plate_posy.append(red_plate(n[0], n[1])[1])
		else:
			for n in moves:
				if n[0]<0 or n[1]<0 or n[0]>s_w or n[1]>s_h:
					pass
				elif n in black_sprites:
					pass
				elif n in white_sprites:
					green_plate(n[0], n[1])
					self.plate_posx.append(green_plate(n[0], n[1])[0])
					self.plate_posy.append(green_plate(n[0], n[1])[1])
				else:
					red_plate(n[0], n[1])
					self.plate_posx.append(red_plate(n[0], n[1])[0])
					self.plate_posy.append(red_plate(n[0], n[1])[1])



	def update(self):
	
		if self in clicked_sprites:
			self.image = self.image2
			self.image.set_colorkey((255, 255, 255))
			self.red()
			for n in range(len(self.plate_posx)):
				w_cond = self.plate_posx[n]<=pygame.mouse.get_pos()[0]<=self.plate_posx[n]+75
				h_cond = self.plate_posy[n]<=pygame.mouse.get_pos()[1]<=self.plate_posy[n]+75
				if w_cond and h_cond:
					light_red(self.plate_posx[n], self.plate_posy[n])
					if pygame.mouse.get_pressed()[0]:
						self.rect.centerx = self.plate_posx[n]+37
						self.rect.top = self.plate_posy[n]-4
						if self.figcol == "W":
							if self.rect.center in black_sprites:
								for j in black_figures:
									if self.rect.center == j.rect.center:
										if j.name == "King":
											win("W")
										j.kill()
						else:
							if self.rect.center in white_sprites:
								for j in white_figures:
									if self.rect.center == j.rect.center:
										if j.name == "King":
											win("B")
										j.kill()	
						global start
						start += 1		
		else:
			self.image = self.image1
			self.image.set_colorkey((255, 255, 255))




# класс Ладьи
# в этой программе нету такого движения, как РОКИРОВКА
class Rook(pygame.sprite.Sprite):
	def __init__(self, image1, image2, centx1, top1, figcol, name):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load(image1)
		self.image1 = self.image
		self.image.set_colorkey((255, 255, 255))
		self.image2 = pygame.image.load(image2)
		self.rect = self.image.get_rect()
		self.rect.centerx = centx1
		self.rect.top = top1
		self.figcol = figcol
		self.plate_posx = []
		self.plate_posy = []
		self.name = name


	def red(self):
		self.plate_posx = []
		self.plate_posy = []
		m = [self.rect.center[0], self.rect.center[1]]
		m1 = [self.rect.center[0], self.rect.center[1]]
		moves = []
		for n in range(1, 8):
			m[0] = self.rect.center[0]+n*one
			if m[0]>s_w:
				m[0] = self.rect.center[0]-one*(8-n)
			moves.append((m[0], m[1]))

		for n in range(1, 8):
			m[1] = self.rect.center[1]+n*one
			if m[1]>s_h:
				m[1] = self.rect.center[1]-one*(8-n)
			moves.append((m1[0], m[1]))

		if self.figcol == "W":
			for i in range(0, 4):
				for n in num_plates_rook(self, moves)[i]:
					if n[0]<0 or n[1]<0 or n[0]>s_w or n[1]>s_h:
						pass
					elif n in white_sprites:
						break
					elif n in black_sprites:
						green_plate(n[0], n[1])
						self.plate_posx.append(green_plate(n[0], n[1])[0])
						self.plate_posy.append(green_plate(n[0], n[1])[1])
						break
					else:
						red_plate(n[0], n[1])
						self.plate_posx.append(red_plate(n[0], n[1])[0])
						self.plate_posy.append(red_plate(n[0], n[1])[1])
		else:
			for i in range(0, 4):
				for n in num_plates_rook(self, moves)[i]:
					if n[0]<0 or n[1]<0 or n[0]>s_w or n[1]>s_h:
						pass
					elif n in black_sprites:
						break
					elif n in white_sprites:
						green_plate(n[0], n[1])
						self.plate_posx.append(green_plate(n[0], n[1])[0])
						self.plate_posy.append(green_plate(n[0], n[1])[1])
						break
					else:
						red_plate(n[0], n[1])
						self.plate_posx.append(red_plate(n[0], n[1])[0])
						self.plate_posy.append(red_plate(n[0], n[1])[1])


	def update(self):
	
		if self in clicked_sprites:
			self.image = self.image2
			self.image.set_colorkey((255, 255, 255))
			self.red()
			for n in range(len(self.plate_posx)):
				w_cond = self.plate_posx[n]<=pygame.mouse.get_pos()[0]<=self.plate_posx[n]+75
				h_cond = self.plate_posy[n]<=pygame.mouse.get_pos()[1]<=self.plate_posy[n]+75
				if w_cond and h_cond:
					light_red(self.plate_posx[n], self.plate_posy[n])
					if pygame.mouse.get_pressed()[0]:
						self.rect.centerx = self.plate_posx[n]+37
						self.rect.top = self.plate_posy[n]-4
						if self.figcol == "W":
							if self.rect.center in black_sprites:
								for j in black_figures:
									if self.rect.center == j.rect.center:
										if j.name == "King":
											win("W")
										j.kill()
						else:
							if self.rect.center in white_sprites:
								for j in white_figures:
									if self.rect.center == j.rect.center:
										if j.name == "King":
											win("B")
										j.kill()
						global start
						start += 1
			
		else:
			self.image = self.image1
			self.image.set_colorkey((255, 255, 255))




# класс Слона
class Bishop(pygame.sprite.Sprite):
	def __init__(self, image1, image2, centx1, top1, figcol, name):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load(image1)
		self.image1 = self.image
		self.image.set_colorkey((255, 255, 255))
		self.image2 = pygame.image.load(image2)
		self.rect = self.image.get_rect()
		self.rect.centerx = centx1
		self.rect.top = top1
		self.figcol = figcol
		self.plate_posx = []
		self.plate_posy = []
		self.name = name


	def red(self):
		self.plate_posx = []
		self.plate_posy = []
		m = [self.rect.center[0], self.rect.center[1]]
		m1 = [self.rect.center[0], self.rect.center[1]]
		#moves = []
		moves_right = []
		moves_left = []
		moves_up = []
		moves_down = []
		for n in range(1, 8):
			m[0] = self.rect.center[0]+n*one
			m[1] = self.rect.center[1]+n*one
			moves_right.append((m[0], m[1]))
			if m[0]<0 or m[1]<0 or m[0]>s_w or m[1]>s_h:
				m[0] = self.rect.center[0]-one*(8-n)
				m[1] = self.rect.center[1]-one*(8-n)
				moves_left.append((m[0], m[1]))

		for n in range(1, 8):
			m[0] = self.rect.center[0]+n*one
			m[1] = self.rect.center[1]-n*one
			moves_up.append((m[0], m[1]))
			if m[0]>s_w or m[1]>s_h:
				m[0] = self.rect.center[0]-one*(8-n)
				m[1] = self.rect.center[1]+one*(8-n)
				moves_down.append((m[0], m[1]))

		num_plates_bishop = moves_right, moves_left[::-1], moves_up, moves_down[::-1]

		if self.figcol == "W":
			for i in range(0, 4):
				for n in num_plates_bishop[i]:
					if n[0]<0 or n[1]<0 or n[0]>s_w or n[1]>s_h:
						pass
					elif n in white_sprites:
						break
					elif n in black_sprites:
						green_plate(n[0], n[1])
						self.plate_posx.append(green_plate(n[0], n[1])[0])
						self.plate_posy.append(green_plate(n[0], n[1])[1])
						break
					else:
						red_plate(n[0], n[1])
						self.plate_posx.append(red_plate(n[0], n[1])[0])
						self.plate_posy.append(red_plate(n[0], n[1])[1])
		else:
			for i in range(0, 4):
				for n in num_plates_bishop[i]:
					if n[0]<0 or n[1]<0 or n[0]>s_w or n[1]>s_h:
						pass
					elif n in black_sprites:
						break
					elif n in white_sprites:
						green_plate(n[0], n[1])
						self.plate_posx.append(green_plate(n[0], n[1])[0])
						self.plate_posy.append(green_plate(n[0], n[1])[1])
						break
					else:
						red_plate(n[0], n[1])
						self.plate_posx.append(red_plate(n[0], n[1])[0])
						self.plate_posy.append(red_plate(n[0], n[1])[1])



	def update(self):
		
		if self in clicked_sprites:
			self.image = self.image2
			self.image.set_colorkey((255, 255, 255))
			self.red()
			for n in range(len(self.plate_posx)):
				w_cond = self.plate_posx[n]<=pygame.mouse.get_pos()[0]<=self.plate_posx[n]+75
				h_cond = self.plate_posy[n]<=pygame.mouse.get_pos()[1]<=self.plate_posy[n]+75
				if w_cond and h_cond:
					light_red(self.plate_posx[n], self.plate_posy[n])
					if pygame.mouse.get_pressed()[0]:
						self.rect.centerx = self.plate_posx[n]+37
						self.rect.top = self.plate_posy[n]-4
						if self.figcol == "W":
							if self.rect.center in black_sprites:
								for j in black_figures:
									if self.rect.center == j.rect.center:
										if j.name == "King":
											win("W")
										j.kill()
						else:
							if self.rect.center in white_sprites:
								for j in white_figures:
									if self.rect.center == j.rect.center:
										if j.name == "King":
											win("B")
										j.kill()
						global start
						start += 1
			
		else:
			self.image = self.image1
			self.image.set_colorkey((255, 255, 255))





# класс Королевы
# по сути в этом классе совмещены Ладья и Слон
class Queen(pygame.sprite.Sprite):
	def __init__(self, image1, image2, centx1, top1, figcol, name):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load(image1)
		self.image1 = self.image
		self.image.set_colorkey((255, 255, 255))
		self.image2 = pygame.image.load(image2)
		self.rect = self.image.get_rect()
		self.rect.centerx = centx1
		self.rect.top = top1
		self.figcol = figcol
		self.plate_posx = []
		self.plate_posy = []
		self.name = name


	def red(self):
		self.plate_posx = []
		self.plate_posy = []
		m = [self.rect.center[0], self.rect.center[1]]
		m1 = [self.rect.center[0], self.rect.center[1]]
		
		moves_right = []
		moves_left = []
		moves_up = []
		moves_down = []

		moves = []
		for n in range(1, 8):
			m[0] = self.rect.center[0]+n*one
			m[1] = self.rect.center[1]+n*one
			moves_right.append((m[0], m[1]))
			if m[0]<0 or m[1]<0 or m[0]>s_w or m[1]>s_h:
				m[0] = self.rect.center[0]-one*(8-n)
				m[1] = self.rect.center[1]-one*(8-n)
				moves_left.append((m[0], m[1]))

		for n in range(1, 8):
			m[0] = self.rect.center[0]+n*one
			m[1] = self.rect.center[1]-n*one
			moves_up.append((m[0], m[1]))
			if m[0]>s_w or m[1]>s_h:
				m[0] = self.rect.center[0]-one*(8-n)
				m[1] = self.rect.center[1]+one*(8-n)
				moves_down.append((m[0], m[1]))

		num_plates_bishop = moves_right, moves_left[::-1], moves_up, moves_down[::-1]

		for n in range(1, 8):
			m[0] = self.rect.center[0]+n*one
			if m[0]>s_w:
				m[0] = self.rect.center[0]-one*(8-n)
			moves.append((m[0], m1[1]))

		for n in range(1, 8):
			m[1] = self.rect.center[1]+n*one
			if m[1]>s_h:
				m[1] = self.rect.center[1]-one*(8-n)
			moves.append((m1[0], m[1]))

		if self.figcol == "W":
			for i in range(0, 4):
				for n in num_plates_rook(self, moves)[i]:
					if n[0]<0 or n[1]<0 or n[0]>s_w or n[1]>s_h:
						pass
					elif n in white_sprites:
						break
					elif n in black_sprites:
						green_plate(n[0], n[1])
						self.plate_posx.append(green_plate(n[0], n[1])[0])
						self.plate_posy.append(green_plate(n[0], n[1])[1])
						break
					else:
						red_plate(n[0], n[1])
						self.plate_posx.append(red_plate(n[0], n[1])[0])
						self.plate_posy.append(red_plate(n[0], n[1])[1])
				for n in num_plates_bishop[i]:
					if n[0]<0 or n[1]<0 or n[0]>s_w or n[1]>s_h:
						pass
					elif n in white_sprites:
						break
					elif n in black_sprites:
						green_plate(n[0], n[1])
						self.plate_posx.append(green_plate(n[0], n[1])[0])
						self.plate_posy.append(green_plate(n[0], n[1])[1])
						break
					else:
						red_plate(n[0], n[1])
						self.plate_posx.append(red_plate(n[0], n[1])[0])
						self.plate_posy.append(red_plate(n[0], n[1])[1])
		else:
			for i in range(0, 4):
				for n in num_plates_rook(self, moves)[i]:
					if n[0]<0 or n[1]<0 or n[0]>s_w or n[1]>s_h:
						pass
					elif n in black_sprites:
						break
					elif n in white_sprites:
						green_plate(n[0], n[1])
						self.plate_posx.append(green_plate(n[0], n[1])[0])
						self.plate_posy.append(green_plate(n[0], n[1])[1])
						break
					else:
						red_plate(n[0], n[1])
						self.plate_posx.append(red_plate(n[0], n[1])[0])
						self.plate_posy.append(red_plate(n[0], n[1])[1])
				for n in num_plates_bishop[i]:
					if n[0]<0 or n[1]<0 or n[0]>s_w or n[1]>s_h:
						pass
					elif n in black_sprites:
						break
					elif n in white_sprites:
						green_plate(n[0], n[1])
						self.plate_posx.append(green_plate(n[0], n[1])[0])
						self.plate_posy.append(green_plate(n[0], n[1])[1])
						break
					else:
						red_plate(n[0], n[1])
						self.plate_posx.append(red_plate(n[0], n[1])[0])
						self.plate_posy.append(red_plate(n[0], n[1])[1])


	def update(self):
		
		if self in clicked_sprites:
			self.image = self.image2
			self.image.set_colorkey((255, 255, 255))
			self.red()
			for n in range(len(self.plate_posx)):
				w_cond = self.plate_posx[n]<=pygame.mouse.get_pos()[0]<=self.plate_posx[n]+75
				h_cond = self.plate_posy[n]<=pygame.mouse.get_pos()[1]<=self.plate_posy[n]+75
				if w_cond and h_cond:
					light_red(self.plate_posx[n], self.plate_posy[n])
					if pygame.mouse.get_pressed()[0]:
						self.rect.centerx = self.plate_posx[n]+37
						self.rect.top = self.plate_posy[n]-4
						if self.figcol == "W":
							if self.rect.center in black_sprites:
								for j in black_figures:
									if self.rect.center == j.rect.center:
										if j.name == "King":
											win("W")
										j.kill()
						else:
							if self.rect.center in white_sprites:
								for j in white_figures:
									if self.rect.center == j.rect.center:
										if j.name == "King":
											win("B")
										j.kill()
						global start
						start += 1
			
		else:
			self.image = self.image1
			self.image.set_colorkey((255, 255, 255))





#Функция создает игровое поле
def GameField():
	#Цвет фона/окна
	screen.fill((102, 51, 0))

	#Создание игрового поля
	surf = pygame.Surface((664, 664))
	surf.fill((255, 255, 255))
	rect = surf.get_rect()
	
	#Разные перменные
	win_def = (s_w - surf.get_width())/2

	s_center = (
		(s_w - surf.get_width()) / 2,
		(s_h - surf.get_height()) / 2
	)

	one_plate_h = surf.get_height() / 8

	s_one = (one_plate_h, one_plate_h)

	surf_one = pygame.Surface(s_one)
	
	screen.blit(surf, s_center)
	
	w1 = win_def
	h1 = win_def

	#Цикл создания черных плиток
	for i in range(1, 80):
		if i%2==0:
			if i==2:
				w1 += one_plate_h
			else:
				w1 += one_plate_h*2
			
			if i%10==0:
				if (i/10)%2==0:
					w1 = win_def + one_plate_h
				else:
					w1 = win_def
				h1 += one_plate_h

			if w1<s_w-one_plate_h-win_def+1:
				surf_one.fill((255, 178, 102))
				screen.blit(surf_one, (w1, h1))


# создание фигур на поле
# 
# из-за плохого качества кода, создание фигур на поле реализовано кучей одинаковых строчек
# думаю, это можно как-то сделать более красиво, хотя бы пешки
# но уникальность каждой фигуры не позволяет абсолютно все засунуть в один цикл на 32 итерации
# 
# как вы можете заметить, для изображения фигур я использую пнг файлы, которые находятся в той же папке, что и файл программы
# рекомендую использовать пнг файл с размером чуть меньше чем одна клетка (у меня: клетка=83х83, фигурка=80х80)
# путь указывайте или относительный или абсолютный, как удобно
def figures():
	wKing = King("wK.png", "wK2.png", (s_w - sq)/2 + (sq/8)*4 + sq/16, (s_w - sq)/2+7*(sq/8), "W", "King")
	white_figures.add(wKing)
	bKing = King("bK.png", "bK2.png", (s_w - sq)/2 + (sq/8)*4 + sq/16, (s_w - sq)/2, "B", "King")
	black_figures.add(bKing)


	wQueen = Queen("wQ.png", "wQ2.png", (s_w - sq)/2 + (sq/8)*3 + sq/16, (s_w - sq)/2+7*(sq/8), "W", "Queen")
	white_figures.add(wQueen)
	bQueen = Queen("bQ.png", "bQ2.png", (s_w - sq)/2 + (sq/8)*3 + sq/16, (s_w - sq)/2, "B", "Queen")
	black_figures.add(bQueen)


	wKnight1 = Knight("wN.png", "wN2.png", (s_w - sq)/2 + (sq/8)*1 + sq/16, (s_w - sq)/2+7*(sq/8), "W", "Knight")
	white_figures.add(wKnight1)
	wKnight2 = Knight("wN.png", "wN2.png", (s_w - sq)/2 + (sq/8)*6 + sq/16, (s_w - sq)/2+7*(sq/8), "W", "Knight")
	white_figures.add(wKnight2)
	bKnight1 = Knight("bN.png", "bN2.png", (s_w - sq)/2 + (sq/8)*1 + sq/16, (s_w - sq)/2, "B", "Knight")
	black_figures.add(bKnight1)
	bKnight2 = Knight("bN.png", "bN2.png", (s_w - sq)/2 + (sq/8)*6 + sq/16, (s_w - sq)/2, "B", "Knight")
	black_figures.add(bKnight2)


	wBishop1 = Bishop("wB.png", "wB2.png", (s_w - sq)/2 + (sq/8)*2 + sq/16, (s_w - sq)/2+7*(sq/8), "W", "Bishop")
	white_figures.add(wBishop1)
	wBishop2 = Bishop("wB.png", "wB2.png", (s_w - sq)/2 + (sq/8)*5 + sq/16, (s_w - sq)/2+7*(sq/8), "W", "Bishop")
	white_figures.add(wBishop2)
	bBishop1 = Bishop("bB.png", "bB2.png", (s_w - sq)/2 + (sq/8)*2 + sq/16, (s_w - sq)/2, "B", "Bishop")
	black_figures.add(bBishop1)
	bBishop2 = Bishop("bB.png", "bB2.png", (s_w - sq)/2 + (sq/8)*5 + sq/16, (s_w - sq)/2, "B", "Bishop")
	black_figures.add(bBishop2)


	wRook1 = Rook("wR.png", "wR2.png", (s_w - sq)/2 + (sq/8)*0 + sq/16, (s_w - sq)/2+7*(sq/8), "W", "Rook")
	white_figures.add(wRook1)
	wRook2 = Rook("wR.png", "wR2.png", (s_w - sq)/2 + (sq/8)*7 + sq/16, (s_w - sq)/2+7*(sq/8), "W", "Rook")
	white_figures.add(wRook2)
	bRook1 = Rook("bR.png", "bR2.png", (s_w - sq)/2 + (sq/8)*0 + sq/16, (s_w - sq)/2, "B", "Rook")
	black_figures.add(bRook1)
	bRook2 = Rook("bR.png", "bR2.png", (s_w - sq)/2 + (sq/8)*7 + sq/16, (s_w - sq)/2, "B", "Rook")
	black_figures.add(bRook2)


	wPawn1 = Pawn("wP.png", "wP2.png", (s_w - sq)/2 + (sq/8)*0 + sq/16, (s_w - sq)/2+6*(sq/8), "W", "Pawn")
	white_figures.add(wPawn1)
	wPawn2 = Pawn("wP.png", "wP2.png", (s_w - sq)/2 + (sq/8)*1 + sq/16, (s_w - sq)/2+6*(sq/8), "W", "Pawn")
	white_figures.add(wPawn2)
	wPawn3 = Pawn("wP.png", "wP2.png", (s_w - sq)/2 + (sq/8)*2 + sq/16, (s_w - sq)/2+6*(sq/8), "W", "Pawn")
	white_figures.add(wPawn3)
	wPawn4 = Pawn("wP.png", "wP2.png", (s_w - sq)/2 + (sq/8)*3 + sq/16, (s_w - sq)/2+6*(sq/8), "W", "Pawn")
	white_figures.add(wPawn4)
	wPawn5 = Pawn("wP.png", "wP2.png", (s_w - sq)/2 + (sq/8)*4 + sq/16, (s_w - sq)/2+6*(sq/8), "W", "Pawn")
	white_figures.add(wPawn5)
	wPawn6 = Pawn("wP.png", "wP2.png", (s_w - sq)/2 + (sq/8)*5 + sq/16, (s_w - sq)/2+6*(sq/8), "W", "Pawn")
	white_figures.add(wPawn6)
	wPawn7 = Pawn("wP.png", "wP2.png", (s_w - sq)/2 + (sq/8)*6 + sq/16, (s_w - sq)/2+6*(sq/8), "W", "Pawn")
	white_figures.add(wPawn7)
	wPawn8 = Pawn("wP.png", "wP2.png", (s_w - sq)/2 + (sq/8)*7 + sq/16, (s_w - sq)/2+6*(sq/8), "W", "Pawn")
	white_figures.add(wPawn8)


	bPawn1 = Pawn("bP.png", "bP2.png", (s_w - sq)/2 + (sq/8)*0 + sq/16, (s_w - sq)/2+1*(sq/8), "B", "Pawn")
	black_figures.add(bPawn1)
	bPawn2 = Pawn("bP.png", "bP2.png", (s_w - sq)/2 + (sq/8)*1 + sq/16, (s_w - sq)/2+1*(sq/8), "B", "Pawn")
	black_figures.add(bPawn2)
	bPawn3 = Pawn("bP.png", "bP2.png", (s_w - sq)/2 + (sq/8)*2 + sq/16, (s_w - sq)/2+1*(sq/8), "B", "Pawn")
	black_figures.add(bPawn3)
	bPawn4 = Pawn("bP.png", "bP2.png", (s_w - sq)/2 + (sq/8)*3 + sq/16, (s_w - sq)/2+1*(sq/8), "B", "Pawn")
	black_figures.add(bPawn4)
	bPawn5 = Pawn("bP.png", "bP2.png", (s_w - sq)/2 + (sq/8)*4 + sq/16, (s_w - sq)/2+1*(sq/8), "B", "Pawn")
	black_figures.add(bPawn5)
	bPawn6 = Pawn("bP.png", "bP2.png", (s_w - sq)/2 + (sq/8)*5 + sq/16, (s_w - sq)/2+1*(sq/8), "B", "Pawn")
	black_figures.add(bPawn6)
	bPawn7 = Pawn("bP.png", "bP2.png", (s_w - sq)/2 + (sq/8)*6 + sq/16, (s_w - sq)/2+1*(sq/8), "B", "Pawn")
	black_figures.add(bPawn7)
	bPawn8 = Pawn("bP.png", "bP2.png", (s_w - sq)/2 + (sq/8)*7 + sq/16, (s_w - sq)/2+1*(sq/8), "B", "Pawn")
	black_figures.add(bPawn8)




# создание всяких игровых вещей закончено, теперь нужно сделать организационные моменты




# название окна, введение времени
# создание двух групп спрайтов
pygame.display.set_caption("Chess")
clock = pygame.time.Clock()
white_figures = pygame.sprite.Group()
black_figures = pygame.sprite.Group()

# вот теперь можно создать фигуры на поле
figures()

# координаты каждой фигуры на поле
white_sprites = [(n.rect.centerx, n.rect.top+40) for n in[s for s in white_figures]]
black_sprites = [(n.rect.centerx, n.rect.top+40) for n in[s for s in black_figures]]

# контейнер для кликнутых спрайтов
# в этой программе в это контейнере может быть только один спрайт или не быть совсем
clicked_sprites = [0]

# переменная для создания порядка подов (белый начинает)
start = 1


#Главный цикл
running = True
while running:
	# фпс в программе, можно изменить в начале
	clock.tick(FPS)
	
	#Цикл красного крестика
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False


		# обработка события нажатия на фигуру(спрайт) и условие поочередной игры

		# из-за особеностей pygame или моих кривых ручек:) на данный момент в этой программе существует
		# один основной баг. pygame может фиксировать только момент нажатия на лкм или момент отжатия,
		# то есть зафиксировать обычный клик в человеческом понимании (нажал и отжал) с помощью
		# внутренных инструментов невозможно
		# этот баг появляется каждый раз после того, как вы кликаете на спрайт и выбираете поле для хода,
		# в этот момент вы можете нажать на это поле, но потом не отжать лкм и пересунуть ее на другое поле,
		# после чего она сразу же туда пересунется, и так до сметри короля или тупика этой фигуры

		if event.type == pygame.MOUSEBUTTONUP:
			pos = pygame.mouse.get_pos()
			if start%2==1:
				clicked_sprites = [s for s in white_figures if s.rect.collidepoint(pos)]
			else:
				clicked_sprites = [s for s in black_figures if s.rect.collidepoint(pos)]
			#print(clicked_sprites, 1, start)
			
			# обновление списка координат каждой фигуры
			white_sprites = [(n.rect.centerx, n.rect.top+40) for n in[s for s in white_figures]]
			black_sprites = [(n.rect.centerx, n.rect.top+40) for n in[s for s in black_figures]]



	

	
	# условие обычного поля,
	# если его нарушить(убить одного из королей), то будет выведена соответствующая надпись и игра будет окончена
	if won == 0:
		GameField()
	else:
		black_figures.empty()
		white_figures.empty()
		surf = pygame.Surface((s_w, s_h))
		surf.set_alpha(5)
		surf.fill((255, 178, 102))
		screen.blit(surf, (0, 0))
		font = pygame.font.Font('freesansbold.ttf', 50)
		if won == 1:
			text = font.render('White won', True, (0, 0, 0))
		elif won == 2:
			text = font.render('Black won', True, (0, 0, 0))
		screen.blit(text, (s_w/2-125, s_h/2))

		
	# обновление и отрисовка всех фигур на полу
	white_figures.update()
	black_figures.update()
	white_figures.draw(screen)
	black_figures.draw(screen)
	pygame.display.flip()
	

	
	

#Выход
pygame.quit()