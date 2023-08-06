from random import randrange

letters = {

"a" : [["      AA      "],
       ["     A  A     "],
       ["    AAAAAA    "],
       ["   A      A   "],
       ["  A        A  "]],

"b" : [["  BBBBB   "],
       ["  B    B  "],
       ["  BBBBB   "],
       ["  B    B  "],
       ["  BBBBB   "]],

"c" : [["  CCCCC  "],
       ["  C      "],
       ["  C      "],
       ["  C      "],
       ["  CCCCC  "]],

"d" : [["  DDDDD    "],
       ["  D    D   "],
       ["  D     D  "],
       ["  D    D   "],
       ["  DDDDD    "]],

"e" : [["  EEEEE  "],
       ["  E      "],
       ["  EEEEE  "],
       ["  E      "],
       ["  EEEEE  "]],

"f" : [["  FFFFF  "],
       ["  F      "],
       ["  FFFFF  "],
       ["  F      "],
       ["  F     "]],

"g" : [["  GGGGG  "],
       ["  G      "],
       ["  G  GG  "],
       ["  G   G  "],
       ["  GGGGG  "]],

"h" : [["  H   H  "],
       ["  H   H  "],
       ["  HHHHH  "],
       ["  H   H  "],
       ["  H   H  "]],

 "i" : [["  I  "],
        ["  I  "],
        ["  I  "],
        ["  I  "],
        ["  I  "]],

"j" : [["    J  "],
       ["    J  "],
       ["    J  "],
       ["  J J  "],
       ["  JJJ  "]],

"k" : [["  K  K  "],
       ["  K K   "],
       ["  KK    "],
       ["  K K   "],
       ["  K  K  "]],

"l" : [["  L      "],
       ["  L      "],
       ["  L      "],
       ["  L      "],
       ["  LLLLL  "]],

"m" : [["  M          M  "],
       ["  M M      M M  "],
       ["  M  M    M  M  "],
       ["  M   M  M   M  "],
       ["  M    MM    M  "]],

"n" : [["  NN    N  "],
       ["  N N   N  "],
       ["  N  N  N  "],
       ["  N   N N  "],
       ["  N    NN  "]],

"o" : [["  OOOOO  "],
       ["  O   O  "],
       ["  O   O  "],
       ["  O   O  "],
       ["  OOOOO  "]],

"p" : [["  PPPPP  "],
       ["  P   P  "],
       ["  PPPPP  "],
       ["  P      "],
       ["  P      "]],

"q" : [["  QQQQQ    "],
       ["  Q   Q    "],
       ["  Q   Q    "],
       ["  Q  QQ    "],
       ["  QQQQQ Q  "]],

"r" : [["  RRRRR  "],
       ["  R   R  "],
       ["  RRRRR  "],
       ["  R  R   "],
       ["  R   R  "]],

"s" : [["  SSSSS  "],
       ["  S      "],
       ["  SSSSS  "],
       ["      S  "],
       ["  SSSSS  "]],

"t" : [["  TTTTT  "],
       ["    T    "],
       ["    T    "],
       ["    T    "],
       ["    T    "]],

"u" : [["  U   U  "],
       ["  U   U  "],
       ["  U   U  "],
       ["  U   U  "],
       ["  UUUUU  "]],

"v" : [["  V       V  "],
       ["   V     V   "],
       ["    V   V    "],
       ["     V V     "],
       ["      V      "]],

"w" : [["  W        WW        W  "],
       ["   W      W  W      W   "],
       ["    W    W    W    W    "],
       ["     W  W      W  W     "],
       ["      WW        WW      "]],

"x" : [["  X   X  "],
       ["   X X   "],
       ["    X    "],
       ["   X X   "],
       ["  X   X  "]],

"y" : [["  Y   Y  "],
       ["   Y Y   "],
       ["    Y    "],
       ["    Y    "],
       ["    Y    "]],

"z" : [["  ZZZZZ  "],
       ["     Z   "],
       ["   ZZZ    "],
       ["   Z     "],
       ["  ZZZZZ  "]],

"0" : [["  00000  "],
       ["  0   0  "],
       ["  0   0  "],
       ["  0   0  "],
       ["  00000  "]],

"1" : [["    1    "],
       ["  1 1    "],
       ["    1    "],
       ["    1    "],
       ["  11111  "]],

"2" : [["  22222  "],
       ["     2   "],
       ["    2    "],
       ["   2     "],
       ["  22222  "]],

"3" : [["  33333  "],
       ["      3  "],
       ["  33333  "],
       ["      3  "],
       ["  33333  "]],

"4" : [["     4   "],
       ["    44   "],
       ["   4 4   "],
       ["  44444  "],
       ["     4   "]],

"5" : [["  55555  "],
       ["  5      "],
       ["  55555  "],
       ["      5  "],
       ["  55555  "]],

"6" : [["  66666  "],
       ["  6      "],
       ["  66666  "],
       ["  6   6  "],
       ["  66666  "]],

"7" : [["  77777  "],
       ["     7   "],
       ["    7    "],
       ["   7     "],
       ["  7      "]],

"8" : [["  88888  "],
       ["  8   8  "],
       ["  88888  "],
       ["  8   8  "],
       ["  88888  "]],

"9" : [["  99999  "],
       ["  9   9  "],
       ["  99999  "],
       ["      9  "],
       ["  99999  "]],

" " : [["    "],
       ["    "],
       ["    "],
       ["    "],
       ["    "]]
       
}


