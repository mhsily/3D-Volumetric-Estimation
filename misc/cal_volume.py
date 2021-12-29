from pyntcloud import PyntCloud
diamond = PyntCloud.from_file("/home/shubbu/Desktop/3d_Estimations/point-cloud/complete.ply")
convex_hull_id = diamond.add_structure("convex_hull")
convex_hull = diamond.structures[convex_hull_id]
volume = convex_hull.volume



print(volume)