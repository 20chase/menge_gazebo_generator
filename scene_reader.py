import os

import numpy as np

from lxml import etree as et


class SceneReader(object):
    def __init__(self, scene_name):
        parser = et.XMLParser(remove_blank_text=True)
        self.tree = et.parse(
            "{0}/output/{1}/{1}S.xml".format(os.getcwd(), scene_name),
            parser
        )

    def find_all_pts(self):
        all_pts = []
        for obst in self.tree.getroot().getchildren()[8]:
            pts = [
                np.array(
                    [vertex.get("p_x"), vertex.get("p_y")], dtype=float
                    ) \
                for vertex in obst
                ]
            all_pts.append(np.array(pts))
        return all_pts 

    def run(self):
        all_pts = self.find_all_pts()
        all_geos = []
        for pts in all_pts:
            center = np.mean(pts, axis=0)
            width = abs(pts[1, 0] - pts[0, 0])
            height = abs(pts[2, 1] - pts[1, 1])
            all_geos.append(
                [center[0], center[1], width, height]
            )
        return all_geos
            
if __name__ == "__main__":
    reader = SceneReader("CrossStreet")
    print reader.run()