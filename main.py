import csv
from functools import cmp_to_key
import csv


class Armor:

    name: str
    hash: int
    id: str
    notes: str
    tag: str
    tier: str
    type_: str
    equippable: str
    mobility: int
    resilience: int
    recovery: int
    discipline: int
    intellect: int
    strength: int
    total: int
    calculated_score: float
    identifier: int

    def __init__(self, hash, name, tier, type_, equippable, mobility, resilience, recovery, discipline, intellect,
                 strength, total, identifier, notes, tag):
        # self.identifier = int(identifier)
        if equippable == 'Hunter':
            self.calculated_score = (int(mobility) * 0.75) + (int(recovery) * 0.1) + (int(resilience) * 0.05) + (
                int(strength) * 0.05) + (int(discipline) * 0.025) + (int(intellect) * 0.025)
        elif equippable == 'Titan':
            self.calculated_score = (int(mobility) * 0.2) + (int(recovery) * 0.05) + (int(resilience) * 0.65) + (
                int(strength) * 0.05) + (int(discipline) * 0.025) + (int(intellect) * 0.025)
        else:
            self.calculated_score = (int(mobility) * 0.05) + (int(recovery) * 0.65) + (int(resilience) * 0.025) + (
                int(strength) * 0.05) + (int(discipline) * 0.2) + (int(intellect) * 0.025)
        self.hash = hash
        self.identifier = int(identifier[3:len(identifier) - 3])
        self.tag = 'junk'
        self.notes = notes
        self.name = name
        self.tier = tier
        self.type_ = type_
        self.equippable = equippable
        self.mobility = int(mobility)
        self.above_twenty = 0
        if self.mobility >= 20:
            self.above_twenty = self.above_twenty + 1
        self.resilience = int(resilience)
        if self.resilience >= 20:
            self.above_twenty = self.above_twenty + 1
        self.recovery = int(recovery)
        if self.recovery >= 20:
            self.above_twenty = self.above_twenty + 1
        self.discipline = int(discipline)
        if self.discipline >= 20:
            self.above_twenty = self.above_twenty + 1
        self.intellect = int(intellect)
        if self.intellect >= 20:
            self.above_twenty = self.above_twenty + 1
        self.strength = int(strength)
        if self.strength >= 20:
            self.above_twenty = self.above_twenty + 1
        self.total = int(total)

    def __repr__(self):
        return f'name: {self.name}, tier: {self.tier}, type: {self.type_}, equippable: {self.equippable}, mobility: {self.mobility}, resilience: {self.resilience}, recovery: {self.recovery}, discipline: {self.discipline}, intellect: {self.intellect}, strength: {self.strength}, total: {self.total}, calculated_score: {self.calculated_score}, chosen: {self.tag}'


class values:

    sort_one = 'mobility'
    sort_two = 'resilience'


def compare(a, b):
    value_1 = {'property1': None, 'property2': None}
    value_2 = {'property1': None, 'property2': None}
    if values.sort_one == 'mobility':
        value_1['property1'] = a.mobility
        value_2['property1'] = b.mobility
    elif values.sort_one == 'resilience':
        value_1['property1'] = a.resilience
        value_2['property1'] = b.resilience
    elif values.sort_one == 'recovery':
        value_1['property1'] = a.recovery
        value_2['property1'] = b.recovery
    elif values.sort_one == 'discipline':
        value_1['property1'] = a.discipline
        value_2['property1'] = b.discipline
    elif values.sort_one == 'intellect':
        value_1['property1'] = a.intellect
        value_2['property1'] = b.intellect
    else:
        value_1['property1'] = a.strength
        value_2['property1'] = b.strength

    if values.sort_two == 'mobility':
        value_1['property2'] = a.mobility
        value_2['property2'] = b.mobility
    elif values.sort_two == 'resilience':
        value_1['property2'] = a.resilience
        value_2['property2'] = b.resilience
    elif values.sort_two == 'recovery':
        value_1['property2'] = a.recovery
        value_2['property2'] = b.recovery
    elif values.sort_two == 'discipline':
        value_1['property2'] = a.discipline
        value_2['property2'] = b.discipline
    elif values.sort_two == 'intellect':
        value_1['property2'] = a.intellect
        value_2['property2'] = b.intellect
    else:
        value_1['property2'] = a.strength
        value_2['property2'] = b.strength

    if value_1['property1'] == value_2['property1']:
        if value_1['property2'] == value_2['property2']:
            return 0
        elif value_1['property2'] < value_2['property2']:
            return 1
        else:
            return -1
    elif value_1['property1'] < value_2['property1']:
        return 1
    else:
        return -1


