import bpy
import glob
import json
from os import path
import random
import shutil


# ----------- Settings -----------------------------------------------------------

# An absolute path for the root directory
PROJECT_DIR = "/Users/teoh/Desktop/nft-collectibles-blender-python/"

# Parts directory containing each directory like "body" or "head" or "misc"
PARTS_DIR = PROJECT_DIR + "parts/"

# Output directory to where all metadata files generated
OUTPUTS_DIR = PROJECT_DIR + "outputs/"
# --------------------------------------------------------------------------------


# Initialize the scene
def init():
    for obj in bpy.data.objects:
        bpy.data.objects.remove(obj)
    for col in bpy.data.collections:
        bpy.data.collections.remove(col)


# Set render config
def set_render_config():

    r = bpy.context.scene.render
    r.engine = "BLENDER_EEVEE"
    r.resolution_x = 1024
    r.resolution_y = 1024

    # File format
    r.image_settings.file_format = 'PNG'

    # Bloom (optional)
    bpy.context.scene.eevee.use_bloom = True
    bpy.context.scene.eevee.bloom_threshold = 3.0
    bpy.context.scene.eevee.bloom_knee = 0.5
    bpy.context.scene.eevee.bloom_radius = 2.0
    bpy.context.scene.eevee.bloom_intensity = 0.1
    bpy.context.scene.eevee.bloom_color = (1.0, 1.0, 1.0)
    bpy.context.scene.eevee.bloom_clamp = 0.0


def append_asset_misc():
    path = PARTS_DIR + "misc/" + "misc.blend/Collection/"
    object_name = "misc"
    bpy.ops.wm.append(filename=object_name, directory=path)

    # Link camera to scene
    cam = bpy.data.objects["camera"]
    scene = bpy.context.scene
    scene.camera = cam

def append_asset_body(t):
    body_type = mat_type = "body " + t

    path = PARTS_DIR + "body/" + body_type + ".blend/Collection/"
    bpy.ops.wm.append(filename=body_type, directory=path)

    body_col = bpy.data.collections[body_type]

def append_asset_head(t):
    head_type = mat_type = "head " + t

    path = PARTS_DIR + "head/" + head_type + ".blend/Collection/"
    bpy.ops.wm.append(filename=head_type, directory=path)

    head_col = bpy.data.collections[head_type]

def append_asset_hand(t):
    hand_type = mat_type = "hand " + t

    path = PARTS_DIR + "hand/" + hand_type + ".blend/Collection/"
    bpy.ops.wm.append(filename=hand_type, directory=path)

    hand_col = bpy.data.collections[hand_type]

def append_asset_leg(t):
    leg_type = mat_type = "leg " + t

    path = PARTS_DIR + "leg/" + leg_type + ".blend/Collection/"
    bpy.ops.wm.append(filename=leg_type, directory=path)

    leg_col = bpy.data.collections[leg_type]

#Insert the background blender
def append_asset_bg():
    bg_type = mat_type = "background"

    path = PARTS_DIR + "background/" + bg_type +".blend/Collection/"
    bpy.ops.wm.append(filename=bg_type, directory=path)

    bg_col = bpy.data.collections[bg_type]

#Change the background image
def background_ChangeImage(t):
    bg_Name = t

    path = PARTS_DIR + "background/" + bg_Name +".jpg"
    mat = bpy.data.materials["Background"]
    nodes = mat.node_tree.nodes
    img_node = nodes.get("Image Texture")
    if img_node:
        print("Success Get")
        img_node.image = bpy.data.images.load(path)
        print("Path " + path)

def render(id):
    # Render
    bpy.ops.render.render(write_still=1)

    # Save
    bpy.data.images['Render Result'].save_render(filepath=OUTPUTS_DIR + id + ".png")


def remove_assets():
    for col in bpy.data.collections:
        if col.name != "misc" and col.name != "background":
            for obj in col.objects:
                bpy.data.objects.remove(obj)
            bpy.data.collections.remove(col)
            continue


def generate(id, adict):
    for attr in adict["attributes"]:
        print(attr["trait_type"])
        # Body
        if attr["trait_type"] == "Body" and attr["value"] != "":
            append_asset_body(attr["value"])
        # Head
        if attr["trait_type"] == "Head" and attr["value"] != "":
            append_asset_head(attr["value"])
        # Head
        if attr["trait_type"] == "Hand" and attr["value"] != "":
            append_asset_hand(attr["value"])
            # Head
        if attr["trait_type"] == "Leg" and attr["value"] != "":
            append_asset_leg(attr["value"])
        if attr["trait_type"] == "bg" and attr["value"] != "":
            background_ChangeImage(attr["value"])

    render(str(id))
    remove_assets()
    print("Generated model id: {}\n".format(id))


def main():
    # Check settings
    if path.exists(PROJECT_DIR) == False:
        print("ERROR: Project directory does not exist. Set the absolute path to the PROJECT_DIR.")
        return
    if path.exists(OUTPUTS_DIR) == False:
        print("ERROR: Outputs directory does not exist. Set the absolute path to the OUTPUTS_DIR.")
        return

    print("Start generating models...")

    # Initialize
    init()
    set_render_config()
    append_asset_misc()
    append_asset_bg()

    # Get all metadata files in "outputs" directory
    metadata_files = glob.glob(OUTPUTS_DIR + "/*.json")
    # Generate models
    for i, metadata in enumerate(metadata_files):
        with open(metadata, 'r') as metaJson:
            data = json.load(metaJson)
            generate(i, data)

    print("Done.")

main()