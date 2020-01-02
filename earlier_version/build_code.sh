compile_all=1
code_dir=/home/roaddb/others/shiyu/code_branch

#===================================================#
#Do not modify the content below
#===================================================#

if [ ${compile_all} -eq 1 ]; then
    rootDir=${code_dir}
    source ~/.bashrc

#    echo -e "\n-------------------------build 3rdparty-------------------------!\n"
#    cd "$rootDir"/3rdparty && ./build.sh -r
#    if [ $? -ne 0 ];then
#        echo -e "\nbuild 3rdparty failed!\n"
#        exit 1
#    fi
#
#    echo -e "\n-------------------------build common-------------------------!\n"
#    cd "$rootDir"/common && ./build.sh -r
#    if [ $? -ne 0 ];then
#        echo -e "\nbuild common failed!\n"
#        exit 1
#    fi
#
#    echo -e "\n-------------------------build rdb-device-common-------------------------!\n"
#    cd "$rootDir"/framework/device/rdb-device-common && ./build.sh -r
#    if [ $? -ne 0 ];then
#        echo -e "\nbuild rdb-device-common failed!\n"
#        exit 1
#    fi
#
#    echo -e "\n-------------------------build road_in_vehicle_common_api-------------------------!\n"
#    cd "$rootDir"/framework/device/road_in_vehicle_common_api && ./build.sh -r
#    if [ $? -ne 0 ];then
#        echo -e "\nbuild road_in_vehicle_common_api failed!\n"
#        exit 1
#    fi

    echo -e "\n-------------------------build algorithm_common-------------------------!\n"
    cd "$rootDir"/core/algorithm_common && ./build.sh -r
    if [ $? -ne 0 ];then
        echo -e "\nbuild algorithm_common failed!\n"
        exit 1
    fi

    echo -e "\n-------------------------build data-receiver-------------------------!\n"
    cd "$rootDir"/framework/device/data-receiver && ./build.sh -vr
    if [ $? -ne 0 ];then
        echo -e "\nbuild data-receiver failed!\n"
        exit 1
    fi

    echo -e "\n-------------------------build algorithm_vehicle_localization-------------------------!\n"
    cd "$rootDir"/core/algorithm_vehicle_localization && ./build.sh -r
    if [ $? -ne 0 ];then
        echo -e "\nbuild algorithm_vehicle_localization failed!\n"
        exit 1
    fi

    echo -e "\n-------------------------build rdb-loc-visualization-------------------------!\n"
    cd "$rootDir"/core/rdb-loc-visualization && ./build.sh -e
    if [ $? -ne 0 ];then
        echo -e "\nbuild rdb-loc-visualization failed!\n"
        exit 1
    fi
fi
