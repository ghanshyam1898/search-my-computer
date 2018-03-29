import os
import urllib.request, urllib.parse, urllib.error
import threading
import json
from get_search_combinations import get_combinations_of_search_file


database_loaded = False
file_names = []
matching_files = []
root = "/"
file_paths_database_location = "database/local_searching_index_file"
first_alphabet_index_database_location = "database/first_alphabet_index_file"
data = []
told_results = []
exactly_matching_case_sensitive_results = []
exactly_matching_case_insensitive_results = []
less_relevant_results = []
folder_names_results = []
all_search_results = []
first_alphabet_index = {}
search_file = ''
less_relevant_results_threads = {}


def get_url_encoded(file_address):
    base_url = "file://"
    temp = ""
    if file_address.startswith("/"):
        file_address = file_address[1:]
    file_address = file_address.split("/")[:-1]
    for item in file_address:
        temp += "/"
        temp += item
    temp = urllib.parse.quote(temp)
    temp = base_url + temp
    return temp


def load_database():
    global file_paths_database_location, file_names, data, first_alphabet_index

    database_validator_result = validate_database()

    if database_validator_result is False:
        input("An error encountered. One or more database file not found. Press enter to exit.")
        exit()

    with open(file_paths_database_location, 'r') as index_file:
        data = index_file.read()
        data = data.split("\n")

    for item in data:
        item = item.split("/")[-1]
        file_names.append(item)

    with open(first_alphabet_index_database_location, 'r') as index_file:
        first_alphabet_index = index_file.read()
        first_alphabet_index = json.loads(first_alphabet_index)


def validate_database():
    global file_paths_database_location

    try:
        with open(file_paths_database_location, 'r') as my_file:
            with open(first_alphabet_index_database_location, 'r') as my_file_1:
                return True

    except:
        return False


def find_exactly_matching_case_sensitive_results():
    global data, search_file, told_results, exactly_matching_case_sensitive_results, first_alphabet_index

    count = 0

    for item in first_alphabet_index[search_file[0].lower()]:

        if file_names[item] == search_file:
            told_results.append(data[count])
            exactly_matching_case_sensitive_results.append(data[count])

        count += 1


def find_exactly_matching_case_insensitive_results():
    global data, search_file, told_results, exactly_matching_case_insensitive_results, first_alphabet_index

    count = 0
    for item in first_alphabet_index[search_file[0]]:

        if file_names[item] == search_file:
            told_results.append(data[count])
            exactly_matching_case_insensitive_results.append(data[count])

        count += 1


def find_less_relevant_results():
    global data, search_file, told_results, exactly_matching_case_sensitive_results, less_relevant_results_threads
    combinations_of_search_file = get_combinations_of_search_file(search_file)

    for selected_search_file in combinations_of_search_file:
        less_relevant_results_threads[selected_search_file] = threading.Thread(target=search_for_supplied_combination, args=(selected_search_file,))
        less_relevant_results_threads[selected_search_file].start()

    for key in less_relevant_results_threads:
        less_relevant_results_threads[key].join()


def search_for_supplied_combination(selected_search_file):
    global data, told_results, less_relevant_results, file_names

    count = 0

    selected_search_file_lower_case = selected_search_file.lower()
    for item in file_names:

        if selected_search_file_lower_case in item.lower() and item not in told_results:
            less_relevant_results.append(data[count])

        count += 1


def search_in_folder_names():
    global data, search_file, told_results, folder_names_results

    for item in data:
        if search_file.lower() in item.lower() and item not in told_results:
            folder_names_results.append(item)


def first_alphabet_indexing():
    global data, file_names, first_alphabet_index

    alphabets = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
                 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

    first_alphabet_index = {}

    for alphabet in alphabets:
        temp = []
        count = 0

        for item in data:
            if item.split('/')[-1][0].lower() == alphabet.lower():
                temp.append(count)

            count += 1
        first_alphabet_index[alphabet] = temp

    temp = []
    count = 0
    for item in data:
        if item.split('/')[-1][0].lower() not in alphabets:
            temp.append(count)

        count += 1

    first_alphabet_index['others'] = temp

    first_alphabet_index = json.dumps(first_alphabet_index)

    with open(first_alphabet_index_database_location, 'w') as myfile:
        myfile.write(first_alphabet_index)


