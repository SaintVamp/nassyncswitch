touch /volume1/sync/speed_time
old_speed=`cat /volume1/sync/speed_time`
new_speed=`ifconfig eth0 | grep "RX bytes"|awk '{print $2}'| tr -d "bytes:"`
rs=`expr $new_speed - $old_speed`
`echo $new_speed > /volume1/sync/speed_time`
if [ $rs -gt 314572800 ]
then
  `echo 0 > /volume1/sync/rs`
else
  `echo 1 > /volume1/sync/rs`
fi