def add_top_two(class_):
    if len(class_) == 0:
        return
    if len(class_) == 1:
        class_[0].tag = 'keep'
    else:
        class_[0].tag = 'keep'
        class_[1].tag = 'keep'


def sort_in_order(class1, class2):
    if class1.identifier == class2.identifier:
        if class1.tag == 'keep':
            if class2.tag == 'keep':
                return 0
            return -1
        elif class2.tag == 'keep':
            return 1
    if class1.identifier > class2.identifier:
        return -1
    return 1


def sort_armor(class_):
    stats = ['mobility', 'resilience', 'recovery', 'discipline', 'intellect', 'strength']
    for stat in stats:
        for stat2 in stats:
            if stat != stat2:
                values.sort_one = stat
                values.stat_two = stat2
                class_ = sorted(class_, key=cmp_to_key(compare))
                add_top_two(class_)

    class_ = sorted(class_, key=cmp_to_key(lambda item1, item2: item2.calculated_score - item1.calculated_score))
    if len(class_) > 0:
        class_[0].tag = 'keep'
    for item in class_:
        if item.above_twenty >= 1:
            item.tag = 'keep'


def sort_classes(class_):
    helmet = list(filter(lambda x: (x.type_ == 'Helmet'), class_))
    gauntlet = list(filter(lambda x: (x.type_ == 'Gauntlets'), class_))
    chest_armor = list(filter(lambda x: (x.type_ == 'Chest Armor'), class_))
    extra = list(
        filter(lambda x: (x.type_ == 'Hunter Cloak' or x.type_ == 'Warlock Bond' or x.type_ == 'Titan Mark'), class_))
    leg_armor = list(filter(lambda x: (x.type_ == 'Leg Armor'), class_))
    sort_armor(helmet)
    sort_armor(gauntlet)
    sort_armor(chest_armor)
    sort_armor(extra)
    sort_armor(leg_armor)


def sort_items(list_of_armor):
    hunter = list(filter(lambda x: (x.equippable == 'Hunter'), list_of_armor))
    warlock = list(filter(lambda x: (x.equippable == 'Warlock'), list_of_armor))
    titan = list(filter(lambda x: (x.equippable == 'Titan'), list_of_armor))
    sort_classes(hunter)
    sort_classes(warlock)
    sort_classes(titan)


items = []

with open('destinyArmor.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    skip = True
    for row in spamreader:
        if skip:
            skip = False
        else:
            items.append(
                Armor(row[1], row[0], row[4], row[5], row[7], row[27], row[28], row[29], row[30], row[31], row[32],
                      row[33], row[2], row[36], row[3]))
items3 = list(filter(lambda x: (x.tier == 'Rare'), items))
items4 = list(filter(lambda x: (x.tier == 'Exotic'), items))
for item in items4:
    item.tag = 'keep'
items2 = list(filter(lambda x: (x.tier != 'Exotic' and x.tier != 'Rare'), items))
sort_items(items2)
items2 = items2 + items3 + items4
# items2 = list(filter(lambda x: x.tag == 'keep', items2))
with open('output.csv', mode='w', newline='') as employee_file:
    employee_writer = csv.writer(employee_file)
    employee_writer.writerow(['Name', 'Hash', 'Id', 'Tag', 'Notes'])
    for item in items2:
        employee_writer.writerow([item.name, item.hash, "\"" + str(item.identifier) + "\"", item.tag, ""])
