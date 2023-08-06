def print_list(list1):
	for each in list1:
		if isinstance(each,list):
			print_list(each)
		else:
			print(each)