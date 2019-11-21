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
import variables_json_master as variables
import subprocess
import io
import json
import schedule


def start_run():
    '''
    @summary: the main function of the script
    '''
    logging.basicConfig(level = logging.INFO, format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    init_env(variables.LOC_RESULT_DIR, variables.RTV_SAVE_DIR)
    modify_sys_config(variables.SYS_CONFIG, variables.VISULIZATION_IP, variables.ALGORITHM_PORT, variables.RTV_SAVE_DIR)

    run_localization('multi', 'ekf')
    run_localization('single', 'ekf')
    run_localization('single', 'ba')
    run_localization('multi', 'ba')


def run_localization(thread, algo):
    '''
    @summary: the function to run localization
    '''
    with io.open(variables.LIST_JSON_PATH, 'rb') as f:
        logging.info("read from list json file: {}".format(variables.LIST_JSON_PATH))
        list_json = json.loads(f.read())
        f.close()
        for item in list_json:
            area_json_path = get_json_item_path(os.path.split(variables.LIST_JSON_PATH)[0], item['Area'])
            cases = item['Cases']
            area, camera_config, db_path, db_type, case_list = read_json_data(area_json_path, cases)
            print(area, camera_config, db_path, db_type, case_list)
            for image_path in case_list:
                result_path = create_result_path(thread, algo, area, image_path)
                recording_top_msg(result_path)
                start_loc(image_path, camera_config, db_type, db_path, result_path, thread, algo)
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


def create_result_path(thread, algo, area, image_path):
    '''
    @summary: create localization result path
    @param thread: single or multi
    @param algo: ekf or ba
    @param area: the area of cases
    @param image_path: the path of rtv/rosbag
    @return: result path
    '''
    image_name = os.path.split(image_path)[-1]
    result_path = variables.LOC_RESULT_DIR + os.sep + thread + "_" + algo + os.sep + area + os.sep + image_name
    logging.info("result_path: {}".format(result_path))
    os.system("mkdir -p {}".format(result_path))
    return result_path


def init_env(result_dir, RTV_SAVE_DIR):
    '''
    @summary: init abox environment
    @param: result_dir: localization total result dir
    '''
    logging.info("init abox environment")
    os.system('sudo rm -rf {}/*'.format(result_dir))
    os.system("ps -ef | grep top | grep -v grep | awk '{print $2}'|xargs sudo kill -9")
    if not os.path.exists(RTV_SAVE_DIR):
        os.system('sudo mkdir -p {}'.format(RTV_SAVE_DIR))


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


def modify_sys_config(config_path, visual_ip, abox_port, rtv_save_path):
    '''
    @summary: modify port and input directory
    @param config_path:data receiver config of localization
    @param port:the port data receiver read data
    @param input_data:the rtv imu gps path, there should be only one group of rtv imu gps in the path
    '''
    logging.info("modify sys config: {}".format(config_path))
    with io.open(config_path, 'rb') as f:
        json_file = json.loads(f.read())
        f.close()

        logging.info("former visualization ip: {}".format(json_file['Visual']['VisualIP']))
        json_file['Visual']['VisualIP'] = visual_ip
        logging.info("new port: {}".format(json_file['Visual']['VisualIP']))

        logging.info("former data receiver port: {}".format(json_file['DataReceiver']['Recorder']['EthAdapterName']))
        json_file['DataReceiver']['Recorder']['EthAdapterName'] = abox_port
        logging.info("new port: {}".format(json_file['DataReceiver']['Recorder']['EthAdapterName']))

        logging.info("former rtv save path: {}".format(json_file['DataReceiver']['Recorder']['SavePath']))
        json_file['DataReceiver']['Recorder']['SavePath'] = rtv_save_path
        logging.info("new path: {}".format(json_file['DataReceiver']['Recorder']['SavePath']))

    with io.open(config_path, 'wb') as f:
        json.dump(json_file, f, sort_keys=True, indent=4, separators=(',', ': '))
        f.close()


def start_loc(image, camera_config, db_type, db_dir, result_path, thread, algo):
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

    exe_file = get_exe_file(thread, algo)
    mode = get_mode(image)
    logging.info('exefile: {}, mode: {}, thread: {}'.format(exe_file, mode, thread))
    if mode == '0':
        loc_cmd = 'nohup ' + generate_multiloc_rosbag_cmd(exe_file, camera_config, db_type,
                                                          db_dir, result_path, mode, image) + ' &'
        subprocess.Popen(loc_cmd, shell=True, cwd=result_path)
        time.sleep(3)
        sim_log_name = result_path + os.sep + 'sim_{}.log'.format(os.path.split(image)[1])
        sim_cmd = generate_simulator_cmd(image, sim_log_name)
        os.system(sim_cmd)
    elif mode == '1':
        loc_cmd = generate_multiloc_cmd(exe_file, camera_config, db_type,
                                        db_dir, result_path, mode, image)
        os.system(loc_cmd)
    else:
        pass

def get_exe_file(thread, algo):
    '''
    @summary: get exe file
    @return: exe file path
    '''
    exe_file = variables.MULTITHREADLOC
    if thread == 'multi' and algo == 'ekf':
        exe_file = variables.MULTITHREADLOC
    elif thread == 'multi' and algo == 'ba':
        exe_file = variables.MULTITHREADBALOC
    elif thread == 'single' and algo == 'ekf':
        exe_file = variables.SINGLETHREADLOC
    elif thread == 'single' and algo == 'ba':
        exe_file = variables.SINGLETHREADBALOC
    else:
        pass
    return exe_file


def get_mode(image):
    '''
    @summary: get localization mode
    @return: mode
    '''
    mode = '1'
    if os.path.splitext(os.path.split(image)[1])[1] == '.bag':
        mode = '0'
    return mode

def generate_multiloc_cmd(exe_file, camera_config, db_type, db_dir, result_path, mode, image_path):
    '''
    @summary: generate multi localization command
    @param mode: localization mode(0/1/2/3)
    @return: multi localization command
    '''
    cmd = 'sudo ' + exe_file + ' ' + \
          '--syscfg' + ' ' + variables.SYS_CONFIG + ' ' + \
          '--modcfg' + ' ' + variables.MOD_CONFIG + ' ' + \
          '--imucfg' + ' ' + variables.IMU_CONFIG + ' ' + \
          '--camcfg' + ' ' + camera_config + ' ' + \
          '--dbtype' + ' ' + db_type + ' ' + \
          '--database' + ' ' + db_dir + ' ' + \
          '--filetype' + ' ' + 'rtvgroup' + ' ' + \
          '--bagrtv' + ' ' + image_path + ' ' + \
          '--loglevel' + ' ' + variables.LOG_LEVEL + ' ' + \
          '--ologpath' + ' ' + result_path + '/log.txt' + ' ' + \
          '--output' + ' ' + result_path + ' ' + \
          '--testname' + ' ' + os.path.split(image_path)[1] + ' ' + \
          '--locmode' + ' ' + mode + ' ' + \
          '--drcfg' + ' ' + variables.DATARECEIVER_CONFIG + ' >/dev/null 2>&1'
    logging.info("localization command: {}".format(cmd))
    return cmd

def generate_multiloc_rosbag_cmd(exe_file, camera_config, db_type, db_dir, result_path, mode, image_path):
    '''
    @summary: generate multi localization command
    @param mode: localization mode(0/1/2/3)
    @return: multi localization command
    '''
    cmd = 'sudo ' + exe_file + ' ' + \
          '--syscfg' + ' ' + variables.SYS_CONFIG + ' ' + \
          '--modcfg' + ' ' + variables.MOD_CONFIG + ' ' + \
          '--imucfg' + ' ' + variables.IMU_CONFIG + ' ' + \
          '--camcfg' + ' ' + camera_config + ' ' + \
          '--dbtype' + ' ' + db_type + ' ' + \
          '--database' + ' ' + db_dir + ' ' + \
          '--loglevel' + ' ' + variables.LOG_LEVEL + ' ' + \
          '--ologpath' + ' ' + result_path + '/log.txt' + ' ' + \
          '--output' + ' ' + result_path + ' ' + \
          '--testname' + ' ' + os.path.split(image_path)[1] + ' ' + \
          '--locmode' + ' ' + mode + ' ' + \
          '--drcfg' + ' ' + variables.DATARECEIVER_CONFIG + ' >/dev/null 2>&1'
    logging.info("localization command: {}".format(cmd))
    return cmd

def generate_simulator_cmd(image_path, sim_log_name):
    '''
    @summary: generate simulator command
    @param image_path: image path(rosbag/rtv)
    @param sim_log_name: simulator log name
    @return: simulator command
    '''
    sim_cmd = 'sudo ' + variables.SIMULATOR_DIR + ' ' + \
              '-d' + ' ' + variables.ALGORITHM_PORT + ' ' + \
              '-f' + ' ' + image_path + ' ' + \
              '-t' + ' ' + variables.ALGORITHM_IP + ' ' + \
              '-m' + ' ' + variables.ALGORITHM_MAC + ' ' + \
              '-g 4 ' + '-u 7 ' + \
              '-k > ' + sim_log_name + ' 2>&1'
    logging.info("send rosbag command: {}".format(sim_cmd))
    return sim_cmd

def recording_top_msg(result_path):
    '''
    @summary: recording top msg of abox
    @param: result_path: localization result path
    '''
    logging.info("recording top msg of abox")
    os.system('top -b -d 5 |grep -E "Tasks|%Cpu|KiB" > {}/topinfo.log &'.format(result_path))


def stop_recording_top_msg():
    '''
    @summary: stop recording top msg of abox
    '''
    logging.info('stop recording top msg of abox')
    os.system("ps -ef | grep top | grep -v grep | awk '{print $2}'|xargs sudo kill -9")


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


def analysis_log(result_path, script_path):
    '''
    @summary: call analysis log script to analysis localization log
    @param result_path: result path of localization
    @param script_path: analysis log script path
    '''
    logging.info('analysis localization log')
    for file in os.listdir(result_path):
        if 'log.txt' in file:
            filepath = result_path + os.sep + file
            cmd = 'python {} {}'.format(script_path, filepath)
            logging.info('command: {}'.format(cmd))
            os.system(cmd)



if __name__ == "__main__":
    start_run()
    # schedule.every().day.at("11:00").do(start_run)
    # while True:
    #     schedule.run_pending()
    #     time.sleep(1)
