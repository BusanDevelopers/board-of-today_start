from random import randint

def get_Wise():
    wise_saying = {}
    with open('project/static/good.txt', 'r', encoding='utf8') as f:
        index = randint(1, 187)
        string = f.readlines()[index]
        if string.find('-') != -1:
            li = string.split('-')
            contents = []
            check = 0
            start = 0
            for ind, ch in enumerate(li[0]):
                if ch == ' ':
                    check = check + 1
                    if check % 3 == 0:
                        contents.append(li[0][start:ind+1])
                        start = ind
                if len(li[0]) == ind+1:
                    contents.append(li[0][start:])
            wise_saying['contents'] = contents
            wise_saying['person'] = li[1]

        elif string.find('–') != -1:
            li = string.split('–')
            contents = []
            check = 0
            start = 0
            for ind, ch in enumerate(li[0]):
                if ch == ' ':
                    check = check + 1
                    if check % 3 == 0:
                        contents.append(li[0][start:ind+1])
                        start = ind
                if len(li[0]) == ind+1:
                    contents.append(li[0][start:])
            wise_saying['contents'] = contents
            wise_saying['person'] = li[1]

        else:
            contents = []
            check = 0
            start = 0
            for ind, ch in enumerate(string):
                if ch == ' ':
                    check = check + 1
                    if check % 3 == 0:
                        contents.append(string[start:ind+1])
                        start = ind
                if len(string) == ind+1:
                    contents.append(string[start:])
            wise_saying['contents'] = contents

    return wise_saying
