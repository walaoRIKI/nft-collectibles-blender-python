import bpy
import glob
import json
from os import path
import random
import shutil

# An absolute path for the root directory
PROJECT_DIR = "/Users/teoh/Desktop/nft-collectibles-blender-python/"

# Parts directory containing each directory like "body" or "head" or "misc"
PARTS_DIR = PROJECT_DIR + "parts/"

def main():
    bg_Name = "bg13"

    path = PARTS_DIR + "background/" + bg_Name +".jpg"
    mat = bpy.data.materials["Background"]
    nodes = mat.node_tree.nodes
    img_node = nodes.get("Image Texture")
    if img_node:
        print("Success Get")
        img_node.image = bpy.data.images.load(path)
        print("Path " + path)

main()