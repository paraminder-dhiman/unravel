import bpy

DESCRIPTIONS = {
    "Unravel Tears": {
        "Mask": "Name of the vertex group that marks where the cloth tears",
        "Hole Size": "How far the holes eat into the painted area. 0 means no holes",
        "Edge Noise": "How ragged the torn edges are",
        "Noise Scale": "Size of the ragged bits along the edge. Higher means smaller, busier bits",
        "Detail": "Extra subdivision for finer edges. Each step makes the cloth about 4 times heavier",
        "Seed": "Changes the random raggedness without changing your paint",
        "Thickness": "How thick the cloth looks at its torn edges",
        "Lip Width": "How far the thick edge reaches from the hole before fading back to thin cloth",
        "Whole Cloth": "Make the entire cloth solid instead of only thickening around the holes",
    },
    "Unravel Threads": {
        "Cloth": "The torn cloth these threads grow from",
        "UV Map": "UV map that gives the weave direction. Threads follow it",
        "Density": "Threads per metre of torn edge",
        "Length": "Longest thread length",
        "Root Width": "Thread thickness where it leaves the cloth",
        "Tip Width": "Thread thickness at its loose end",
        "Resolution": "Points along each thread. More gives smoother curls but heavier scenes",
        "Seed": "Changes the random look of the threads",
        "Length Random": "How much shorter some threads are. 0 makes them all full length",
        "Clumping": "How much thread tips gather into small bunches",
        "Curl Radius": "How far threads curl around their own direction",
        "Curl Turns": "How many curls each thread makes along its length",
        "Frizz": "Small random wiggles along each thread",
        "Droop": "How much threads sag under their own weight",
        "Surface Contact": "Keep threads from sinking into the cloth",
        "Contact Offset": "How high above the cloth surface threads are kept",
        "Contact Depth": "Threads deeper than this below the cloth are left alone, so they can hang behind it",
        "Viewport Density": "Share of threads shown in the viewport. Renders always show all of them",
        "Material": "Material used by these threads",
    },
    "Unravel Strand": {
        "Path": "The curve this strand follows",
        "Fibers": "Number of fibres twisted together in the strand",
        "Fiber Spread": "Distance of each fibre from the centre of the strand",
        "Twist": "Turns the fibres make around each other per metre",
        "Tip Flare": "How much the fibres splay apart toward the end of the strand",
        "Root Width": "Fibre thickness at the start of the strand",
        "Tip Width": "Fibre thickness at the end of the strand",
        "Curl Radius": "How far the whole strand spirals around the drawn path",
        "Curl Turns": "How many spirals the strand makes along its length",
        "Frizz": "Small random wiggles along each fibre",
        "Point Spacing": "Distance between points along the strand. Smaller is smoother but heavier",
        "Seed": "Changes the random look of the strand",
        "Material": "Material used by this strand",
    },
}

for group_name, descriptions in DESCRIPTIONS.items():
    group = bpy.data.node_groups[group_name]
    for item in group.interface.items_tree:
        if item.item_type == 'SOCKET' and item.in_out == 'INPUT' and item.name in descriptions:
            item.description = descriptions[item.name]
    print("Described", group_name)

bpy.ops.wm.save_mainfile()
print("Saved", bpy.data.filepath)