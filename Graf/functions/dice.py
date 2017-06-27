from random import randint


digs = '0123456789'

def roll(orig):
	new = ''
	dice = False
	die = ''
	start = 0
	ret = 0

	for i, v in enumerate(orig):
		if v == 'd':
			dice = True
			start = i
			continue

		if dice:
			#check if end of string
			if v in digs:
				die += v
			elif v in '+-/*()':
				#string[:start] + random + string[index+1:]
				try:
					new += str(randint(1,int(die))) + v
				except:
					return '', -1

				dice = False
				die = ''
			else:
				print('NAH')

		else:
			if v not in digs + '+-/*()':
				print("Encountered bad character at", i+1)
				return '', -1
			else:
				new += v

	if dice:
		try:
			new += str(randint(1,int(die)))
		except:
			return '', -1

	try:
		ret = int(eval(new))
	except:
		pass

	return new, ret
