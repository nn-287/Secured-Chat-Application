# Binary to decimal conversion
def bin2dec(binary):

	decimal, i = 0, 0
	while(binary != 0):
		dec = binary % 10
		decimal = decimal + dec * pow(2, i)
		binary = binary//10
		i += 1
	return decimal


s = '0101011'
print(bin2dec(s))