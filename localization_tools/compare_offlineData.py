# from xml.etree.ElementTree import iterparse
from bs4 import BeautifulSoup
import numpy as np
import matplotlib.pyplot as plt
import logging
import os

def grep_pose_list(file):
    pose = []
    predict = []
    with open(file) as f:
        for tag in f:
            if "frmID" in tag:
                continue

            info = tag.split()
            pose.append(info[3] + "," + info[4] + "," + info[5])
            predict.append(info[9] + "," + info[10] + "," + info[11])
    return pose, predict


def count_distance(pose1, pose2):
    pose1 = np.array(str_to_float(pose1))
    pose2 = np.array(str_to_float(pose2))
    distance = np.sqrt(np.sum(np.square(pose1 - pose2)))
    return distance


def str_to_float(pose):
    new_pose = []
    for i in pose.split(','):
        new_pose.append(float(i))
    return new_pose


def compare_offline(case_dir, case_name, output_path='tmp'):
    '''
    compare posreport kml and pose kml of the same case.
    only when report way is image.
    '''
    logging.info("case: {}".format(case_name))

    offline_file = os.popen('ls {}'.format(os.path.join(case_dir, '*-offLine_LocResult.txt'))).read().split()[0]

    pose_list, predict_list = grep_pose_list(offline_file)
    logging.debug("pose list:\n{}".format(pose_list))

    distance_list = []
    distance1 = []
    distance05 = []

    logging.info("the length of two kml. optimizePose kml: {}, reportPose kml: {}".format(len(pose_list), len(predict_list)))

    gap = 1
    maxIndex = len(pose_list) - gap
    for i in range(maxIndex):
        distance = count_distance(predict_list[i], pose_list[i+gap])
        distance_list.append(distance)
        if distance > 0.2:
            distance1.append((i,distance, predict_list[i], pose_list[i]))
        elif distance > 0.1:
            distance05.append((i,distance, predict_list[i], pose_list[i]))
        else:
            pass
    logging.debug("distance list:\n{}".format(distance_list))
    if distance05:
        logging.debug('the distance more than 0.5:')
        for item in distance05:
            logging.debug('index:%d, distance:%f, poseReport:%s, optimizePos:%s'%(item[0], item[1], item[2], item[3]))
    if distance1:
        logging.warning('the distance more than 3:')
        for item in distance1:
            logging.warning('index:%d, distance:%f, poseReport:%s, optimizePos:%s'%(item[0], item[1], item[2], item[3]))

    distance_list = np.array(distance_list)
    logging.info('total frames: {}'.format(len(distance_list)))
    logging.info('max_distance: {}'.format(np.max(distance_list)))
    logging.info('ave_distance: {}'.format(np.average(distance_list)))
    logging.info('variance: {}'.format(np.var(distance_list)))

    plt.figure(figsize=(20, 8))
    plt.plot(distance_list[::-1], color='#66BAB7')
    plt.title("kml distance of {}".format(case_name))
    plt.xlabel("id")
    plt.ylabel("distance(m)")
    plt.grid(axis='y')

    # plt.show()
    plt.savefig("{}/{}_offline.png".format(output_path, case_name))



if __name__ == '__main__':
    logging.basicConfig(filename='/home/user/localization/script/pythonproject/tools-for-working/tmp/compare_offline.log', level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    # logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    #folder = "/Users/jian.li/roadDB/caseRunLog/JLR_cam65_longSection" #"/Users/jian.li/roadDB/caseRunLog/honda"#
    #case_name_list = ['2017-01-01_T_07-20-50.455_UTC',
    #                  '2017-01-01_T_07-10-50.455_UTC',
    #                  '2017-01-01_T_06-55-50.455_UTC',
    #                  '2017-01-01_T_06-45-50.455_UTC',
    #                  '2017-01-01_T_06-40-50.455_UTC',
    #                  '2017-01-01_T_06-35-50.455_UTC']
    # folder = "/home/user/localization/RDB-46012/result_branch/multi_ekf/honda"
    # case_name_list = ['2019-09-05_T_18-24-04.387_UTC.img']
    #
    # for case_name in case_name_list:
    #     case_dir = os.path.join(folder, case_name)
    #     compare_offline(case_dir, case_name)

    # compare_offline('/home/user/localization/RDB-46012/result_branch/multi_ekf/honda/2019-09-11_T_23-59-46.484_UTC.img', '20191111144607_multi_ekf_honda_2019-09-11_T_23-59-46.484_UTC.img_branch1', '/home/user/localization/RDB-46012/output')
    compare_offline('/home/user/localization/RDB-46012/result_branch/multi_ekf/honda/2019-09-11_T_23-29-46.484_UTC.img', '20191111144607_multi_ekf_honda_2019-09-11_T_23-29-46.484_UTC.img_branch1', '/home/user/localization/RDB-46012/output')
