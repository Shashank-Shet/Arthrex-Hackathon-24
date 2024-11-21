import cv2
import matplotlib.pyplot as plt
import numpy as np
from argparse import ArgumentParser

# Final image dims
SIZE = 400, 400

parser = ArgumentParser()
parser.add_argument("normal", type=str, help="Path to ref normal xray")
parser.add_argument("problem", type=str, help="Path to ref problem xray")
parser.add_argument("test", type=str, help="Path to test xray")
parser.add_argument("output_fpath", type=str)


def concatenate_images(im_normal: np.ndarray, im_problem: np.ndarray, im_test: np.ndarray):
    fig, axs = plt.subplot_mosaic([
        ["normal", "problem", "test",],
    ], gridspec_kw={'hspace': 0.3})
    axs['normal'].axis('off')
    axs['normal'].imshow(im_normal)
    axs['normal'].set_title("Reference XRay 1")

    axs['problem'].axis('off')
    axs['problem'].imshow(im_problem)
    axs['problem'].set_title("Reference XRay 2")

    axs['test'].axis('off')
    axs['test'].imshow(im_test)
    axs['test'].set_title("Test XRay")

    return fig, axs


if __name__ == '__main__':
    args = parser.parse_args()
    im_normal = cv2.imread(args.normal)
    im_problem = cv2.imread(args.problem)
    im_test = cv2.imread(args.test)

    im_normal = cv2.resize(im_normal, SIZE)
    im_problem = cv2.resize(im_problem, SIZE)
    im_test = cv2.resize(im_test, SIZE)

    fig, axs = concatenate_images(im_normal, im_problem, im_test)
    fig.savefig(args.output_fpath, bbox_inches='tight', pad_inches=0.1)

