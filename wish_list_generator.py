file1 = open('wish_list.txt', 'r', encoding='utf8')
lines = file1.readlines()

found_pvp = False
grouping = ''
things_to_keep = ''
item_found = False
for line in lines:
    if line.startswith('//'):
        if item_found:
            if found_pvp:
                grouping = ''
            else:
                things_to_keep = things_to_keep + grouping
                grouping = ''
            item_found = False
            found_pvp = False
        if 'pvp' in line.lower():
            found_pvp = True
    else:
        item_found = True
    if 'pvp' not in line.lower():
        grouping = grouping + line

things_to_keep = things_to_keep + '\n' + grouping
f = open("wish_list_refined.txt", "a", encoding='utf8')
f.write(things_to_keep)