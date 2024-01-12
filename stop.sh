hostname=an
if [ "$hostname" = "NAS2" ]; then

fi

curl -o /volume1/checkdata.py https://gitee.com/saintvamp/nassyncswitch/raw/master/main.py
curl -o /volume1/speed.sh  https://gitee.com/saintvamp/nassyncswitch/raw/master/speed.sh
curl -o /volume1/checkdata.py https://gitee.com/saintvamp/nassyncswitch/raw/master/exec.sh
sed -i 's/\/session\/2/\/session\/1/g' /volume1/checkdata.py
python3 /volume1/checkdata.py