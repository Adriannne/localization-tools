compile_all=1
taskspace_code=/home/roaddb/others/shiyu/code_master

#===================================================#
#Do not modify the content below
#===================================================#

if [ ${compile_all} -eq 1 ]; then
    rootDir=${taskspace_code}
    source ~/.bashrc

    echo -e "\n--------------------build 3rd party-------------------------!\n"
    cd "$rootDir"/3rdparty  && ./build.sh -r
    if [ $? -ne 0 ];then 
       echo -e "\nbuild 3rd party failed!\n"
       exit 1
    fi
    echo -e "\n--------------------build global common-------------------------!\n"
    cd "$rootDir"/common/ && ./build.sh -r
    if [ $? -ne 0 ];then 
       echo -e "\nbuild global common failed!\n"
       exit 1
    fi
    echo -e "\n--------------------build core common-------------------------!\n"
    cd "$rootDir"/core/common/ && ./build.sh -r
    if [ $? -ne 0 ];then 
       echo -e "\nbuild core common failed!\n"
       exit 1
    fi
    echo -e "\n--------------------build gmock-------------------------!\n"
    cd "$rootDir"/framework/device/gmock/ && ./build.sh -r
    if [ $? -ne 0 ];then 
       echo -e "\nbuild gmock failed!\n"
       exit 1
    fi
    echo -e "\n--------------------build roaddb_logger-------------------------!\n"
    cd "$rootDir"/framework/device/roaddb_logger/ && ./build.sh -r
    if [ $? -ne 0 ];then 
       echo -e "\nbuild roaddb_logger failed!\n"
       exit 1
    fi
    echo -e "\n--------------------build rdb-vehicle-sensor-data-parser-------------------------!\n"
    cd "$rootDir"/framework/device/rdb-vehicle-sensor-data-parser/ && ./build.sh -r
    if [ $? -ne 0 ];then
       echo -e "\nbuild rdb-vehicle-sensor-data-parser failed!\n"
       exit 1
    fi
    echo -e "\n--------------------build roaddb_video-------------------------!\n"
    cd "$rootDir"/framework/device/roaddb_video/ && ./build.sh -r
    if [ $? -ne 0 ];then 
       echo -e "\nbuild roaddb_video failed!\n"
       exit 1
    fi
    echo -e "\n-----------------build road_in_vehicle_common_api----------------------!\n"
    sleep 5s
    cd "$rootDir"/framework/device/road_in_vehicle_common_api/ && ./build.sh -r
    if [ $? -ne 0 ];then 
       echo -e "\nbuild common api failed!\n"
       exit 1
    fi
    echo -e "\n--------------------build data receiver-------------------------!\n"
    echo `pwd`
    cd "$rootDir"/framework/device/data-receiver/ && ./build.sh -vr
    echo `pwd`
    if [ $? -ne 0 ];then 
       echo -e "\nbuild data receiver failed!\n"
       exit 1
    fi
    echo -e "\n--------------------build core algorithm_common-------------------------!\n"
    echo `pwd`
    cd "$rootDir"/core/algorithm_common/ && ./build.sh -r
    echo `pwd`
    if [ $? -ne 0 ];then 
       echo -e "\nbuild algorithm_common failed!\n"
       exit 1
    fi
    echo -e "\n--------------------build algorithm_vehicle_localization-------------------------!\n"
    echo `pwd`
    cd "$rootDir"/core/algorithm_vehicle_localization/ && ./build.sh -r
    echo `pwd`
    if [ $? -ne 0 ];then 
       echo -e "\nbuild algorithm_vehicle_localization failed!\n"
       exit 1
    fi
fi
