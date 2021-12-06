import json
from os import path
import random
import re
import shutil


#  --- Settings -----------------------------------------------------------------------------------------

# Total number of characters generated
TOTAL_CHARACTERS = 4

# An absolute path for the root directory
PROJECT_DIR = "c:/nft-collectibles-blender-python/"

# Output directory to where all metadata files generated
OUTPUTS_DIR = PROJECT_DIR + "outputs/"

# Metadata JSON structure - Please see https://docs.opensea.io/docs/metadata-standards
METADATA_NAME = "NFT Character"
METADATA_SYMBOL = ""
METADATA_DESCRIPTION = "NFT Collectibles using Blender Python"
METADATA_IMAGE_BASE_URL = "https://example.com/"
METADATA_EXTERNAL_URL = "https://example.com/"

# List - One item will be selected for each list
list_bg = [
    "green", "navy", "red", "yellow"
]
list_body = [
    "shirt", "tanktop", "zombie"
]
list_head = [
    "devil", "dragon", "frog", "pixel", "warrior"
]
# -------------------------------------------------------------------------------------------------------


def rand_attributes(id):
    # Rarity
    rarity = random.randint(0, 499)

    rand_head = random.choice(list_head)

    rand_body = random.choice(list_body)

    # Format
    rand_body = rand_body.replace("_", " ").title()
    rand_head = rand_head.replace("_", " ").title()

    attributes = [
        {
            "trait_type": "Body",
            "value": rand_body
        },
        {
            "trait_type": "Head",
            "value": rand_head
        }
    ]

    return attributes


def rand_attr_bg():
    rand_bg = random.choice(list_bg).title()

    attr = {
        "trait_type": "Background",
        "value": rand_bg
    }

    return attr


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
        print("ERROR: Properties duplicate.")
        return
    # Add background to attribute
    for u in unique_list:
        u["attributes"].append(rand_attr_bg())

    json_data = {}

    for i, adict in enumerate(unique_list):
        # Create metadata
        obj = {
            "name": METADATA_NAME + " #" + str(i),
            "symbol": METADATA_SYMBOL,
            "description": METADATA_DESCRIPTION,
            "image": METADATA_IMAGE_BASE_URL + str(i) + ".png",
            "external_url": METADATA_EXTERNAL_URL + str(i),
            "attributes": adict["attributes"]
        }
        with open(OUTPUTS_DIR + str(i) + ".json", 'w') as outjson:
            json.dump(obj, outjson, indent=4)

        print("Generated metadata id: {}\n".format(i))

    print("Done.")


main()