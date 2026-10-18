import bpy
import os

GROUPS = ("Unravel Tears", "Unravel Threads", "Unravel Strand", "Unravel Thread Mesh")

here = os.path.dirname(os.path.abspath(__file__))
target = os.path.normpath(os.path.join(here, "..", "unravel", "assets", "unravel_nodes.blend"))
os.makedirs(os.path.dirname(target), exist_ok=True)

blocks = {bpy.data.node_groups[name] for name in GROUPS}
bpy.data.libraries.write(target, blocks, fake_user=True)
print("Saved", len(blocks), "node groups to", target)