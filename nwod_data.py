"""
Module for data for generating random NWoD characters.

"""

CREATION_POINTS = {
    'attributes': [5, 4, 3],
    'skills': [11, 7, 4],
    'merits': [7],
}

MERITS = {
    'mental': {
        'common sense': {'range': [1], 'CO': True},
        'danger sense': {'range': [2]},
        'eidetic memory': {'range': [2], 'CO': True},
        'encyclopedic knowledge': {'range': [4], 'CO': True},
        'holistic awareness': {'range': [3]},
        'language': {'range': [1]},
        'meditative mind': {'range': [1]},
        'unseen sense': {'range': [3]},
    },

    'physical': {
        'ambidextrous': {'range': [3], 'CO': True},
        'brawling dodge': {'range': [1],
                           'prereqs': {'strength': 2, 'brawl': 1}},
        'direction sense': {'range': [1]},
        'disarm': {'range': [2]},
        'fast reflexes': {'range': [1, 2], 'cost': 'simple'},
        'fighting finesse': {'range': [2],
                             'prereqs': {'dexterity': 3, 'weaponry': 2}},

        #'Fighting Style'
        'fleet of foot': {'range': [1, 2, 3]},
        'fresh start': {'range': [1]},
        'giant': {'range': [4], 'CO': True},
        'gunslinger': {'range': [3]},
        'iron stamina': {'range': [1, 2, 3]},
        'iron stomach': {'range': [2]},
        'natural immunity': {'range': [1]},
        'quick draw': {'range': [1], 'prereqs': {'dexterity': 3}},
        'quick healer': {'range': [4], 'prereqs': {'stamina': 4}},
        'strong back': {'range': [1], 'prereqs': {'dexterity': 3}},
        'strong lungs': {'range': [3], 'prereqs': {'athletics': 3}},
        'stunt driver': {'range': [3], 'prereqs': {'dexterity': 3}},
        'toxin resistance': {'range': [2], 'prereqs': {'stamina': 3}},
        'weaponry dodge': {'range': [1],
                           'prereqs': {'strength': 2, 'weaponry': 1}},

    },

    'social': {
        'allies': {'range': [1, 2, 3, 4, 5]},
        'barfly': {'range': [1]},
        'contacts': {'range': [1, 2, 3, 4, 5]},
        'fame': {'range': [1, 2, 3, 4, 5]},
        'inspiring': {'range': 4},
        'mentor': {'range': [1, 2, 3, 4, 5]},
        'resources': {'range': [1, 2, 3, 4, 5]},
        'retainer': {'range': [1, 2, 3, 4, 5]},
        'status': {'range': [1, 2, 3, 4, 5]},
        'striking looks': {'range': [2, 4]},
    }
}
