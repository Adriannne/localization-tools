import os
import subprocess
import json
import logging

def check_rtv_undistort(rtv_path):
    bin_file = '/opt/ygomi/roadDB/bin/rtv_detail_info'
    if os.path.isfile(bin_file):
        p = subprocess.Popen('{} --irtvpath {}'.format(bin_file, rtv_path), shell=True, stdout=subprocess.PIPE)
        # p = subprocess.Popen('cat /Users/user/shiyu/script/tools-for-loc/tmp/test1.json', shell=True, stdout=subprocess.PIPE)
        ret = p.stdout.readlines()
        dic = json.loads(ret[0].decode())
        if dic['exit_code'] == 0:
            logging.info('undistort_flag: {}'.format(dic['rtv_info']['undistort_flag']))
            logging.info('rtv_frames_total: {}'.format(dic['rtv_info']['rtv_frames_total']))
        else:
            logging.warning('rtv_detail_info failed to get rtv info!')
    else:
        logging.warning('rtv_detail_info does not exist!')

if __name__ == '__main__':
    logging.basicConfig(level = logging.INFO, format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    check_rtv_undistort('/home/roaddb/test_case/1-JLR_cam65_longSection/RTV_undistorted/2017-01-01_T_06-35-50.455_UTC/2017-01-01_T_06-35-50.455_UTC.img')