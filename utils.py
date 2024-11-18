import json
import streamlit as st
import streamlit_shadcn_ui as ui
from streamlit_space import space
import random

animals = json.load(open(r'betterAnimalDB\animals.json', 'r'))


def get_traits(animal1, animal2):

    trait1, trait2 = None, None
    for animal in animals:
        if animal['name'] == animal1:

            trait1 = {'Class': animal['taxonomy']['class'],
              'Location': animal['locations'],
              'Diet': animal['characteristics']['diet'],
                'Prey': animal['characteristics']['main_prey']
                      }

        elif animal['name'] == animal2:

            trait2 = {'Class': animal['taxonomy']['class'],
              'Location': animal['locations'],
              'Diet': animal['characteristics']['diet'],
                'Prey': animal['characteristics']['main_prey']
                }

    return trait1, trait2

def compare_traits(animal1, animal2):
    traits1, traits2 = get_traits(animal1, animal2)

    shared = {}
    for trait in ['Class', 'Diet', 'Prey']:
        if traits1[trait] == traits2[trait]:
            shared[trait] = traits1[trait]

        # Compare 'location' as a special case
    locations1 = set(traits1['Location'])
    locations2 = set(traits2['Location'])
    common_locations = locations1.intersection(locations2)

    # Add shared locations to shared traits
    if common_locations:
        shared['Location'] = ", ".join(common_locations)

    return shared

def uncover_card(shared_traits, i):
    if shared_traits:
        num = len(shared_traits)
        topCols_count = min(num, 2)
        buttonCols_count = max(0, num-topCols_count)

        topCols = st.columns(topCols_count)


        for k in range(topCols_count):
            with topCols[k]:
                key = list(shared_traits.keys())[k]
                ui.metric_card(title=key, content=shared_traits[key], key=f"card{random.randint(0, 20000)}")

        if buttonCols_count > 0:
            buttonCols = st.columns(buttonCols_count)
            for k in range(buttonCols_count):
                with buttonCols[k]:
                    key = list(shared_traits.keys())[k+topCols_count]
                    ui.metric_card(title=key, content=shared_traits[key], key=f"card{random.randint(0, 20000)}")

        space()
    else:
        st.title("Unfortunately no commonalities")


