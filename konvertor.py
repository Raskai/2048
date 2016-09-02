array = [176808350587232577]
for x in array:
	for n in range(48,-1,-16):
		print((x & (0xF000 << n)) >> (n+12), " | ", (x & (0xF00 << n)) >> (n+8), " | ", (x & (0xF0 << n)) >> (n+4), " | ", (x & (0xF << n)) >> n )
	print(" ")