import os
# import imageio
import cv2

import numpy as np

from lxml import etree as et


class WorldGenerator(object):
    def __init__(self, wall_png):
        self.scene_name = wall_png.split('/')[-1][:-9]

        self.wall_png = os.getcwd() + wall_png
        img = cv2.imread(self.wall_png)
        img = 255 - img
        img = cv2.resize(img, (129, 129))
        cv2.imwrite(
            "./{}/heightmap.png".format(self.scene_name),
            img
        )
        self.wall_size = img.shape[0]

    def generate(self, 
                 write_plugin=False):
        sdf = et.Element("sdf", version="1.6")
        world = et.SubElement(
            sdf, "world", name="default"
        )

        gravity = et.SubElement(world, "gravity")
        gravity.text = "0 0 -0.98"

        et.SubElement(
            world, "atmosphere", type='adiabatic'
        )
        physics = et.SubElement(
            world, "physics", 
            name='default_physics',
            default='0', 
            type='ode'
        )
        max_step_size = et.SubElement(physics, "max_step_size")
        max_step_size.text = "0.001"
        
        real_time_factor = et.SubElement(physics, "real_time_factor")
        real_time_factor.text = "1"

        real_time_update_rate = et.SubElement(physics, "real_time_update_rate")
        real_time_update_rate.text = "1000"

        include = et.SubElement(world, "include")
        uri = et.SubElement(include, "uri")
        uri.text = "model://sun"
        
        scene = et.SubElement(
            world, "model", name=self.scene_name
        )
        static = et.SubElement(scene, "static")
        static.text = "1"
        
        link = et.SubElement(
            scene, "link", name="link"
        )
        collision = et.SubElement(
            link, "collision", name="collision"
        )
        geo_collision = et.SubElement(
            collision, "geometry"
        )
        heightmap = et.SubElement(
            geo_collision, "heightmap"
        )
        
        uri = et.SubElement(
            heightmap, "uri"
        )
        uri.text = "file://" + os.getcwd() + "/" + self.scene_name + "/heightmap.png"
        
        size = et.SubElement(
            heightmap, "size"
        )
        size.text = "1 1 1"

        visual = et.SubElement(
            link, "visual", name="visual"
        )
        geo_visual = et.SubElement(
            visual, "geometry"
        )
        
        heightmap_visual = et.SubElement(
            geo_visual, "heightmap"
        )
        uri = et.SubElement(heightmap_visual, "uri")
        uri.text = "file://" + os.getcwd() + "/" + self.scene_name + "/heightmap.png"

        size = et.SubElement(heightmap_visual, "size")
        size.text = "{0} {0} 30".format(self.wall_size)

        if write_plugin:
            plugin = et.SubElement(
                world, "plugin", 
                name="menge_plugin_randomized", 
                filename="libmenge_plugin_randomized.so"
            )
            menge_root = et.SubElement(
                plugin, "menge_root"
                )
            menge_root.text = "/home/micrl/menge_ws/Menge"

            menge_project_file = et.SubElement(
                plugin, "menge_project_file"
                )
            menge_project_file.text = "example/" + self.scene_name + ".xml"

            perception_distance = et.SubElement(
                plugin, "perception_distance"
                )
            perception_distance.text = "5.0"

        tree = et.ElementTree(sdf)
        tree.write(
            self.scene_name + ".world", 
            pretty_print=True, 
            xml_declaration=False
        )


if __name__ == "__main__":
    generator = WorldGenerator(
        "/example/CrossStreetWalls.png"
    )
    generator.generate()

