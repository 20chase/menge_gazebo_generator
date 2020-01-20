import os

import numpy as np

from lxml import etree as et


class SceneReader(object):
    def __init__(self, scene_name):
        self.scene_name = scene_name
        parser = et.XMLParser(remove_blank_text=True)
        self.tree = et.parse(
            "{0}/output/{1}/{1}S.xml".format(os.getcwd(), scene_name),
            parser
        )

    def find_all_pts(self):
        for i in range(len(self.tree.getroot().getchildren())):
            if self.tree.getroot().getchildren()[i].tag == "ObstacleSet":
                obst_idx = i
                break
        all_pts = []
        for obst in self.tree.getroot().getchildren()[obst_idx]:
            pts = [
                np.array(
                    [vertex.get("p_x"), vertex.get("p_y")], dtype=float
                    ) \
                for vertex in obst
                ]
            all_pts.append(np.array(pts))
        return all_pts

    def remove_obstacle_nodes(self):
        for i in range(len(self.tree.getroot().getchildren())):
            if self.tree.getroot().getchildren()[i].tag == "ObstacleSet":
                obst_idx = i
                break
        
        for i, obst in enumerate(self.tree.getroot().getchildren()[obst_idx]):
            if i == 0:
                continue
            self.tree.getroot().getchildren()[obst_idx].remove(obst)

        self.tree.write(
            "./output/{0}/{0}S.xml".format(self.scene_name), 
            pretty_print=True, 
            xml_declaration=True
        )
        print("Remove obstacle nodes in {}S.xml".format(self.scene_name))

    def run(self):
        all_pts = self.find_all_pts()
        all_geos = []
        for pts in all_pts:
            center = np.mean(pts, axis=0)
            width = abs(pts[1, 0] - pts[0, 0])
            height = abs(pts[2, 1] - pts[1, 1])
            all_geos.append(
                [center[0], center[1], width, height]
                # [pts[0, 0], pts[0, 1], width, height]
            )
        return all_geos
            
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--scene_name", default="CrossStreet", type=str
        )
    args = parser.parse_args()
    reader = SceneReader(args.scene_name)
    reader.run()