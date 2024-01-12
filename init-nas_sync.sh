hostname=`echo hostname`
if [ "$hostname" = "SV-NAS2" ]; then
    curl -o /volume1/start.sh https://gitee.com/saintvamp/nassyncswitch/raw/master/start.sh
    sed -i 's/name=/name=NAS2/g' /volume1/start.sh
    curl -o /volume1/stop.sh https://gitee.com/saintvamp/nassyncswitch/raw/master/stop.sh
    sed -i 's/hostname=an/hostname=NAS2/g' /volume1/stop.sh
fi

