# Menge Gazebo Generator

## Install
git clone include submodules
``` shell
git submodule update --init --recursive
```

## Usage

Here is a example to use it. 
``` shell
python main.py ./example/CrossStreet.xml -r $RESOLUTION
```

The result will be generated in output directory. 


## How to generate input file

1. Install painting tools.
``` shell
sudo apt-get install gimp
```

2. Paint a wall map and a behavior map.
``` shell
gimp
```

3. Write a xml file for above maps. For xml defination details, you can refer the README.md file in MengeFileGenerator. 

