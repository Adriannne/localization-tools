import os

def scan_all_logs(dir_path, result_log, key, limits=99):
    new_file = open(result_log, 'w')

    for root, dir_list, file_list in os.walk(dir_path):
        for file_name in file_list:
            if "log.txt_keyInfo.txt" in file_name:
                file_path = os.path.join(root, file_name)
                print(file_path)
                new_file.writelines(file_path + '\n')

                file = open(file_path)

                l = 0
                for lines in file.readlines():
                    if key in lines:
                        new_file.writelines(lines)
                        l += 1
                    if l >= limits:
                        break
                file.close()
                new_file.writelines('\n')

    new_file.close()



# scan_path = "/home/user/localization/RDB-44712"
# scan_all_logs(scan_path, result_log, 'decode fail', 20)

scan_path = "/home/user/localization/RDB-45057/result"
result_log = os.path.join(scan_path, "extract_warning_keylog.txt")
scan_all_logs(scan_path, result_log, '[warning]', 99999999)
