hostname=an
if [ "$hostname" = "NAS2" ]; then
    curl -o /volume1/check/checkdata.py https://gitee.com/saintvamp/nassyncswitch/raw/master/checkdata.py
    curl -o /volume1/check/speed.sh  https://gitee.com/saintvamp/nassyncswitch/raw/master/speed.sh
    curl -o /volume1/check/exec.sh https://gitee.com/saintvamp/nassyncswitch/raw/master/exec.sh
    sed -i 's/name=/name=NAS2/g' /volume1/check/exec.sh
    python3 /volume1/check/checkdata.py
elif [ "$hostname" = "NAS3" ]; then
    curl -o /volume1/check/checkdata.py https://gitee.com/saintvamp/nassyncswitch/raw/master/checkdata.py
    curl -o /volume1/check/speed.sh  https://gitee.com/saintvamp/nassyncswitch/raw/master/speed.sh
    curl -o /volume1/check/exec.sh https://gitee.com/saintvamp/nassyncswitch/raw/master/exec.sh
    sed -i 's/name=/name=NAS3/g' /volume1/check/exec.sh
    python3 /volume1/check/checkdata.py
fi

