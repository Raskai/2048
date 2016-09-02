from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException
import random
import math

driver = webdriver.Chrome()
driver.get("https://gabrielecirulli.github.io/2048/")


gamestate = 0 

def setNewTile(n):
	
	if element:
		return element
	else:
		return False

def getNew(n):
	WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "tile-new")))   # Najde n+1-tý objekt s class "tile-new"
	newTile = driver.find_elements_by_class_name("tile-new")[n]
	newTilePositionX = int(newTile.get_attribute("class").split()[2][-3])     # Najde 3 znak od konce v 2 classu nových tiles, což je jejich x souřadnice
	newTilePositionY = int(newTile.get_attribute("class").split()[2][-1])     #Podobně i y souřadnici
	try:
		newTileValue = int(newTile.get_attribute("class").split()[1][-1])     #Stejnou metodou najde hodnotu nového tile
	except selenium.common.exceptions.StaleElementReferenceException:          #Fce občas náhodně hází chybu
		getNew(n)
		return
	newSpawn = int(math.log2(newTileValue)) << ((((4-newTilePositionY)*4)+(4-newTilePositionX))*4)
	'''Aktualizuje herní plochu v paměti. Herní plocha je vyjádřena 64-bitovým číslem, každé políčko má 16x vyšší hodnotu než
	předchozí. Mocniny dvojek ve novém políčku jsou vynásobeny příslušnou hodnotou 16 a přidány do gamestate.'''
	return newSpawn

            # Definice globálních variables
for i in range (0,2):
	gamestate |= getNew(i)
new = 0
listRight = []
listRightScores = []
listLeft = []
listLeftScores = []
score = 0
try_board = 0
iterations = 1000
spawnRate = [1,1,1,1,1,1,1,1,1,2]
lastBest = 5
stuck = 0
rand_board = 0

def read_lists():
	global listRight
	global listLeft
	global listRightScores
	global listLeftScores
	f = open('right.txt', 'r')
	for line in f:
		for word in line.split():
			listRight.append(int(word))
	f.close()
	f = open('left.txt', 'r')
	for line in f:
		for word in line.split():
			listLeft.append(int(word))
	f.close()
	f = open('rightScores.txt', 'r')
	for line in f:
		for word in line.split():
			listRightScores.append(int(word))
	f.close()
	f = open('leftScores.txt', 'r')
	for line in f:
		for word in line.split():
			listLeftScores.append(int(word))
	f.close()

read_lists()

def right(board,bool):																			# Definice funkcí na ovládání
	if bool == True:
		ActionChains(driver).send_keys(Keys.ARROW_RIGHT).perform()
	points = 0
	line1 = board & 0xFFFF
	line2 = (board & 0xFFFF0000) >> 16
	line3 = (board & 0xFFFF00000000) >> 32
	line4 = (board & 0xFFFF000000000000) >> 48
	points = listRightScores[line1] + listRightScores[line2] + listRightScores[line3] + listRightScores[line4]
	line1 = listRight[line1]
	line2 = listRight[line2]
	line3 = listRight[line3]
	line4 = listRight[line4]
	board = line1 | (line2 << 16) | (line3 << 32) | (line4 << 48)
	return (board, points)

def left(board,bool):
	if bool == True:
		ActionChains(driver).send_keys(Keys.ARROW_LEFT).perform()
	points = 0
	line1 = board & 0xFFFF
	line2 = (board & 0xFFFF0000) >> 16
	line3 = (board & 0xFFFF00000000) >> 32
	line4 = (board & 0xFFFF000000000000) >> 48
	points = listLeftScores[line1] + listLeftScores[line2] + listLeftScores[line3] + listLeftScores[line4]
	line1 = listLeft[line1]
	line2 = listLeft[line2]
	line3 = listLeft[line3]
	line4 = listLeft[line4]
	board = line1 | (line2 << 16) | (line3 << 32) | (line4 << 48)
	return (board, points)

def up(board,bool):       #Vyměnit
	if bool == True:
		ActionChains(driver).send_keys(Keys.ARROW_UP).perform()
	points = 0
	a1 = board & 0xF0F00F0FF0F00F0F
	a2 = board & 0x0000F0F00000F0F0
	a3 = board & 0x0F0F00000F0F0000
	a = a1 | (a2 << 12) | (a3 >> 12)
	b1 = a & 0xFF00FF0000FF00FF
	b2 = a & 0x00FF00FF00000000
	b3 = a & 0x00000000FF00FF00
	board_t = b1 | (b2 >> 24) | (b3 << 24)
	line1 = board_t & 0xFFFF
	line2 = (board_t & 0xFFFF0000) >> 16
	line3 = (board_t & 0xFFFF00000000) >> 32
	line4 = (board_t & 0xFFFF000000000000) >> 48 
	points = listLeftScores[line1] + listLeftScores[line2] + listLeftScores[line3] + listLeftScores[line4]
	line1 = listLeft[line1]
	line2 = listLeft[line2]
	line3 = listLeft[line3]
	line4 = listLeft[line4]
	board_t = line1 | (line2 << 16) | (line3 << 32) | (line4 << 48)
	b1 = board_t & 0xFF00FF0000FF00FF
	b2 = board_t & 0x00FF00FF00000000
	b3 = board_t & 0x00000000FF00FF00
	board_t = b1 | (b2 >> 24) | (b3 << 24)
	a1 = board_t & 0xF0F00F0FF0F00F0F
	a2 = board_t & 0x0000F0F00000F0F0
	a3 = board_t & 0x0F0F00000F0F0000
	board = a1 | (a2 << 12) | (a3 >> 12)
	return (board, points)

