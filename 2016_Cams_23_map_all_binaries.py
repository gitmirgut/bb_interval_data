
PATH_REPRO_IN = '/mnt/storage/beesbook-data-clean/pipeline_data/repo_season_2016_fixed'
PATH_REPRO_OUT = '/mnt/storage/beesbook/171109_mapped_repo_season_2016_fixed'
PATH_INTERVALS = './2016_Cams_23_intervals_pair_validation.json'
PATH_PARAM = './2016_Cams23/'
LOG_PATH = '2016_Cams23_log.txt'
CAM_LEFT = 2
CAM_RIGHT = 3

import json
import logging
import os

import iso8601

import bb_binary.repository as bbb_r
import bb_convert_binaries.core as con_core
import bb_stitcher.core as st_core

log = logging.getLogger(__name__)

def get_parameter_path(root_path, interval_id, cam_left_id, cam_right_id):
    """Get the path of the file which holds the paremter for the surveyor.

    Args:
        root_path (str): Path where all the paremter files are located.
        interval_id (int): Id of the Interval you need.
        cam_left_id (int): Id of the left camera.
        cam_right_id (int): Id of the right camera.

    Returns:
        (str): path of the interval file.
    """
    prefix = 'Cams_{left_cam}{right_cam}_interval_{int_id}'.format(left_cam=cam_left_id, right_cam=cam_right_id, int_id=str(interval_id).zfill(2))
    ext = 'json'
    valid_file = [f for f in os.listdir(root_path) if f[:19] == prefix and f[-4:] == ext]
    if len(valid_file) == 1:
        return os.path.join(root_path, valid_file[0])
    else:
        Exception('This should not be possible!')

logging.basicConfig(
    filename=LOG_PATH,
    level=logging.ERROR,
    format='%(asctime)s - %(name)-12s- %(levelname)s - %(message)s')
logging.getLogger(__name__).setLevel(logging.DEBUG)
logging.getLogger('bb_convert_binaries.core').setLevel(logging.DEBUG)


log.info('START MAPPING')
log.info('--------------------------------------')
log.info('Repro in: {in_repro}'.format(in_repro=PATH_REPRO_IN))
log.info('Repro out: {out_repro}'.format(out_repro=PATH_REPRO_OUT))
log.info('File with intervals: {intervals}'.format(intervals=PATH_INTERVALS))
log.info('Directory with parameter files: {directory}'.format(directory=PATH_PARAM))
log.info('--------------------------------------')
with open(PATH_INTERVALS) as data_file:
    intervals = json.load(data_file)

bbb_repro = bbb_r.Repository(PATH_REPRO_IN)
bbb_converter = con_core.BBB_Converter()


for interval in intervals:
    interval_id = interval['id']
    log.info('# Starting mapping for Interval {id}'.format(id=interval_id))

    path_param = get_parameter_path(PATH_PARAM, interval_id, CAM_LEFT, CAM_RIGHT)
    curr_surveyor = st_core.Surveyor()
    curr_surveyor.load(path_param)

    for key in ['left', 'right']:
        if interval[key] is None:
            log.warning('The side {side} of the Interval {int_id} is None'.format(side=key, int_id=interval['id']))
            continue

        curr_cam_id = interval[key]['cam_id']
        curr_start = iso8601.parse_date(interval[key]['ts_start'])
        curr_end = iso8601.parse_date(interval[key]['ts_end'])

        log.info('START Interval:{int_id} | Side: {side} | Cam_id:{cam_id}'.format(int_id=interval['id'], side=key, cam_id=curr_cam_id))
        log.info('start ts: {start_ts} | end ts: {end_ts}'.format(start_ts=curr_start, end_ts=curr_end))

        bbb_converter.convert_bbb_interval(curr_start, curr_end, bbb_repro, curr_cam_id, curr_surveyor, PATH_REPRO_OUT)

        log.info('Success')
        log.info('###########################################')
