def print_lol (the_list, the_level=0):
    for each_item in the_list:
        if isinstance(the_list,list):
            print_lol(each_item,the_level+1)
        else:
            print(each_item)
