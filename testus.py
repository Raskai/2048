listRight = []
def read_words():
	global listRight
	f = open('right.txt', 'r')
	for line in f:
		for word in line.split():
			listRight.append(int(word))
	f.close()
read_words()
gamestate = [0,3,4,5]
line1 = listRight[gamestate[3]+16*gamestate[2]+(16**2)*gamestate[1]+(16**3)*gamestate[0]]
print(line1%16)
print((line1%256-line1%16)/16)
print((line1%4096)/256-(line1%256)/16-line1%16)
print((line1%65536)/4096-(line1%4096)/256-(line1%256)/16-line1%16)
