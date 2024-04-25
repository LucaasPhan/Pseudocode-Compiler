def OUTPUT(codeLine):

    printed = ''

    # keeping track of the end of the string
    string_flag = False


    if "OUTPUT" in codeLine:
        codeLine = codeLine.lstrip().strip("OUTPUT ")
    elif "PRINT" in codeLine:
        codeLine = codeLine.lstrip().strip("PRINT ")
    
    itemList = codeLine.split(',')
    print(itemList)
    i = 0

    while i < len(itemList) or cont:
        itemNW = re.sub(r'\s+(?=(?:[^"]*"[^"]*")*[^"]*$)', '', itemList[i])
        print(itemList[i])
        


        if itemNW[0] == '\"' :
            string_flag = True
            
            if itemNW[-1] == '\"':
                string_flag = False
                print(string_flag)
            elif itemNW[-1] != '\"':
                itemList[i] = itemList[i] + "," + itemList[i + 1]
                del itemList[i + 1]
                string_flag = True
                print(string_flag)
        
        elif itemNW[-1] ==  "\"" and string_flag:
            itemList[i - 1] = itemList[i - 1] + "," + itemList[i]
            del itemList[i]
            string_flag = False
            print(string_flag)

        elif not string_flag:
            string_flag = False
            print(string_flag)

        if itemNW in itemList[-1]:
           cont = False


        # print(itemList[i])
        i += 1
        

    return itemList

text = 'PRINT "I doubt I can. It’s a major part of many, many words. Omitting it is as hard as making muffins without flour. It’s as hard as spitting without saliva,", Age, " I love my, people,41924798"'
print(OUTPUT(text))