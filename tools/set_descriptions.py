import bpy

DESCRIPTIONS = {
    "Unravel Tears": {
        "Mask": "Name of the vertex group that marks where the cloth tears",
        "Hole Size": "How far the holes eat into the painted area. 0 means no holes",
        "Edge Noise": "How ragged the torn edges are",
        "Noise Scale": "Size of the ragged bits along the edge. Higher means smaller, busier bits",
        "Detail": "Extra subdivision for finer edges. Each step makes the cloth about 4 times heavier",
        "Seed": "Changes the random raggedness without changing your paint",
        "Thickness": "How thick the cloth looks at its torn edges. Eases off on tight curves so the edge can't fold through itself",
        "Lip Width": "How far the thick edge reaches from the hole before fading back to thin cloth",
        "Whole Cloth": "Make the entire cloth solid instead of only thickening around the holes",
        "Edge Smoothing": "Smooths the stepped outline of each hole. 0 keeps the raw edge",
        "Scale": "Size of the cloth compared to real life. Set from the Unravel tab",
        "Holes Baked": "Set by Bake Tears. On means the holes are already in the mesh and only the thickness is added",
    },
    "Unravel Threads": {
        "Cloth": "The torn cloth these threads grow from",
        "UV Map": "UV map that gives the weave direction. Threads follow it when Flow is below 1",
        "Density": "Threads per metre of torn edge",
        "Length": "Longest thread length",
        "Root Width": "Thread thickness where it leaves the cloth. Shows in Material Preview and Rendered view. Up to 2 cm",
        "Tip Width": "Thread thickness at its loose end. Shows in Material Preview and Rendered view. Up to 2 cm",
        "Resolution": "Points along each thread. More gives smoother curls but heavier scenes",
        "Seed": "Changes the random look of the threads",
        "Length Random": "How much shorter some threads are. 0 makes them all full length",
        "Clumping": "1 gathers thread tips into bunches, -1 gathers roots into tufts that fan out like grass, 0 is off",
        "Curl Radius": "How far threads curl around their own direction",
        "Curl Turns": "How many curls each thread makes along its length",
        "Frizz": "Small random wiggles along each thread",
        "Droop": "How much threads sag under their own weight",
        "Surface Contact": "Keep threads from sinking into the cloth",
        "Contact Offset": "How high above the cloth surface threads are kept",
        "Contact Depth": "Threads deeper than this below the cloth are left alone, so they can hang behind it",
        "Viewport Density": "Share of threads shown in the viewport. Renders always show all of them",
        "Material": "Material used by these threads",
        "Direction Random": "Tilts threads by a random angle. 0 keeps them neatly aligned",
        "Flow": "0 follows the weave of the cloth, 1 points threads into the hole",
        "Aim": "Across Edge points each thread straight into the hole from where it grows. Toward Centre points threads at the middle of their hole",
        "Follow Curvature": "Bend threads along the surface the cloth would have had, instead of straight out",
        "Stay in Hole": "Shorten threads that would reach past the far side of their hole",
        "Frizz Waves": "How many big wiggles each thread makes. Low gives lazy bends, high gives tight frizz",
        "Bridges": "Share of threads that stay connected across narrow gaps. 0 means none",
        "Bridge Gap": "Widest gap a thread can bridge. Narrower gaps get more bridges",
        "Bridge Sag": "How much bridging threads sag in the middle",
        "Scale": "Size of the cloth compared to real life. Set from the Unravel tab",
    },
    "Unravel Strand": {
        "Path": "The curve this strand follows",
        "Fibers": "Number of fibres twisted together in the strand",
        "Fiber Spread": "Distance of each fibre from the centre of the strand",
        "Twist": "Turns the fibres make around each other per metre",
        "Tip Flare": "How much the fibres splay apart toward the end of the strand",
        "Root Width": "Fibre thickness at the start of the strand. Shows in Material Preview and Rendered view. Up to 2 cm",
        "Tip Width": "Fibre thickness at the end of the strand. Shows in Material Preview and Rendered view. Up to 2 cm",
        "Curl Radius": "How far the whole strand spirals around the drawn path",
        "Curl Turns": "How many spirals the strand makes along its length",
        "Frizz": "Small random wiggles along each fibre",
        "Point Spacing": "Distance between points along the strand. Smaller is smoother but heavier",
        "Seed": "Changes the random look of the strand",
        "Material": "Material used by this strand",
        "Scale": "Size of the cloth compared to real life. Set from the Unravel tab",
        "Cloth": "The cloth this strand lies on. The strand follows it when it moves or simulates",
    },
    "Unravel Thread Mesh": {
        "Threads": "The threads object to turn into mesh tubes",
        "Sides": "Sides around each thread tube. 3 is lightest",
        "Detail": "Share of points kept along each thread. Lower is lighter",
        "UV Map": "UV map name to store on the tubes, so the cloth colour carries over",
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