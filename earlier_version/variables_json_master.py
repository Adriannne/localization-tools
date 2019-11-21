#user setting
#CODE_DIR='/home/roaddb/others/shiyu/code_master'
CODE_DIR='/home/roaddb/others/shiyu/code_release'
LOC_RESULT_DIR = '/home/roaddb/others/shiyu/testresult'
LIST_JSON_PATH = '/home/roaddb/others/shiyu/193_script/rtv_img_list.json'
RTV_SAVE_DIR = '/home/roaddb/others/shiyu/RDB-39490/test_mode2'


#variales of machine
VISULIZATION_IP = '10.69.141.31'
ALGORITHM_IP = '10.69.140.220'
ALGORITHM_MAC = 'd0:4c:c1:02:4e:10'
ALGORITHM_PORT = 'eth6'
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
