#user setting
CODE_DIR='/home/roaddb/others/shiyu/temp_test/code_branch'
LOC_RESULT_DIR = '/home/roaddb/others/shiyu/temp_test/test_result'
LIST_JSON_PATH = '/home/roaddb/others/shiyu/temp_test/temp_list.json'
RTV_SAVE_DIR = '/opt/ygomi/roadDB/rtv_dst'


#variales of machine
VISULIZATION_IP = '10.69.140.190'
ALGORITHM_IP = '10.69.140.193'
ALGORITHM_MAC = 'd0:4c:c1:02:4e:2a'
ALGORITHM_PORT = 'p20p1'
ALGORITHM_USER_NAME = 'roaddb'
ALGORITHM_PASSWORD = 'Test1234'

#variables of localization
MULTITHREADLOC = CODE_DIR+'/core/algorithm_vehicle_localization/dist/x64/bin/MultiThreadsLoc'
MULTITHREADBALOC = CODE_DIR + '/core/algorithm_vehicle_localization/dist/x64/bin/MultiThreadsBALoc'
SINGLETHREADLOC = CODE_DIR + '/core/algorithm_vehicle_localization/dist/x64/bin/SingleThreadLoc'
SINGLETHREADBALOC = CODE_DIR + '/core/algorithm_vehicle_localization/dist/x64/bin/SingleThreadBALoc'
LOG_LEVEL = '0'
LOC_MODE = '1'
LOC_CONFIG_PATH = CODE_DIR + '/core/algorithm_vehicle_localization/config'
SYS_CONFIG = LOC_CONFIG_PATH + '/sysConfig.json'
MOD_CONFIG = LOC_CONFIG_PATH + '/modConfig.json'
IMU_CONFIG = LOC_CONFIG_PATH + '/IMUConfig_Conti65.json'
CAMERA_CONFIG = LOC_CONFIG_PATH + '/camera_65_bigger_lens.json'
DATARECEIVER_CONFIG = CODE_DIR + '/framework/device/data-receiver/config/locDataReceiver.json'
SIMULATOR_DIR = CODE_DIR + '/framework/device/rdb-tools-debug-tools/rosplay-simulator/dist/x64/bin/rosplay-simulator'
