hostname=`hostname`
if [ "$hostname" = "SV-NAS2" ]; then
    curl -o /volume1/check/start.sh https://gitee.com/saintvamp/nassyncswitch/raw/master/start.sh
    sed -i 's/name=/name=NAS2/g' /volume1/check/start.sh
    curl -o /volume1/check/stop.sh https://gitee.com/saintvamp/nassyncswitch/raw/master/stop.sh
    sed -i 's/hostname=an/hostname=NAS2/g' /volume1/check/stop.sh
    sh /volume1/check/start.sh
elif [ "$hostname" = "SV-NAS3" ]; then
    curl -o /volume1/check/start.sh https://gitee.com/saintvamp/nassyncswitch/raw/master/start.sh
    sed -i 's/name=/name=NAS3/g' /volume1/check/start.sh
    curl -o /volume1/check/stop.sh https://gitee.com/saintvamp/nassyncswitch/raw/master/stop.sh
    sed -i 's/hostname=an/hostname=NAS3/g' /volume1/check/stop.sh
    sh /volume1/check/start.sh
fi