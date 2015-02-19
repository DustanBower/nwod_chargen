#!/usr/bin/env python
"""
Module for generating random NWoD characters.

"""
from nwod_data import CREATION_POINTS
from nwod_data import MERITS

from collections import OrderedDict
from collections import defaultdict
from itertools import chain
from random import choice
from random import randrange
from random import shuffle

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
    ])),

    ('merits', MERITS),

    ])


# There's really just no excuse for this.  I'd like to feel bad about it,
# but I don't.  I'm using a list comprehension to call update multiple times,
# updating a dictionary with the default values appropriate for the type,
# even going so far as to use the int of a truth condition to choose whether
# the default is one or zero.  Since the list has depth, I'm flattening it
# as I go.
PREREQS = {}
_ = [PREREQS.update({_: int(section_ == 'attributes')
                        for _ in chain(*[SECTIONS[section_][_]
                            for _ in [_ for _ in SECTIONS[section_]]])})
                                for section_ in SECTIONS]

PURCHASE_TYPE = 'creation_points'

def dots(section, number):
    """
    Function to calculate how many dots a particular amount of character
    points is worth, by which I mean correct for the fact that 6 cp in
    a skill is 5 dots.

    """

    if section == 'attributes' and number == 5:
        return 4
    if section == 'skills' and number == 6:
        return 5

    return number


def cost(section, dots_, mes_cost=True):
    """
    Determine cost of a particular desired rank (i.e., skill rank 5
    returns 6

    """

    if dots_ == 4 and section == 'attributes':
        return 5

    # correct for the 6 dot cost for 5 dot skills (and merits, for non-MES)
    if dots_ == 5:
        if section == 'skills':
            return 6

        if section == 'merits' and mes_cost == False:
            return 6

    return dots_


def check_prereqs(item, purchase_type=PURCHASE_TYPE):
    """
    Check the prerequisites of an an item.

    item: the particular entry to check the prerequisites of
    purchase_type: what the item is being purchased with
        (e.g., creation points or experience points)

    returns True if the prerequisite is met, false otherwise.

    """
    prereqs = item.get('prereqs')
    creation_only = item.get('CO', False)

    if creation_only and purchase_type != 'creation_points':
        return False

    if not prereqs:
        return True

    # if any are missing or less than the target, prereq check fails
    for prereq in prereqs:
        try:
            if PREREQS[prereq] < prereqs[prereq]:
                return False
        except KeyError:
            return False

    return True


def purchase(sheet, section, category, available,
             purchase_type=PURCHASE_TYPE):
    """
    Logic for purchasing Attributes/Merits/etc.

    """

    selection = choice([_ for _ in sheet[section][category]])
    min_, max_ = (1, 4 if section == 'attributes' else 5)
    if section == 'merits':
        merit = SECTIONS[section][category][selection]
        count = 0

        while not check_prereqs(merit, purchase_type):
            selection = choice([_ for _ in sheet[section][category]])
            merit = SECTIONS[section][category][selection]
            # try 3 times to buy a merit, then give up
            if count >= 3:
                return 0 # no purchase, no cost
            count += 1

    # pick a random number from the amount we're allowed
    if section == 'merits':
        try:
            number = choice(merit['range'])
        except TypeError:
            number = merit['range']
    else:
        number = randrange(min_, max_ + 1)
    number = cost(section, number)

    current_dots = 0

    try:
        current_dots = sheet[section][category][selection]
    except KeyError:
        sheet[section][category][selection] = 0

    number = min(number, available, 5 - current_dots)

    # pick a random stat and add the random value
    if number:
        sheet[section][category][selection] += dots(section, number)
        PREREQS[selection] = sheet[section][category][selection]
    return number


def render_category_types(sheet, section, category, category_type):
    """
    Render type by category.  Since we have zeroed entries for all merits,
    we should skip those merits which are 0 dots, but we can't do the
    same with Attributes and Skills.

    returns a line of the item and the dot value, except if it's a zero-dot
    merit, which returns an empty string.

    """
    if section == 'merits':
        if not sheet[section][category][category_type]:
            return ''

    return '\n{0: <25} {1}'.format(category_type.title(),
                 'o' * sheet[section][category][category_type])


def make_sheet():
    """
    category_creation_points = dict(zip(ATTRIBUTES.keys(),
                                        CREATION_POINTS['attributes']))
    """
    # shuffle available points
    _ = [shuffle(CREATION_POINTS[_]) for _ in ('attributes', 'skills')]


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

            # Merit categories are unimportant
            if section != 'merits':
                output += '\n\n-{}-'.format(category.title())

            # generate the stats closest to the point of printing them so
            # we're not traversing the loop multiple times, because doing that
            # annoys me
            while creation_points > 0:
                creation_points -= purchase(sheet, section, category,
                                            creation_points)

            for category_type in sheet[section][category]:
                output += render_category_types(sheet, section, category,
                                                category_type)

    return output

if __name__ == '__main__':
    print(make_sheet())
