hostname=an
if [ "$hostname" = "NAS2" ]; then
    curl -o /volume1/sync/checkdata.py https://gitee.com/saintvamp/nassyncswitch/raw/master/checkdata.py
    curl -o /volume1/sync/speed.sh  https://gitee.com/saintvamp/nassyncswitch/raw/master/speed.sh
    curl -o /volume1/sync/exec.sh https://gitee.com/saintvamp/nassyncswitch/raw/master/exec.sh
    sed -i 's/\/session\/2/\/session\/1/g' /volume1/sync/checkdata.py
    sed -i 's/name=/name=NAS2/g' /volume1/sync/exec.sh
    python3 /volume1/sync/checkdata.py
fi

