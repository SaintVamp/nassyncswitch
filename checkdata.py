# 这是一个示例 Python 脚本。
import os
import sqlite3
import time
import datetime


def get_time():
    now = datetime.datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")


flag = 0

local_conn = sqlite3.connect("count.sqlite")
local_cur = local_conn.cursor()
local_cur.execute(
    'CREATE TABLE IF NOT EXISTS status(id INTEGER PRIMARY KEY,local_mtime INTEGER,local_file_size INTEGER,timestamp INTEGER,number INTEGER)')
# conn = sqlite3.connect('/volume1/@cloudsync/session/2/event-db.sqlite')
conn = sqlite3.connect('/volume1/@cloudsync/session/1/event-db.sqlite')
cur = conn.cursor()
cur.execute('select max(id) from event_info')
v_id = cur.fetchone()[0]
os.system("echo '-2:" + str(get_time()) + " v_id is " + str(v_id) + " '>> /volume1/check/run.log")
cur.execute(
    'select id,local_mtime,mtime,local_file_size,file_size,timestamp,file_type from event_info where id =' + str(v_id))
v_data = cur.fetchone()
os.system("echo '-1:" + str(v_data) + " '>> /volume1/check/run.log")

local_cur.execute('select * from status')
local_data = local_cur.fetchone()
if local_data == None:
    op_sql = ("insert into status values (" + str(v_data[0]) + "," + str(v_data[1]) + "," +
              str(v_data[3]) + "," + str(v_data[5]) + ",0)")
    local_cur.execute(op_sql)
    local_conn.commit()
    os.system("echo '0:" + str(get_time()) + " init data '>> /volume1/check//run.log")
else:
    os.system("echo '01:" + str(local_data[0]) + " " + str(v_data[0]) + " init data '>> /volume1/check//run.log")
    if local_data[0] == v_data[0]:  # id是否相同
        if v_data[6] == 1:  # 同步的是否是目录
            if v_data[1] + v_data[5] == local_data[1] + local_data[3]:  # 判断local_mtime+timestamp是否一致
                if local_data[4] == 2:  # 判断number计次数
                    flag = 1
                    op_sql = "delete from status "
                    local_cur.execute(op_sql)
                    local_conn.commit()
                    os.system("echo '1:" + str(get_time()) + " count num is 2 '>> /volume1/check//run.log")
                    # 重启
                else:
                    op_sql = "update status set number = " + str(local_data[4] + 1)
                    local_cur.execute(op_sql)
                    local_conn.commit()
                    os.system("echo '2:" + str(get_time()) + " write count '>> /volume1/check//run.log")
            else:
                op_sql = ("update status set local_mtime = " + str(v_data[1]) + ",local_file_size = " +
                          str(v_data[3]) + ",timestamp = " + str(v_data[5]) + ",number = 0")
                local_cur.execute(op_sql)
                local_conn.commit()
                os.system("echo '3:" + str(get_time()) + " update data '>> /volume1/check//run.log")
        else:
            if v_data[1] - v_data[2] != 0 or v_data[3] - v_data[4] != 0:
                # 远端local_mtime,mtime,local_file_size,file_size是否已经一致
                pass
                os.system("echo '4:" + str(get_time()) + " no sync waiting '>> /volume1/check//run.log")
                # 不一致，继续等待
            else:
                if v_data[1] + v_data[5] == local_data[1] + local_data[3]:  # 判断local_mtime+timestamp是否一致
                    if local_data[4] == 2:  # 判断number计次数
                        flag = 1
                        op_sql = "delete from status "
                        local_cur.execute(op_sql)
                        local_conn.commit()
                        os.system("echo '5:" + str(get_time()) + " count num is 2 '>> /volume1/check//run.log")
                        # 重启
                    else:
                        op_sql = "update status set number = " + str(local_data[4] + 1)
                        local_cur.execute(op_sql)
                        local_conn.commit()
                        os.system("echo '6:" + str(get_time()) + " "
                                  + str(local_data[4]) + " write count '>> /volume1/check//run.log")
                else:
                    op_sql = ("update status set local_mtime = " + str(v_data[1]) + ",local_file_size = " +
                              str(v_data[3]) + ",timestamp = " + str(v_data[5]) + ",number = 0")
                    local_cur.execute(op_sql)
                    local_conn.commit()
                    os.system("echo '7:" + str(get_time()) + " update data '>> /volume1/check//run.log")
    else:
        op_sql = ("update status set local_mtime = " + str(v_data[1]) + ",local_file_size = " + str(v_data[3]) + ",id = " +
                  str(v_data[0]) + ",timestamp = " + str(v_data[5]) + ",number = 0")
        local_cur.execute(op_sql)
        local_conn.commit()
        os.system("echo '8:" + str(get_time()) + " update data '>> /volume1/check//run.log")
local_conn.close()
conn.close()
os.system("sh /volume1/check//speed.sh")
with open('/volume1/check//rs', 'r', encoding='utf-8') as f:
    data = int(f.readline())
    os.system("echo '9-1:speed_rs is " + str(data) + "'>> /volume1/check//run.log")
if flag == 1 and data == 1:
    os.system("echo '9:" + str(get_time()) + " close '>> /volume1/check//run.log")
    os.system("sh /volume1/check//exec.sh")
    # 重启
