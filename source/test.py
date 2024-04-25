import re

def OUTPUT(codeLine):
    # remove the OUTPUT and PRINT of the codeLine
    if "OUTPUT" in codeLine:
        codeLine = codeLine.lstrip().strip("OUTPUT ")
    elif "PRINT" in codeLine:
        codeLine = codeLine.lstrip().strip("PRINT ")

    # The complete item list of the
    splited_item_list= []
    items_by_comma = codeLine.split(",")
    item_index_count = 0
    in_string = False

    for item in items_by_comma:
        if item[0] == " ":
            item = item.lstrip()

            if item[0] == "\"" and item[-1] == "\"":
                splited_item_list.append(item)
                item_index_count += 1
                in_string = False   
            elif item[0] == "\"" and item[-1] != "\"":
                splited_item_list.append(item)
                in_string = True
            elif item[0] != '\"' and item[-1] != '\"' and in_string:
                splited_item_list[item_index_count] += ", " + item 
                in_string = True
            elif item[-1] == '\"' and in_string:
                splited_item_list[item_index_count] += ", " + item 
                item_index_count += 1
                in_string = False

            if item[0] != '\"' and item[-1] != '\"' and not in_string:
                item_index_count += 1
                splited_item_list.append(item)
        else:
            if item[0] == "\"" and item[-1] == "\"":
                splited_item_list.append(item)
                item_index_count += 1
                in_string = False   
            elif item[0] == "\"" and item[-1] != "\"":
                splited_item_list.append(item)
                in_string = True
            elif item[0] != '\"' and item[-1] != '\"' and in_string:
                splited_item_list[item_index_count] += "," + item 
                in_string = True
            elif item[-1] == '\"' and in_string:
                splited_item_list[item_index_count] += "," + item 
                item_index_count += 1
                in_string = False

            if item[0] != '\"' and item[-1] != '\"' and not in_string:
                item_index_count += 1
                splited_item_list.append(item)

    print(splited_item_list)

    printed = "" 
    for item in splited_item_list:
        if item[0] == '\"' and item[-1] == '\"':
            printed += item[1:-1]
        if item[0] != '\"' and item[-1] != '\"':
            printed += item
    
    print(printed)


text = input()
OUTPUT(text)

