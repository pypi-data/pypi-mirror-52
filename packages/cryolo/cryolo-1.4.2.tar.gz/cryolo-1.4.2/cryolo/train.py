#! /usr/bin/env python

#
# COPYRIGHT
#
# All contributions by Ngoc Anh Huyn:
# Copyright (c) 2017, Ngoc Anh Huyn.
# All rights reserved.
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

from __future__ import print_function

import argparse
import json
import multiprocessing
import os
import time

import numpy as np

import cryolo.config_tools as config_tools
import cryolo.imagereader as imagereader
import cryolo.lowpass as lowpass
from cryolo.preprocessing import parse_annotation2
from . import utils


os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
try:
    os.environ["CUDA_VISIBLE_DEVICES"]
except KeyError:
    os.environ["CUDA_VISIBLE_DEVICES"] = "0"
os.environ["HDF5_USE_FILE_LOCKING"] = "FALSE"

argparser = argparse.ArgumentParser(
    description="Train crYOLO model on any dataset",
    formatter_class=argparse.ArgumentDefaultsHelpFormatter,
)

argparser.add_argument("-c", "--conf", required=True, help="path to configuration file")

argparser.add_argument(
    "-w",
    "--warmup",
    type=int,
    default=None,
    help="Number of warmup epochs. If none, it tries to read it from the config file. If it is not defined in the "
    "config file, it is set to 0.",
)

argparser.add_argument(
    "-nc",
    "--num_cpu",
    type=int,
    default=-1,
    help="Number of CPUs used during training. By default it will use half of the available CPUs.",
)

argparser.add_argument(
    "-p",
    "--patch",
    default=None,
    type=int,
    help="Number of patches. If none, it tries to read it from the config file. If it is not defined in the "
    "config file, it is set to 1.",
)

argparser.add_argument(
    "-e",
    "--early",
    default=10,
    type=int,
    help="Early stop patience. If the validation loss did not improve longer than the early stop patience, "
    "the training is stopped.",
)

argparser.add_argument("--exp_loss", help=argparse.SUPPRESS, action="store_true")

argparser.add_argument(
    "-g",
    "--gpu",
    default=-1,
    nargs="+",
    help="Specifiy which gpu(s) should be used. Multiple GPUs are separated by a whitespace",
)

argparser.add_argument(
    "--warm_restarts",
    action="store_true",
    help="Use warm restarts and cosine annealing during training",
)

argparser.add_argument(
    "--skip_augmentation",
    action="store_true",
    default=False,
    help="Use it if you want to deactivate data augmentation during training.",
)

argparser.add_argument(
    "--fine_tune",
    action="store_true",
    default=False,
    help="Set it to true if you only want to use the fine tune mode.",
)

argparser.add_argument(
    "--gpu_fraction",
    type=float,
    default=1.0,
    help="Specify the fraction of memory per GPU used by crYOLO during training. Only values between 0.0 and 1.0 are allowed.",
)

argparser.add_argument(
    "--seed",
    type=int,
    default=10,
    help="Seed for random number generator. Mainly influences selection of validation images. Should be the same during different training runs!",
)


