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
    echo -e "\n--------------------build rdb-device-common-------------------------!\n"
    cd "$rootDir"/framework/device/rdb-device-common/ && ./build.sh -r
    if [ $? -ne 0 ];then 
       echo -e "\nbuild rdb-device-common failed!\n"
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