def down(board,bool):
	if bool == True:
		ActionChains(driver).send_keys(Keys.ARROW_DOWN).perform()
	points = 0
	a1 = board & 0xF0F00F0FF0F00F0F
	a2 = board & 0x0000F0F00000F0F0
	a3 = board & 0x0F0F00000F0F0000
	a = a1 | (a2 << 12) | (a3 >> 12)
	b1 = a & 0xFF00FF0000FF00FF
	b2 = a & 0x00FF00FF00000000
	b3 = a & 0x00000000FF00FF00
	board_t = b1 | (b2 >> 24) | (b3 << 24)
	line1 = board_t & 0xFFFF
	line2 = (board_t & 0xFFFF0000) >> 16
	line3 = (board_t & 0xFFFF00000000) >> 32
	line4 = (board_t & 0xFFFF000000000000) >> 48
	points = listRightScores[line1] + listRightScores[line2] + listRightScores[line3] + listRightScores[line4]
	line1 = listRight[line1]
	line2 = listRight[line2]
	line3 = listRight[line3]
	line4 = listRight[line4]
	board_t = line1 | (line2 << 16) | (line3 << 32) | (line4 << 48)
	b1 = board_t & 0xFF00FF0000FF00FF
	b2 = board_t & 0x00FF00FF00000000
	b3 = board_t & 0x00000000FF00FF00
	board_t = b1 | (b2 >> 24) | (b3 << 24)
	a1 = board_t & 0xF0F00F0FF0F00F0F
	a2 = board_t & 0x0000F0F00000F0F0
	a3 = board_t & 0x0F0F00000F0F0000
	board = a1 | (a2 << 12) | (a3 >> 12)
	return (board, points)

moveList = [right, up, left, down]

'''moveOptions = {0 : ActionChains(driver).send_keys(Keys.ARROW_RIGHT).perform(),
           1 : ActionChains(driver).send_keys(Keys.ARROW_UP).perform(),
           2 : ActionChains(driver).send_keys(Keys.ARROW_LEFT).perform(),
           3 : ActionChains(driver).send_keys(Keys.ARROW_DOWN).perform(),
           }'''
def findBest():
	global rand_board
	rand_board = 0
	result = 0
	backup = 0
	score_avg = []
	for x in range (0,4):
		hue = moveList[x](gamestate,False)                         #Pro každý směr
		print(rand_board)
		score_array = []
		for n in range(0,iterations):
			rand_board = hue[0]
			score = hue[1]
			dead = 0
			while dead < 10:
				zeros = []
				backup = rand_board
				result = random.choice(moveList)(rand_board,False)
				rand_board = result[0]
				score += result[1]
				if backup != rand_board:
					dead = 0
					for m in range(0,16):
						if ((rand_board >> (m * 4)) & 0xF) == 0:
							zeros.append(m)
					if len(zeros) != 0:
						rand_board |= (random.choice(spawnRate) << ((random.choice(zeros)) * 4))						
				else:
					dead += 1
			score_array.append(score)
		score_avg.append(sum(score_array) / iterations)
	max_value = max(score_avg)
	return(score_avg.index(max(score_avg)))

def runGame():
	global best
	global move
	global gamestate
	global score
	while len(driver.find_elements_by_class_name("game-message")[0].get_attribute("class").split()) != 2:   # Když má zvolený element 2 classy, hra skončila
		best = findBest()
		move = moveList[best](gamestate,True)
		gamestate = move[0]
		score = move[1]
		WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "tile-new")));      #Čeká na přítomnost nového tile
		gamestate |= getNew(0)																	   #Najde pozici a hodnotu nového tile, přidá ho do herní plochy																					   #Najde pozici a hodnotu nového tile, přidá ho do herní plochy
		if best == lastBest:
			stuck +=1
		else:
			stuck = 0
		if stuck > 10:
			random.choice(moveList)(rand_board,True)
		lastBest = best

rungame()

button = driver.find_elements_by_class_name("keep-playing-button")
button.click()

rungame()


	


