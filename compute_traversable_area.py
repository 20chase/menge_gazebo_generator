import imageio

import numpy as np


class TraversableAreaComputer(object):
    def __init__(self, image_path):
        self.src_img = imageio.imread(image_path)

    def run(self):
        traverible_area = 0
        for i in range(self.src_img.shape[0]):
            for j in range(self.src_img.shape[1]): 
                if np.sum(self.src_img[i, j, :]) == 765:
                    traverible_area += 1

        print("rate: ", float(traverible_area) / (self.src_img.size / 3))


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "path", type=str
        )
    args = parser.parse_args()

    computer = TraversableAreaComputer(args.path)
    computer.run()