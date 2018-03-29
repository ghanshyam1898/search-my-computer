def get_combinations_of_search_file(search_file):
    combinations = []

    # for " " -> "_"
    temp = ""
    for item in search_file:
        if item == " ":
            temp += "_"
        else:
            temp += item
    combinations.append(temp)

    # for " " -> "-"
    temp = ""
    for item in search_file:
        if item == " ":
            temp += "-"
        else:
            temp += item
    combinations.append(temp)

    # for "_" -> " "
    temp = ""
    for item in search_file:
        if item == "_":
            temp += " "
        else:
            temp += item
    combinations.append(temp)

    # for "_" -> "-"
    temp = ""
    for item in search_file:
        if item == "_":
            temp += "-"
        else:
            temp += item
    combinations.append(temp)


    # for "-" -> " "
    temp = ""
    for item in search_file:
        if item == "":
            temp += " "
        else:
            temp += item
    combinations.append(temp)

    # for "-" -> "_"
    temp = ""
    for item in search_file:
        if item == "-":
            temp += "_"
        else:
            temp += item
    combinations.append(temp)

    temp = []
    for item in combinations:
        if item not in temp:
            temp.append(item)
    combinations = temp

    if len(combinations) == 0:
        combinations.append(search_file)

    return combinations
#



def string_to_word_list(search_file):
	combinations = []
	splitted_search_file = []
	temp = ''

	for item in search_file:
		if item in (' ', '-', '_'):
			if len(temp) > 0:
				splitted_search_file.append(temp)
				temp = ''
		else:
			temp += item

	if len(temp) > 0:
		splitted_search_file.append(temp)
		temp = ''

	return splitted_search_file


if __name__ == '__main__':
	print(string_to_word_list(input("Enter the name of the file : ")))