def _main_():
    try:
        multiprocessing.set_start_method("spawn")
    except RuntimeError:
        print("Ignore set start method")

    args = argparser.parse_args()

    if isinstance(args.gpu, list):
        if len(args.gpu) == 1:
            str_gpus = args.gpu[0].strip().split(" ")
        else:
            str_gpus = [str(entry) for entry in args.gpu]
        num_gpus = len(str_gpus)
        os.environ["CUDA_VISIBLE_DEVICES"] = ",".join(str_gpus)
    else:
        num_gpus = 1
        if args.gpu != -1:
            str_gpus = str(args.gpu)
            os.environ["CUDA_VISIBLE_DEVICES"] = ",".join(str_gpus)

    if args.gpu_fraction < 1.0 and args.gpu_fraction > 0.0:
        import tensorflow as tf
        from keras.backend.tensorflow_backend import set_session
        import keras.backend.tensorflow_backend as k

        print("AVAIL", k._get_available_gpus())

        config = tf.ConfigProto()

        config.gpu_options.per_process_gpu_memory_fraction = args.gpu_fraction

        set_session(tf.Session(config=config))

    config_path = args.conf
    with open(config_path) as config_buffer:
        try:
            config = json.loads(config_buffer.read())
        except json.JSONDecodeError:
            print(
                "Your configuration file seems to be corruped. Please check if it is valid."
            )
        if config["model"]["input_size"] % 32 > 0:
            new_input_size = int(32 * round(float(config["model"]["input_size"]) / 32))
            print("You input size is not a multiple of 32. Round it to the next multiple of 32:", new_input_size)
            config["model"]["input_size"] = new_input_size

    if args.patch is not None:
        num_patches = int(args.patch)
    else:
        num_patches = config_tools.get_number_patches(config)

    early_stop = int(args.early)

    warm_restarts = args.warm_restarts

    do_augmentation = not args.skip_augmentation

    do_fine_tune = args.fine_tune

    num_cpus = args.num_cpu
    seed = args.seed
    if args.warmup is not None:
        warmup_epochs = int(args.warmup)
        print("Read warmup by argument")
    else:
        if config["train"]["warmup_epochs"] is not None:
            warmup_epochs = config["train"]["warmup_epochs"]
            print("Read warmup by config")
        else:
            warmup_epochs = 0
            print("Set warmup to zero")
    if early_stop < warmup_epochs:
        early_stop = warmup_epochs

    experimental_loss = args.exp_loss

    grid_w, grid_h = config_tools.get_gridcell_dimensions(config)

    ###############################
    #   Parse the annotations
    ###############################

    # parse annotations of the training set

    train_imgs, train_labels = parse_annotation2(
        ann_dir=config["train"]["train_annot_folder"],
        img_dir=config["train"]["train_image_folder"],
        grid_dims=(grid_w, grid_h, num_patches),
        anchor_size=int(config["model"]["anchors"][0]),
    )
    config["model"]["labels"] = ["particle"]

    # parse annotations of the validation set, if any, otherwise split the training set
    if os.path.exists(config["valid"]["valid_annot_folder"]):
        valid_imgs, valid_labels = parse_annotation2(
            config["valid"]["valid_annot_folder"],
            config["valid"]["valid_image_folder"],
            (grid_w, grid_h, num_patches),
        )

        if (
            len(valid_imgs) == 0
            or len(valid_labels) == 0
            or len(valid_labels) != len(valid_imgs)
        ):
            if len(valid_imgs) == 0:
                print(
                    "No validation images were found. Invalid validation configuration. Check your config file."
                )
            if len(valid_labels) == 0:
                print(
                    "No validation labels were found. Invalid validation configuration. Check your config file."
                )
    else:
        np.random.seed(seed)
        train_valid_split = int(0.8 * len(train_imgs))
        np.random.shuffle(train_imgs)
        valid_imgs = train_imgs[train_valid_split:]
        train_imgs = train_imgs[:train_valid_split]
        print("Validation set:")
        print([item["filename"] for item in valid_imgs])

    #####################################
    # Write runfile
    #####################################

    valid_imgs_paths = [item["filename"] for item in valid_imgs]
    valid_annot_paths = [item["boxpath"] for item in valid_imgs]
    train_imgs_paths = [item["filename"] for item in train_imgs]
    train_annot_paths = [item["boxpath"] for item in train_imgs]

    runjson = {}
    runjson["run"] = {}
    runjson["run"]["valid_images"] = valid_imgs_paths
    runjson["run"]["valid_annot"] = valid_annot_paths
    runjson["run"]["train_images"] = train_imgs_paths
    runjson["run"]["train_annot"] = train_annot_paths

    if not os.path.exists("runfiles/"):
        os.mkdir("runfiles/")
    timestr = time.strftime("%Y%m%d-%H%M%S")
    with open("runfiles/run_" + timestr + ".json", "w") as outfile:
        json.dump(runjson, outfile, ensure_ascii=False, indent=4)

    ##############################
    # Filter the data
    ##############################

    if "filter" in config["model"]:
        filter_options = config["model"]["filter"]
        if len(filter_options) > 2:
            model_path, overlap, nn_batch_size, filter_img_path = filter_options
            print("Filter data using noise2noise model: ", model_path)

            # Correct absolute filenames
            train_imgs_paths = [img["filename"] for img in train_imgs]

            filtered_paths = utils.filter_images_nn_dir(
                img_paths=train_imgs_paths,
                output_dir_filtered_imgs=filter_img_path,
                model_path=model_path,
                padding=overlap,
                batch_size=nn_batch_size,
            )

            # Update paths of newly filtered images
            for index, path in enumerate(filtered_paths):
                train_imgs[index]["filename"] = path

            valid_imgs_paths = [img["filename"] for img in valid_imgs]
            filtered_paths = utils.filter_images_nn_dir(
                img_paths=valid_imgs_paths,
                output_dir_filtered_imgs=filter_img_path,
                model_path=model_path,
                padding=overlap,
                batch_size=nn_batch_size,
            )
            # Update paths of newly filtered images
            for index, path in enumerate(filtered_paths):
                valid_imgs[index]["filename"] = path

        else:
            cutoff, filter_img_path = filter_options
            lowpass.filter_images(train_imgs, cutoff, filter_img_path, num_cpus)
            lowpass.filter_images(valid_imgs, cutoff, filter_img_path, num_cpus)

    overlap_labels = set(config["model"]["labels"]).intersection(
        set(train_labels.keys())
    )

    # Read first image and check the image depth.
    img_first = imagereader.image_read(train_imgs[0]["filename"])
    isgrey = False
    if len(img_first.shape) == 2:
        isgrey = True
    elif np.all(img_first[:, :, 0] == img_first[:, :, 1]) and np.all(
        img_first[:, :, 0] == img_first[:, :, 2]
    ):
        isgrey = True

    if isgrey:
        depth = 1
    else:
        depth = 3

    # As only on box size is expected, the anchor box size automatically

    if len(config["model"]["anchors"]) > 2:
        # general model is used
        img_width = 4096.0 / num_patches
        img_height = 4096.0 / num_patches
        cell_w = img_width / grid_w
        cell_h = img_height / grid_h
        anchors = np.array(config["model"]["anchors"], dtype=float)
        anchors[::2] = anchors[::2] / cell_w
        anchors[1::2] = anchors[1::2] / cell_h

    else:
        # specifc model is used
        img_width = float(img_first.shape[1]) / num_patches
        img_height = float(img_first.shape[0]) / num_patches

        cell_w = img_width / grid_w
        cell_h = img_height / grid_h
        box_width, box_height = config_tools.get_box_size(config)

        anchor_width = 1.0 * box_width / cell_w
        anchor_height = 1.0 * box_height / cell_h
        anchors = [anchor_width, anchor_height]

    if not config["train"]["log_path"]:
        log_path = "~/logs/"
    else:
        log_path = config["train"]["log_path"]
        if not os.path.exists(log_path):
            os.mkdir(log_path)

    # Get overlap patches
    overlap_patches = 0
    if "overlap_patches" in config["model"]:
        overlap_patches = int(config["model"]["overlap_patches"])
    elif not len(config["model"]["anchors"]) > 2:
        overlap_patches = config["model"]["anchors"][0]

    ###############################
    #   Construct the model
    ###############################
    backend_weights = None
    if "backend_weights" in config["model"]:
        backend_weights = config["model"]["backend_weights"]
    from cryolo.frontend import YOLO

    pretrained_weights = None
    if os.path.exists(config["train"]["pretrained_weights"]):
        pretrained_weights = config["train"]["pretrained_weights"]
    if num_gpus > 1:
        import tensorflow as tf

        with tf.device("/cpu:0"):
            yolo = YOLO(
                architecture=config["model"]["architecture"],
                input_size=config["model"]["input_size"],
                input_depth=depth,
                labels=config["model"]["labels"],
                max_box_per_image=config["model"]["max_box_per_image"],
                anchors=anchors,
                backend_weights=backend_weights,
                experimental_loss=experimental_loss,
                pretrained_weights=pretrained_weights,
                fine_tune=do_fine_tune,
            )
    else:
        yolo = YOLO(
            architecture=config["model"]["architecture"],
            input_size=config["model"]["input_size"],
            input_depth=depth,
            labels=config["model"]["labels"],
            max_box_per_image=config["model"]["max_box_per_image"],
            anchors=anchors,
            backend_weights=backend_weights,
            experimental_loss=experimental_loss,
            pretrained_weights=pretrained_weights,
            fine_tune=do_fine_tune,
        )

    # print a summary of the whole model
    yolo.model.summary()

    # USE MULTIGPU
    parallel_model = None
    if num_gpus > 1:
        from keras.utils import multi_gpu_model

        parallel_model = multi_gpu_model(yolo.model, gpus=num_gpus, cpu_merge=False)

    ###############################
    # Start the training process
    ###############################
    start = time.time()
    parent_pid = os.getpid()
    yolo.train(
        train_imgs=train_imgs,
        valid_imgs=valid_imgs,
        train_times=config["train"]["train_times"],
        valid_times=config["valid"]["valid_times"],
        nb_epoch=config["train"]["nb_epoch"],
        learning_rate=config["train"]["learning_rate"],
        batch_size=config["train"]["batch_size"],
        warmup_epochs=warmup_epochs,
        object_scale=config["train"]["object_scale"],
        no_object_scale=config["train"]["no_object_scale"],
        coord_scale=config["train"]["coord_scale"],
        class_scale=config["train"]["class_scale"],
        saved_weights_name=config["train"]["saved_weights_name"],
        debug=config["train"]["debug"],
        log_path=log_path,
        early_stop_thresh=early_stop,
        num_patches=num_patches,
        warm_restarts=warm_restarts,
        overlap_patches=overlap_patches,
        parallel_model=parallel_model,
        num_cpus=num_cpus,
        do_augmentation=do_augmentation,
    )

    end = time.time()
    print("Time elapsed for training:", (end - start))
    """
    time.sleep(3)
    ###############################
    # Find hanging threads and terminate them!
    ###############################
    try:
        parent = psutil.Process(parent_pid)
    except psutil.NoSuchProcess:
        return

    children = parent.children(recursive=False)
    for process in children:
        print("Terminate hanging child process")
        process.terminate()
    """


if __name__ == "__main__":
    multiprocessing.set_start_method("spawn")
    _main_()
