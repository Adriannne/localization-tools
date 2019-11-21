import os

filename = "/home/user/localization/RDB-44611/result_branch/multi_ekf/JLR_cam65_longSection/2017-01-01_T_06-45-50.455_UTC.img"
dirname = "/home/user/localization/RDB-44611/result_branch/multi_ekf"

g = os.walk(filename)

for path, dir_list, file_list in g:
    for file_name in file_list:
        if "point.kml" in file_name:
            print(os.path.join(path, file_name))
            # print(file_name.split("-")[0])
            log_path = os.path.join(path, file_name.split("-")[0] + "-log.txt.txt")
            if os.path.isfile(log_path):
                print(log_path)
                os.system("grep '.kml' {}".format(log_path))