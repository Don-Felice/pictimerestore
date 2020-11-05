# -*- coding: utf-8 -*-
# FSegerer 04112020

# Backup folders and files

# external imports
import argparse

# project intern imports
from pictimerestore.utils import get_filelist
from pictimerestore.utils import change_date_from_name


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("dir_images", type=str,
                        help="number of images to be taken")
    parser.add_argument("-r", "--recursive", action='store_true', default=False,
                        help="look for images recursively")

    args = parser.parse_args()

    # start

    list_imgs = get_filelist(args.dir_images, recursive=args.recursive)

    for file in list_imgs:
        change_date_from_name(file)