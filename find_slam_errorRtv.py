import os

'''
the content of tmp/test.txt is from cmd:

roaddb@jpr239-backend:/opt/ygomi/roadDB/file_storage/serialized_process/backup/20191127105656_2019.1127.1830_JLR_data/Process/events/uploads$ find -name "106"
./9900ef1389294a4a8bcdbd6ff73a96d0/2019-11-27/logs/cmd/vehicle-slam/106
./9a888756abd64a7a8c817f7493b009d0/2019-11-27/logs/cmd/vehicle-slam/106

roaddb@jpr239-backend:/opt/ygomi/roadDB/file_storage/serialized_process/backup/20191127105656_2019.1127.1830_JLR_data/Process/events/uploads$ find -name "7"
./9900ef1389294a4a8bcdbd6ff73a96d0/2019-11-27/logs/cmd/vehicle-slam/7

roaddb@jpr239-backend:/opt/ygomi/roadDB/file_storage/serialized_process/backup/20191127105656_2019.1127.1830_JLR_data/Process/events/uploads$ find -name "10"
./662a9f9ee70a4242b3b4014c6aeb55f6/2019-11-27/logs/cmd/vehicle-slam/10
./f59b4d37976442a4bbb97309598b9493/2019-11-27/logs/cmd/vehicle-slam/10
./11dc00aad7154adc940eac75d3531d39/2019-11-27/logs/cmd/vehicle-slam/10
./038f6c4a28b44c8daa4d6e33b8a0c54c/2019-11-27/logs/cmd/vehicle-slam/10
'''

with open("tmp/test.txt", 'r') as f:
    for line in f.readlines():
        # print(line.split()[0].split('.')[1])
        linepath = "/opt/ygomi/roadDB/file_storage/serialized_process/backup/20191127105656_2019.1127.1830_JLR_data/Process/events/uploads" + line.split()[0].split('.')[1]
        # print(linepath)

        result = os.popen("ls {}".format(linepath))
        for line in result.readlines():
            if "stdout" in line:
                path = os.path.join(linepath, line.split()[0])
                os.popen("gzip {} -d".format(path))
                with open(os.path.splitext(path)[0], 'r') as f:
                    for line in f.readlines():
                        if "cmd options" in line:
                            # print(line.split()[3])
                            meta = os.path.split(line.split()[3])[1]
                            print(meta)