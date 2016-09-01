from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException
from random import randint
import math

driver = webdriver.Chrome();
driver.get("https://gabrielecirulli.github.io/2048/");

def read_words(words_file):
    return [word for line in open(words_file, 'r') for word in line.split()]
listRight = read_words('right.txt')

def setNewTile(n):
	
	if element:
		return element;
	else:
		return False;

def getNew(n):
	global gamestate;
	WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "tile-new")));   # Najde n+1-tý objekt s class "tile-new"
	newTile = driver.find_elements_by_class_name("tile-new")[n];
	newTilePositionX = int(newTile.get_attribute("class").split()[2][-3]);     # Najde 3 znak od konce v 2 classu nových tiles, což je jejich x souřadnice
	newTilePositionY = int(newTile.get_attribute("class").split()[2][-1]);     #Podobně i y souřadnici
	try:
		newTileValue = int(newTile.get_attribute("class").split()[1][-1]);     #Stejnou metodou najde hodnotu nového tile
	except selenium.common.exceptions.StaleElementReferenceException:          #Fce občas náhodně hází chybu
		getNew(n);
		return;
	print (newTilePositionY);
	print (newTilePositionX);
	print(newTileValue);
	gamestate[x+(y-1)*4] = log2(newTileValue)
	'''Aktualizuje herní plochu v paměti. Herní plocha je vyjádřena 64-bitovým číslem, každé políčko má 16x vyšší hodnotu než
	předchozí. Mocniny dvojek ve novém políčku jsou vynásobeny příslušnou hodnotou 16 a přidány do gamestate.'''
	print(gamestate);
	return;

gamestate = [0] * 16;              # Definice globálních variables
for i in range (0,2):
	getNew(i);

new = 0;

def right():																			# Definice funkcí na ovládání
		ActionChains(driver).send_keys(Keys.ARROW_RIGHT).perform();
		global gamestate;
		line1 = gamestate[0:4]
		line2 = gamestate[4:8]
		line3 = gamestate[8:12]
		line4 = gamestate[12:16]
		line1 = listRight[gamestate[0]+16*gamestate[1]+(16**2)*gamestate[2]+(16**3)*gamestate[3])
			

def up():
		ActionChains(driver).send_keys(Keys.ARROW_UP).perform();
def left():
		ActionChains(driver).send_keys(Keys.ARROW_LEFT).perform();
def down():
		ActionChains(driver).send_keys(Keys.ARROW_DOWN).perform();
options = {0 : right,
           1 : up,
           2 : left,
           3 : down,
           }

while len(driver.find_elements_by_class_name("game-message")[0].get_attribute("class").split()) != 2:  # Když má zvolený element 2 classy, hra skončila
	options[randint(0,3)]();
	WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "tile-new")));      #Čeká na přítomnost nového tile
	getNew(0);																						   #Najde pozici a hodnotu nového tile, přidá ho do herní plochy

	


