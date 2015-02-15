#!/usr/bin/env python
from collections import OrderedDict
from collections import defaultdict
from random import choice
from random import randrange
from random import shuffle

CREATION_POINTS = {
    'attributes': [5, 4, 3],
    'skills': [11, 7, 4],
    'merits': [7],
}

MERITS = {
    'Common Sense': {'range': [1], 'CO': True},
    'Danger Sense': {'range': [2]},
    'Eidetic Memory': {'range': [2], 'CO': True},
    'Encyclopedic Knowledge': {'range': [4], 'CO': True},
    'Holistic Awareness': {'range': [3]},
    'Language': {'range': [1]},
    'Meditative Mind': {'range': [1]},
    'Unseen Sense': {'range': [3]},

    'Ambidextrous': {'range': [3], 'CO': True},
    'Brawling Dodge': {'range': [1], 'prereqs': {'strength': 2, 'brawl': 1}},
    'Direction Sense': {'range': [1]},
    'Disarm': {'range': [2]},
    'Fast Reflexes': {'range': [1, 2], 'cost': 'simple'},
    'Fighting Finesse': {'range': [2],
                         'prereqs': {'dexterity': 3, 'weaponry': 2}},
    #'Fighting Style'
    'Fleet of Foot': {'range': [1, 2, 3]},
    'Fresh Start': {'range': [1]},
    'Giant': {'range': [4], 'CO': True},
    'Gunslinger': {'range': [3]},
    'Iron Stamina': {'range': [1, 2, 3]},
    'Iron Stomach': {'range': [2]},
    'Natural Immunity': {'range': [1]},
    'Quick Draw': {'range': [1], 'prereqs': {'dexterity': 3}},
    'Quick Healer': {'range': [4], 'prereqs': {'stamina': 4}},
    'Strong Back': {'range': [1], 'prereqs': {'dexterity': 3}},
    'Strong Lungs': {'range': [3], 'prereqs': {'athletics': 3}},
    'Stunt Driver': {'range': [3], 'prereqs': {'dexterity': 3}},
    'Toxin Resistance': {'range': [2], 'prereqs': {'stamina': 3}},
    'Weaponry Dodge': {'range': [1],
                       'prereqs': {'strength': 2, 'weaponry': 1}},

    'Allies': {'range': [1, 2, 3, 4, 5]},
    'Barfly': {'range': [1]},
    'Contacts': {'range': [1, 2, 3, 4, 5]},
    'Fame': {'range': [1, 2, 3, 4, 5]},
    'Inspiring': {'range': 4},
    'Mentor': {'range': [1, 2, 3, 4, 5]},
    'Resources': {'range': [1, 2, 3, 4, 5]},
    'Retainer': {'range': [1, 2, 3, 4, 5]},
    'Status': {'range': [1, 2, 3, 4, 5]},
    'Striking Looks': {'range': [2, 4]},
}

BASE_DOTS = defaultdict(int, {'attributes': 1})

SECTIONS = OrderedDict([
    ('attributes', OrderedDict([
        ('mental', ['intelligence', 'wits', 'resolve']),
        ('physical', ['strength', 'dexterity', 'stamina']),
        ('social', ['presence', 'manipulation', 'composure']),
    ])),

    ('skills', OrderedDict([
        ('mental', ['academics', 'computer', 'craft', 'investigation',
                    'medicine', 'occult', 'politics', 'science']),
        ('physical', ['athletics', 'brawl', 'drive', 'firearms', 'larceny',
                     'stealth', 'survival', 'weaponry']),
        ('social', ['animal ken', 'empathy', 'expression', 'intimidation',
                   'persuasion', 'socialize', 'streetwise', 'subterfuge']),
    ]))])

def dots(section, number):
    """
    Function to calculate how many dots a particular amount of character
    points is worth, by which I mean correct for the fact that 6 cp in
    a skill is 5 dots.

    """
    if section == 'skills' and number == 6:
        return 5

    return number


def make_sheet():
    # shuffle available points
    [shuffle(CREATION_POINTS[_]) for _ in ('attributes', 'skills')]

    """
    category_creation_points = dict(zip(ATTRIBUTES.keys(),
                                        CREATION_POINTS['attributes']))
    """

    # create empty ordered dicts for attributes and skills corresponding
    # to the order commonly used on sheets, blank sheet, in other words
    # basically we're building an ordered dict in the form of
    #   sheet['attributes']['mental']['intelligence'], etc.
    sheet = OrderedDict([(section, 
        OrderedDict([(category,
            OrderedDict([(section_type, BASE_DOTS[section])
                for section_type in SECTIONS[section][category]]))
                    for category in SECTIONS[section]]))
                        for section in SECTIONS])

    # display sheet
    output = ""
    for section in sheet:
        output += '\n\n==={}==='.format(section.upper())
        for category, creation_points in zip(sheet[section],
                                             CREATION_POINTS[section]):
            output += '\n\n-{}-'.format(category.title())
            # generate the stats closest to the point of printing them so
            # we're not traversing the loop multiple times, because doing that
            # annoys me
            while creation_points > 0:
                # pick a random number from the amount we're allowed
                max_ = 4 if section == 'attributes' else 5
                number = randrange(1, max_ + 1)
                # correct for the 6 dot cost for 5 dot skills

                number = (6 if number == 5 and section == 'skills'
                          else number)
                selection = choice([_ for _ in sheet[section][category]])
                current_dots = sheet[section][category][selection]
                number = min(number, creation_points, 5 - current_dots)
                # pick a random stat and add the random value
                sheet[section][category][selection] += dots(section, number)
                creation_points -= number

            for category_type in sheet[section][category]:
                output += '\n{0: <15} {1}'.format(category_type.title(),
                     'o' * sheet[section][category][category_type])

    return output

if __name__ == '__main__':
    print(make_sheet())