load_database_thread = threading.Thread(target=load_database)
find_exactly_matching_results_thread = threading.Thread(target=find_exactly_matching_case_sensitive_results)
find_less_relevant_results_thread = threading.Thread(target=find_less_relevant_results)
search_in_folder_names_thread = threading.Thread(target=search_in_folder_names)


load_database_thread.start()

ans = input("\nEnter the file name to search OR Type 'refresh' to refresh the index : ")

if ans == "refresh":
    count = 0

    print("Fetching list of files in the given location...\nPlease wait \n\nNote that"
          " I will print the name of every 100th file I find..\n\n")

    for path, subdirs, files in os.walk(root):
        for name in files:
            count += 1
            matching_files.append(os.path.join(path, name))
            if count % 100 == 0:
                print(path, end=' ')
                print(name)

    data = matching_files
    print("\n\nList of all files in the given location obtained.")

    with open(file_paths_database_location, 'w') as index_file:
        for item in matching_files:
            try:
                index_file.write(item)
                index_file.write("\n")
            except UnicodeEncodeError:
                print("Encountered a UnicodeEncodeError. Ignoring it.")

    print("\n\nFinished crawling files. Now starting first alphabet indexing.")

    first_alphabet_indexing()

    print("\n\nIndex refreshed. Start the program again to search.")

else:

    # Variables :

    # data - list - contains the full paths
    # search_file - string - contains the item to search
    # told_results - list - contains previously matching elements, to avoid repetion of same result
    # file_names - list - contains only the names of the files, not the path

    search_file = ans

    load_database_thread.join()
    # print("database loaded")
    find_exactly_matching_results_thread.start()
    # print("Exactly matching startrd")
    find_less_relevant_results_thread.start()
    # print("less relevant started")
    search_in_folder_names_thread.start()
    # print("folder names search started")

    # print("waiting for results from exactly matching thread.")
    find_exactly_matching_results_thread.join()
    # print("exactly matching found")
    find_less_relevant_results_thread.join()
    # print("less relevant found")
    search_in_folder_names_thread.join()
    # print("folder names searched")

    for item in exactly_matching_case_sensitive_results:
        all_search_results.append(item)

    for item in less_relevant_results:
        all_search_results.append(item)

    for item in folder_names_results:
        all_search_results.append(item)

    all_search_results=set(all_search_results)
    all_search_results = list(set(all_search_results))

    if len(all_search_results) == 0:
        print("\n\n\nNo search results found for the given query\n\n\n")

    elif len(all_search_results) > 5:
        print(str(len(all_search_results)) + " results found\n\n")
        file_type = input("Please enter the file type to filter the results or just press enter : ")
        if file_type == "":
            count = 0
            for item in all_search_results:
                count += 1
                if count % 10 == 0:
                    input("\n-- Press enter to see more results -- ")

                print(item.split("/")[-1])
                print(item)
                print(get_url_encoded(item))
                print("\n\n")

        else:
            temp = []
            for item in all_search_results:
                if item.endswith(file_type):
                    print(item.split("/")[-1])
                    print(item)
                    print(get_url_encoded(item))
                    temp.append(item)
                    print("\n\n")

            input("\n\n-- Press enter to see other results -- ")
            count = 0
            for item in all_search_results:
                if item not in temp:
                    count += 1
                    if count % 10 == 0:
                        input("\n-- Press enter to see more results -- ")
                    print(item.split("/")[-1])
                    print(item)
                    print(get_url_encoded(item))
                    print("\n\n")

    else:
        for item in all_search_results:
            print("\n\n")
            print(item.split("/")[-1])
            print(item)
            print(get_url_encoded(item))