def writeLettersToConsole(string):
	"""This function takes a string input and prints it as big letters to console"""

	letter_line_size = 5
	string = string.lower()

	for letter_line in range(letter_line_size):
		for letter in string:
			print(letters.get(letter)[letter_line:letter_line+1][0][0], end="")
		print("")


def giveMeChristmas(tree_size = 17, tree_layer_size = 5, tree_char = '*', tree_decoration_char = '0'):
	"""
	* This function prints a christmas tree with decorations.
	* You can change the aperance of the tree by changing tree_char.
	* You can change the decorations of the tree by changing tree_decoration_char.
	* You can change the siz of the tree by changing tree_size, it works better with values bigger than 15.
	* You can change the layer size of the tree by changing tree_layer_size, it could look bad depending on the tree_size.
	"""
	
	#to create an equilateral triangle this function crates two right triangles so size should be half
	tree_size = int(tree_size / 2)

	for layer_index in range(tree_layer_size):

		#creating a size difference between layers
		tree_size_factor = tree_layer_size - layer_index
		dynamic_tree_size =  tree_size - tree_size_factor


		#we should cut some of the layer if it is not the first layer
		if(layer_index == 0):
			cut_the_top = 0
		else:
			cut_the_top = int(dynamic_tree_size/tree_layer_size+1)


		#top
		for i in range(cut_the_top, dynamic_tree_size):

			#adding some extra spaces for compansading size difference on the layers
			for j in range(tree_size - dynamic_tree_size):
				print("   ", end="")

			#adding invisible triangle 
			for j in range(dynamic_tree_size):
				if(j < dynamic_tree_size - i):
					print("   ", end="")

			#adding first half of the triangle and random decorations
			for j in range(dynamic_tree_size):
				if(j <= i):
					if(randrange(10) == 0):
						print(" " + tree_decoration_char + " ", end="")
					else:
						print(" " + tree_char + " ", end="")
			
			#adding second half of the triangle and random decorations
			for j in range(dynamic_tree_size):
				if(j < i):
					if(randrange(10) == 0):
						print(" " + tree_decoration_char + " ", end="")
					else:
						print(" " + tree_char + " ", end="")

			print("")


	#bottom
	for i in range(tree_size):
		for j in range(tree_size*2):
			if(j > (tree_size/2)+1 and j < tree_size + (tree_size/2)-1):
				print(" " + tree_char + " ", end="")
			else:
				print("   ", end="")
		print("")

