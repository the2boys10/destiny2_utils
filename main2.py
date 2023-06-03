import csv
import csv
from typing import List

JUNK = 'junk'
KEEP = 'keep'

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
        self.hash = hash
        self.identifier = int(identifier[3:len(identifier) - 3])
        self.combination_fail = 0
        self.failed_round = False
        self.tag = KEEP
        self.notes = notes
        self.name = name
        self.tier = tier
        self.type_ = type_
        self.equippable = equippable
        self.mobility = int(mobility)
        self.resilience = int(resilience)
        self.recovery = int(recovery)
        self.discipline = int(discipline)
        self.intellect = int(intellect)
        self.strength = int(strength)
        self.total = int(total)

    def __repr__(self):
        return f'name: {self.name}, tier: {self.tier}, type: {self.type_}, equippable: {self.equippable}, mobility: {self.mobility}, resilience: {self.resilience}, recovery: {self.recovery}, discipline: {self.discipline}, intellect: {self.intellect}, strength: {self.strength}, total: {self.total}, chosen: {self.tag}'

def _remove_legendaries_less_than_threshold(items: List[Armor]) -> List[Armor]:
    filtered_items = []
    for item in items:
        if item.total < 60:
            item.tag = JUNK
            continue
        filtered_items.append(item)
    return filtered_items

def _set_all_items_to_tag(items: List[Armor], tag: str):
    for item in items:
        item.tag = tag

def _is_better_in_all_stats(item_1: List[Armor], item_2: List[Armor], stats: List[str]):
        stat_counter = 0
        for stat in stats:
            if item_1.__dict__[stat] > item_2.__dict__[stat]:
                stat_counter += 1
        if stat_counter == len(stats):
            return True
        return False

def _filter_keep_items(items: List[Armor]) -> List[Armor]:
    filtered_items = []
    for item in items:
        if item.tag == KEEP:
            filtered_items.append(item)
    return filtered_items

def _filter_items_which_have_been_superseeded(items: List[Armor], stats: List[str]) -> List:
    _set_all_items_to_tag(items=items, tag=KEEP)
    for i in range(len(items)):
        for j in range(i+1, len(items)):
            if items[j].tag == JUNK:
                continue
            if _is_better_in_all_stats(item_1=items[i], item_2=items[j], stats=stats):
                items[j].tag == JUNK
    return _filter_keep_items(items=items)

def _create_powerset_2_from_list(items: List[str]) -> List[List[str]]:
    stat_combinations = []
    for i in range(len(items)):
        for j in range(i+1, len(items)):
            stat_combinations.append([items[i], items[j]])
    return stat_combinations

def _set_failed_round(items: List[Armor], value: List[str]) -> None:
    for item in items:
        item.failed_round = value

def _set_combination_fail_for_powerset_2(items: List[Armor], stat_combination: List[str]) -> None:
    _set_failed_round(items=items, value=False)
    for i in range(len(items)):
        if items[i].failed_round == True:
            continue
        for j in range(len(items)):
            if items[j].failed_round == True or i==j:
                continue
            stat_counter = 0
            for stat in stat_combination:
                if items[i].__dict__[stat] > items[j].__dict__[stat]:
                    stat_counter += 1
            if stat_counter == len(stat_combination):
                items[j].failed_round = True
    for item in items:
        if item.failed_round == True:
            item.combination_fail += 1

def _filter_based_on_stat_powerset_2(items: List[Armor], stats: List[str]) -> List[Armor]:
    stat_combinations = _create_powerset_2_from_list(items=stats)
    for stat_combination in stat_combinations:
        _set_combination_fail_for_powerset_2(items=items, stat_combination=stat_combination)
    for item in items:
        if item.combination_fail == len(stat_combinations):
            item.tag = JUNK
    return _filter_keep_items(items=items)

def _sort_armor(items: List[Armor]):
    stats = ['mobility', 'resilience', 'recovery', 'discipline', 'intellect', 'strength']
    filtered_items = _remove_legendaries_less_than_threshold(items=items)
    filtered_items = _filter_items_which_have_been_superseeded(items=filtered_items, stats=stats)
    filtered_items = _filter_based_on_stat_powerset_2(items=filtered_items, stats=stats)

def _sort_classes(items: List[Armor]):
    helmet = list(filter(lambda x: (x.type_ == 'Helmet'), items))
    gauntlet = list(filter(lambda x: (x.type_ == 'Gauntlets'), items))
    chest_armor = list(filter(lambda x: (x.type_ == 'Chest Armor'), items))
    extra = list(
        filter(lambda x: (x.type_ == 'Hunter Cloak' or x.type_ == 'Warlock Bond' or x.type_ == 'Titan Mark'), items))
    leg_armor = list(filter(lambda x: (x.type_ == 'Leg Armor'), items))
    armors = [helmet, gauntlet, chest_armor, extra, leg_armor]
    for armor in armors:
        _sort_armor(items=armor)


def _sort_items(list_of_armor: List[Armor]):
    hunter = list(filter(lambda x: (x.equippable == 'Hunter'), list_of_armor))
    warlock = list(filter(lambda x: (x.equippable == 'Warlock'), list_of_armor))
    titan = list(filter(lambda x: (x.equippable == 'Titan'), list_of_armor))
    _sort_classes(items=hunter)
    _sort_classes(items=warlock)
    _sort_classes(items=titan)


def _filter_armor():
    items = []
    with open('destinyArmor.csv', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        skip = True
        for row in spamreader:
            if skip:
                skip = False
                continue
            items.append(
                Armor(hash=row[1], name=row[0], tier=row[4], type_=row[5], equippable=row[7], mobility=row[24], resilience=row[25], recovery=row[26], discipline=row[27], intellect=row[29], strength=row[29],
                        total=row[30], identifier=row[2], notes=row[33], tag=row[3]))
    items_filtered = list(filter(lambda x: (x.tier == 'Legendary'), items))
    _sort_items(list_of_armor=items_filtered)
    with open('output.csv', mode='w', newline='') as employee_file:
        employee_writer = csv.writer(employee_file)
        employee_writer.writerow(['Name', 'Hash', 'Id', 'Tag', 'Notes'])
        for item in items_filtered:
            employee_writer.writerow([item.name, item.hash, "\"" + str(item.identifier) + "\"", item.tag, ""])

if __name__== "__main__":
    _filter_armor()