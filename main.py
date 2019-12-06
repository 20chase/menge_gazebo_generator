import argparse
import subprocess
import os

parser = argparse.ArgumentParser()
parser.add_argument("path", help="path to the scenario XML file")
args = parser.parse_args()

scene_name = args.path.split('/')[-1][:-4] 
cwd = os.getcwd()
output_dir = cwd + "/output/" + scene_name 

os.chdir("MengeFileGenerator")
os.system("python menge_generator.py {} -o {}".format(
    args.path, output_dir
))
os.chdir(cwd)

os.system("python world_generator.py --scene_name {}".format(
    scene_name
))




