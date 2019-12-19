CUR_DIR=$(pwd)

for case in `ls ${CUR_DIR}`
do
    if [ -d "${CUR_DIR}/${case}" ];then
        cd ${CUR_DIR}/${case}
        echo $(pwd)
        mv ${CUR_DIR}/${case}/${case}.sensing.img    ${CUR_DIR}/${case}/${case}.img
        mv ${CUR_DIR}/${case}/${case}.65.imu        ${CUR_DIR}/${case}/${case}.imu
        mv ${CUR_DIR}/${case}/${case}.DGPS.gps       ${CUR_DIR}/${case}/${case}.gps
    fi
done
