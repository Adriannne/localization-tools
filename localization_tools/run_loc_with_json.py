#!/usr/bin/env python
# coding=utf-8
'''
Run single thread localization

Create on Sep 07, 2018
@author: Shiyu Chen
'''

import os
import time
import logging
import subprocess
import io
import json
import getopt
import sys


def start_run():
    '''
    @summary: the main function of the script
    '''
    logging.basicConfig(level = logging.INFO, format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    run_localization('multi', 'ekf')
    # run_localization('single', 'ekf')
    # run_localization('single', 'ba')
    # run_localization('multi', 'ba')


def getArgs():
    '''
    @summary: get input params
    @return: codepath, resultpath, jsonpath
    '''
    code_path, result_path, json_path = ".", ".", "."

    options, args = getopt.getopt(sys.argv[1:], "c:r:j:", ["codepath=", "resultpath=", "jsonpath=", "help"])
    for name_, value_ in options:
        if name_ in ("-h", "--help"):
            usage()
        elif name_ in ("-c", "--codepath"):
            code_path = value_
            print(code_path)
        elif name_ in ("-r", "--resultpath"):
            result_path = value_
            print(result_path)
        elif name_ in ("-j", "--jsonpath"):
            json_path = value_
            print(json_path)
        else:
            print("error! cannot find this option: " + name_)
            usage()

    return code_path, result_path, json_path


def usage():
    '''
    @summary: print help info
    '''
    info = '''
    python run_loc_with_json.py -c <codepath> -r <resultpath> -j <jsonpath>
    '''
    print(info)
    exit()


def run_localization(thread, algo):
    '''
    @summary: the function to run localization
    '''
    code_path, total_result_path, json_path = getArgs()
    # os.system('sudo rm -rf {}/*'.format(total_result_path))

    with io.open(json_path, 'rb') as f:
        logging.info("read from list json file: {}".format(json_path))
        list_json = json.loads(f.read())
        f.close()
        for item in list_json:
            area_json_path = get_json_item_path(os.path.split(json_path)[0], item['Area'])
            cases = item['Cases']
            area, camera_config, db_path, db_type, case_list = read_json_data(area_json_path, cases)
            print(area, camera_config, db_path, db_type, case_list)
            for image_path in case_list:
                check_rtv_undistort(image_path)
                result_path = create_result_path(total_result_path, thread, algo, area, image_path)
                recording_top_msg(result_path)
                start_loc(image_path, camera_config, db_type, db_path, result_path, thread, algo, code_path)
                time.sleep(3)
                start_next(result_path)
                stop_recording_top_msg()


def read_json_data(area_json_path, cases):
    '''
    @summary: read data from area json file
    @param area_json_path: area json path
    @param cases: cases in list json
    @return: items in area json: area, camera_config, db_path, db_type, case_list
    '''
    case_list = []
    with io.open(area_json_path, 'rb') as f:
        logging.info("read from area json file: {}".format(area_json_path))
        area_json = json.loads(f.read())
        f.close()
        area = area_json['Area']
        area_json_parent_path = os.path.split(area_json_path)[0]
        camera_config = get_json_item_path(area_json_parent_path, area_json['CameraParameter'])
        db_path = get_json_item_path(area_json_parent_path, area_json['DBPath'])
        db_type = area_json['DBType']
        if cases:
            for item in cases:
                case_list.append(get_json_item_path(area_json_parent_path, item))
        else:
            for item in area_json['Cases']:
                case_list.append(get_json_item_path(area_json_parent_path, item['RtvRosbag']))
    return area, camera_config, db_path, db_type, case_list


def get_json_item_path(parent_path, path):
    '''
    @summary: get item path in json
    @param parent_path: the directory of json file
    @param path: item path in json file
    @return: absolute path of item
    '''
    if path[0] == '/':
        return path
    else:
        return parent_path + os.sep + path


def check_rtv_undistort(rtv_path):
    bin_file = '/opt/ygomi/roadDB/bin/rtv_detail_info'
    if os.path.isfile(bin_file):
        p = subprocess.Popen('{} --irtvpath {}'.format(bin_file, rtv_path), shell=True, stdout=subprocess.PIPE)
        ret = p.stdout.readlines()
        dic = json.loads(ret[0].decode())
        if dic['exit_code'] == 0:
            logging.info('undistort_flag: {}'.format(dic['rtv_info']['undistort_flag']))
            logging.info('rtv_frames_total: {}'.format(dic['rtv_info']['rtv_frames_total']))
        else:
            logging.warning('rtv_detail_info failed to get rtv info!')
    else:
        logging.warning('rtv_detail_info does not exist!')


def create_result_path(total_path, thread, algo, area, image_path):
    '''
    @summary: create localization result path
    @param thread: single or multi
    @param algo: ekf or ba
    @param area: the area of cases
    @param image_path: the path of rtv/rosbag
    @return: result path
    '''
    image_name = os.path.split(image_path)[-1]
    result_path = total_path + os.sep + thread + "_" + algo + os.sep + area + os.sep + image_name
    logging.info("result_path: {}".format(result_path))
    os.system("mkdir -p {}".format(result_path))
    return result_path

def start_loc(image, camera_config, db_type, db_dir, result_path, thread, algo, code_path):
    '''
    @summary: run localization with mode0 or mode1
    @param image: the image file path
    @param camera_config: the camera config path
    @param db_type: the db path
    @param db_dir: the db type
    @param result_path: the result path
    @param thread: single or multi
    @param algo: ekf or ba
    '''

    exe_file = get_exe_file(thread, algo, code_path)
    loc_cmd = generate_multiloc_cmd(exe_file, camera_config, db_type,
                                    db_dir, result_path, image, code_path)
    os.system(loc_cmd)

def get_exe_file(thread, algo, code_path):
    '''
    @summary: get exe file
    @return: exe file path
    '''
    if thread == 'multi' and algo == 'ekf':
        exe_file = code_path + '/core/algorithm_vehicle_localization/dist/x64/bin/MultiThreadsLoc'
    elif thread == 'multi' and algo == 'ba':
        exe_file = code_path + '/core/algorithm_vehicle_localization/dist/x64/bin/MultiThreadsBALoc'
    elif thread == 'single' and algo == 'ekf':
        exe_file = code_path + '/core/algorithm_vehicle_localization/dist/x64/bin/SingleThreadLoc'
    else:
        exe_file = code_path + '/core/algorithm_vehicle_localization/dist/x64/bin/SingleThreadBALoc'

    return exe_file

def generate_multiloc_cmd(exe_file, camera_config, db_type, db_dir, result_path, image_path, code_path):
    '''
    @summary: generate multi localization command
    @param mode: localization mode(0/1/2/3)
    @return: multi localization command
    '''
    loc_config_path = code_path + '/core/algorithm_vehicle_localization/config'
    sys_config = loc_config_path + '/sysConfig.json'
    mod_config = loc_config_path + '/modConfig.json'
    imu_config = loc_config_path + '/IMUConfig_Conti65.json'
    datareceiver_config = code_path + '/framework/device/data-receiver/config/locDataReceiver.json'

    cmd = 'sudo ' + exe_file + ' ' + \
          '--syscfg' + ' ' + sys_config + ' ' + \
          '--modcfg' + ' ' + mod_config + ' ' + \
          '--imucfg' + ' ' + imu_config + ' ' + \
          '--calib' + ' ' + camera_config + ' ' + \
          '--drcfg' + ' ' + datareceiver_config + ' ' + \
          '--dbtype' + ' ' + db_type + ' ' + \
          '--database' + ' ' + db_dir + ' ' + \
          '--filetype' + ' ' + 'rtvgroup' + ' ' + \
          '--bagrtv' + ' ' + image_path + ' ' + \
          '--loglevel 0 ' + \
          '--ologpath' + ' ' + result_path + '/log.txt' + ' ' + \
          '--output' + ' ' + result_path + ' ' + \
          '--testname' + ' ' + os.path.split(image_path)[1] + ' ' + \
          '--visualip 10.69.140.179 --locmode 1 >/dev/null 2>&1'
    logging.info("localization command: {}".format(cmd))
    return cmd

def recording_top_msg(result_path):
    '''
    @summary: recording top msg of abox
    @param: result_path: localization result path
    '''
    logging.info("recording top msg of abox")
    os.system("ps -ef | grep top | grep -v grep | awk '{print $2}'|xargs sudo kill -9")
    os.system('top -b -d 5 |grep -E "Tasks|%Cpu|KiB |RES|MultiThreadsLoc" > {}/topinfo.log &'.format(result_path))


def stop_recording_top_msg():
    '''
    @summary: stop recording top msg of abox
    '''
    logging.info('stop recording top msg of abox')
    os.system("ps -ef | grep top | grep -v grep | awk '{print $2}'|xargs sudo kill -9")

def check_localiztion_running():
    '''
    @summary: check if localization is running, if true, throw an except and exit.
    '''
    logging.info("check if localization is running")
    p = subprocess.Popen('ps -ef | grep MultiThreadsLoc | grep -v grep | wc -l', shell=True, stdout=subprocess.PIPE)
    locThread = str(p.stdout.readlines())
    logging.info("result:{}".format(locThread))
    if '0' in locThread:
        return True

def start_next(result_dir):
    '''
    @summary: check if script can run next rosbag
    @param result_path: result path of localization
    '''
    logging.info('check whether start next localization')
    if check_bin_file(result_dir):
        return True
    else:
        time.sleep(300)
        if check_bin_file(result_dir):
            return True
        else:
            logging.info("ThreadTiming.bin file didn't exist!")
            if check_localiztion_running():
                logging.info("localization is already running! force quit!")
                os.system("ps -ef | grep Multi | grep -v grep | awk '{print $2}'|xargs sudo kill -9")

def check_bin_file(result_dir):
    '''
    @summary: check if threadtiming.bin file has generated, if do, means localization process has done.
    @param result_path: result path of localization
    '''
    for file in os.listdir(result_dir):
        if ".bin" in file:
            return True


if __name__ == "__main__":
    start_run()
