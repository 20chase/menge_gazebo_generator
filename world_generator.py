import os

import numpy as np

from lxml import etree as et
from scene_reader import SceneReader


class WorldGenerator(object):
    def __init__(self, scene_name, resolution=0.1):
        self.scene_name = scene_name
        self.resolution = resolution

        reader = SceneReader(self.scene_name)
        self.all_geos = reader.run()

    def base_generate(self):
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

        return sdf, world

    def generate_wall(self, scene, idx, geos):
        link_name = "Wall_{}".format(idx)
        link = et.SubElement(
            scene, "link", name=link_name
            )
        pose = et.SubElement(link, "pose", frame='')
        pose.text = "{} {} 0 0 0 0".format(
            self.resolution*geos[0], self.resolution*geos[1]
            )

        collision = et.SubElement(
            link, "collision", name=link_name + "_collision"
        )
        pose = et.SubElement(collision, "pose", frame='')
        pose.text = "0 0 1.25 0 0 0"
        geo_collision = et.SubElement(collision, "geometry")
        box = et.SubElement(geo_collision, "box")
        size = et.SubElement(box, "size")
        size.text = "{} {} 2.5".format(
            self.resolution*geos[2], self.resolution*geos[3]
            )

        visual = et.SubElement(
            link, "visual", name=link_name + "_visual"
        )
        pose = et.SubElement(visual, "pose", frame='')
        pose.text = "0 0 1.25 0 0 0"
        geo_visual = et.SubElement(visual, "geometry")
        box = et.SubElement(geo_visual, "box")
        size = et.SubElement(box, "size")
        size.text = "{} {} 2.5".format(
            self.resolution*geos[2], self.resolution*geos[3]
            )
        material = et.SubElement(visual, "material")
        script = et.SubElement(material, "script")
        uri = et.SubElement(script, "uri")
        uri.text = "file://media/materials/scripts/gazebo.material"
        name = et.SubElement(script, "name")
        name.text = "Gazebo/Grey"
        ambient = et.SubElement(material, "ambient")
        ambient.text = "1 1 1 1"

        self_collide = et.SubElement(link, "self_collide")
        self_collide.text = "0"
        enable_wind = et.SubElement(link, "enable_wind")
        enable_wind.text = "0"
        kinematic = et.SubElement(link, "kinematic")
        kinematic.text = "0"

        return scene

    def generate(self, 
                 write_plugin=False):
        
        sdf, world = self.base_generate()
        scene = et.SubElement(
            world, "model", name=self.scene_name
        )
        static = et.SubElement(scene, "static")
        static.text = "1"

        for i, geos in enumerate(self.all_geos):
            if i == 0:
                pose = et.SubElement(scene, "pose", frame='')
                pose.text = "{} {} 0 0 0 0".format(
                    -self.resolution*geos[0], -self.resolution*geos[1]
                    )
                continue
            scene = self.generate_wall(scene, i, geos)

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
            "./{0}/{0}.world".format(self.scene_name), 
            pretty_print=True, 
            xml_declaration=False
        )


if __name__ == "__main__":
    generator = WorldGenerator("CrossStreet")
    generator.generate()

