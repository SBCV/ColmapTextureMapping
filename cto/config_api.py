import os
from shutil import copyfile
from enum import Enum
from cto.utility.config import Config
from cto.utility.logging_extension import logger


class ReconstructionMode(Enum):
    Open3D = 'Open3D'
    Colamp = 'Colmap'


def get_reconstruction_mode(config):
    reconstruction_mode = config.get_option_value('reconstruction_mode', target_type=str)
    assert reconstruction_mode in [ReconstructionMode.Open3D.value, ReconstructionMode.Colamp.value]
    return reconstruction_mode


def get_dataset_idp(config):
    reconstruction_mode = get_reconstruction_mode(config)
    dataset_idp = config.get_option_value(
        'dataset_idp', target_type=str, section=reconstruction_mode)
    logger.vinfo('dataset_idp', dataset_idp)
    return dataset_idp


def create_config():
    config_fp = 'configs/cto.cfg'
    config_with_default_values_fp = 'configs/cto_default_values.cfg'
    if not os.path.isfile(config_fp):
        logger.info('Config file missing ... create a copy from config with default values.')
        copyfile(os.path.abspath(config_with_default_values_fp), os.path.abspath(config_fp))
        logger.info('Adjust the input path in the created config file (cto.cfg)')
        assert False
    return Config(config_fp=config_fp)


def compute_ofp(config):
    dataset_idp = get_dataset_idp(config)
    reconstruction_mode = get_reconstruction_mode(config)
    mesh_textured_max_iter_x_ofn = config.get_option_value(
        'mesh_textured_max_iter_x_ofn', target_type=str)
    maximum_iteration = config.get_option_value(
        'maximum_iteration', target_type=int, section=reconstruction_mode)
    mesh_textured_max_iter_x_ofn = mesh_textured_max_iter_x_ofn.replace('_x.', '_' + str(maximum_iteration) + '.')
    return os.path.join(dataset_idp, mesh_textured_max_iter_x_ofn)


def depth_maps_from_mesh(config):
    return config.get_option_value('use_depth_maps_from_mesh', target_type=bool)

