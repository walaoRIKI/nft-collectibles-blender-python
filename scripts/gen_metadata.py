import json
from os import path
import random
import re
import shutil


#  --- Settings -----------------------------------------------------------------------------------------

# Total number of characters generated
TOTAL_CHARACTERS = 20

# An absolute path for the root directory
PROJECT_DIR = "/Users/teoh/Desktop/nft-collectibles-blender-python/"

# Output directory to where all metadata files generated
OUTPUTS_DIR = PROJECT_DIR + "outputs/"

# Metadata JSON structure - Please see https://docs.opensea.io/docs/metadata-standards
METADATA_NAME = "NFT Character"
METADATA_SYMBOL = ""
METADATA_DESCRIPTION = "NFT Collectibles using Blender Python"
METADATA_IMAGE_URL = "https://example.com/"
METADATA_EXTERNAL_URL = "https://example.com/"

# List - One item will be selected for each list
list_body = [
    "samurai 5", "samurai 7"
]
list_head = [
    "chicken", "cow", "dog", "dragon", "horse", "monkey", "mouse", "pig", "rabbit", "sheep", "snake", "tiger"
]
list_hand = [
    "samurai 5", "samurai 7"
]
list_leg = [
    "samurai 5", "samurai 7"
]
list_bg = [
    "bg1", "bg2", "bg3", "bg4", "bg5", "bg6", "bg7", "bg8", "bg9", "bg10", "bg11", "bg12", "bg13", "bg14", "bg15",
    "bg16", "bg17"
]
# -------------------------------------------------------------------------------------------------------


def rand_attributes(id):
    # Random parts
    rand_head = random.choice(list_head)
    rand_body = random.choice(list_body)
    rand_hand = random.choice(list_hand)
    rand_leg = random.choice(list_leg)
    rand_bg = random.choice(list_bg)

    # Formatting
    # rand_body = rand_body.replace("_", " ").title()
    # rand_head = rand_head.replace("_", " ").title()
    # rand_hand = rand_hand.replace("_", " ").title()
    # rand_leg = rand_leg.replace("_", " ").title()

    attributes = [
        {
            "trait_type": "Body",
            "value": rand_body
        },
        {
            "trait_type": "Head",
            "value": rand_head
        },
        {
            "trait_type": "Hand",
            "value": rand_hand
        },
        {
            "trait_type": "Leg",
            "value": rand_leg
        },
        {
            "trait_type":"bg",
            "value":rand_bg
        }
    ]

    return attributes

def main():
    # Check settings
    if path.exists(PROJECT_DIR) == False:
        print("ERROR: Project directory does not exist. Set the absolute path to the PROJECT_DIR.")
        return
    if path.exists(OUTPUTS_DIR) == False:
        print("ERROR: Outputs directory does not exist. Set the absolute path to the OUTPUTS_DIR.")
        return

    print("Start generating metadata...")

    # Create dict
    dict_list = []

    for i in range(TOTAL_CHARACTERS):
        attributes = rand_attributes(i)
        adict = {
            "attributes": attributes
        }
        dict_list.append(adict)

    # Remove duplicates for json
    unique_list = list(map(json.loads, set(map(json.dumps, dict_list))))
    # Check duplicates
    if len(unique_list) < TOTAL_CHARACTERS:
        print("ERROR: Properties duplicate. Please run again.")
        return

    json_data = {}

    for i, adict in enumerate(unique_list):
        # Create metadata
        obj = {
            "name": METADATA_NAME + " #" + str(i),
            "symbol": METADATA_SYMBOL,
            "description": METADATA_DESCRIPTION,
            "image": METADATA_IMAGE_URL + str(i) + ".png",
            "external_url": METADATA_EXTERNAL_URL + str(i),
            "attributes": adict["attributes"]
        }
        with open(OUTPUTS_DIR + str(i) + ".json", 'w') as outjson:
            json.dump(obj, outjson, indent=4)

        print("Generated metadata id: {}\n".format(i))

    print("Done.")


main()