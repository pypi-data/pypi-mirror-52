#
# COPYRIGHT
#
# All contributions by Thorsten Wagner:
# Copyright (c) 2017 - 2019, Thorsten Wagner.
# All rights reserved.
#
# ---------------------------------------------------------------------------
#         Do not reproduce or redistribute, in whole or in part.
#      Use of this code is permitted only under licence from Max Planck Society.
#            Contact us at thorsten.wagner@mpi-dortmund.mpg.de
# ---------------------------------------------------------------------------
#

import sys


def get_number_patches(config):
    """
    Returns the number of patches in config file.
    :param config: config dictionary
    :return: Number of patches
    """
    if "num_patches" in config["model"]:
        num_patches = config["model"]["num_patches"]
    else:
        num_patches = 1
        print("Set patch_size to 1 (default)")

    return num_patches


def get_gridcell_dimensions(config):
    """
    Returns the grid cell dimension in dependence of the use network.
    :param config: config dictionary
    :return: grid cell dimensions
    """
    if config["model"]["architecture"] == "YOLO":
        downsampling_factor = 32.0
    elif (
        config["model"]["architecture"] == "crYOLO"
        or config["model"]["architecture"] == "PhosaurusNet"
    ):
        downsampling_factor = 16.0
    else:
        raise Exception(
            "Architecture not supported! "
            "Only support for PhosaurusNet, YOLO and crYOLO at the moment!"
        )

    grid_w = config["model"]["input_size"] / downsampling_factor
    grid_h = config["model"]["input_size"] / downsampling_factor

    return grid_w, grid_h


def get_box_size(config):
    """
    Read the box size from the config.

    :param config:
    :return: Box size
    """
    if "particle_diameter" in config["model"]:
        box_height = config["model"]["particle_diameter"]
        box_width = config["model"]["particle_diameter"]
    elif len(config["model"]["anchors"]) == 2:
        box_height, box_width = config["model"]["anchors"]
    else:
        sys.exit("You have to specify the 'particle_diameter' in your config. Stop.")
    return box_width, box_height
