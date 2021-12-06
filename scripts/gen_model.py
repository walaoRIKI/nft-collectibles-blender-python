import bpy
import glob
import json
from os import path
import random
import shutil


# ----------- Settings -----------------------------------------------------------

# An absolute path for the root directory
PROJECT_DIR = "c:/nft-collectibles-blender-python/"

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


def assign_bg_material(mat_type):
    bg = bpy.data.objects["bg"]
    mat = bpy.data.materials.get(mat_type)

    # Assign material
    bg.data.materials[0] = mat


def append_asset_body(t):
    body_type = mat_type = "body_" + t

    path = PARTS_DIR + "body/" + body_type + ".blend/Collection/"
    bpy.ops.wm.append(filename=body_type, directory=path)

    body_col = bpy.data.collections[body_type]


def append_asset_head(t):
    head_type = mat_type = "head_" + t

    path = PARTS_DIR + "head/" + head_type + ".blend/Collection/"
    bpy.ops.wm.append(filename=head_type, directory=path)

    head_col = bpy.data.collections[head_type]


def render(id):
    # Render
    bpy.ops.render.render(write_still=1)

    # Save
    bpy.data.images['Render Result'].save_render(filepath=OUTPUTS_DIR + id + ".png")


def remove_assets():
    for col in bpy.data.collections:
        if col.name != "misc":
            for obj in col.objects:
                bpy.data.objects.remove(obj)
            bpy.data.collections.remove(col)
            continue


def generate(id, adict):
    for attr in adict["attributes"]:
        # Background
        if attr["trait_type"] == "Background" and attr["value"] != "":
            assign_bg_material("bg_" + attr["value"].lower())
        # Body
        if attr["trait_type"] == "Body" and attr["value"] != "":
            append_asset_body(attr["value"].replace(" ", "_").lower())
        # Head
        if attr["trait_type"] == "Head" and attr["value"] != "":
            append_asset_head(attr["value"].replace(" ", "_").lower())

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

    # Get all metadata files in "outputs" directory
    metadata_files = glob.glob(OUTPUTS_DIR + "/*.json")
    # Generate models
    for i, metadata in enumerate(metadata_files):
        with open(metadata, 'r') as metaJson:
            data = json.load(metaJson)
            generate(i, data)

    print("Done.")

main()