# 这是一个示例 Python 脚本。
import sqlite3
import os
import time

flag = 0

local_conn = sqlite3.connect("status.sqlite")
local_cur = local_conn.cursor()
local_cur.execute(
    'CREATE TABLE IF NOT EXISTS status(id INTEGER PRIMARY KEY,local_mtime INTEGER,local_file_size INTEGER,timestamp INTEGER,number INTEGER)')
conn = sqlite3.connect('/volume1/@cloudsync/session/2/event-db.sqlite')
cur = conn.cursor()
cur.execute('select max(id) from event_info')
v_id = cur.fetchone()[0]
cur.execute(
    'select id,local_mtime,mtime,local_file_size,file_size,timestamp,file_type from event_info where id =' + str(v_id))
v_data = cur.fetchone()

local_cur.execute('select * from status')
local_data = local_cur.fetchone()
if local_data == None:
    op_sql = ("insert into status values (" + str(v_data[0]) + "," + str(v_data[1]) + "," +
              str(v_data[3]) + "," + str(v_data[5]) + ",0)")
    local_cur.execute(op_sql)
    local_conn.commit()
else:
    if local_data[0] == v_data[0]:  # id是否相同
        if v_data[6] == 1:  # 同步的是否是目录
            if v_data[1] + v_data[5] == local_data[1] + local_data[3]:  # 判断local_mtime+timestamp是否一致
                if local_data[4] == 2:  # 判断number计次数
                    flag = 1
                    op_sql = "delete from status "
                    local_cur.execute(op_sql)
                    local_conn.commit()
                    # 重启
                else:
                    os.system("echo '" + str(time.time()) + " write count '>> run.log")
                    op_sql = "update status set number = " + str(local_data[4] + 1)
                    local_cur.execute(op_sql)
                    local_conn.commit()
            else:
                op_sql = ("update status set local_mtime = " + str(v_data[1]) + ",local_file_size = " +
                          str(v_data[3]) + ",timestamp = " + str(v_data[5]) + ",number = 0")
                local_cur.execute(op_sql)
                local_conn.commit()
        else:
            if v_data[1] - v_data[2] != 0 or v_data[3] - v_data[4] != 0:
                # 远端local_mtime,mtime,local_file_size,file_size是否已经一致
                pass
                os.system("echo '" + str(time.time()) + " no sync waiting '>> run.log")
                # 不一致，继续等待
            else:
                if v_data[1] + v_data[5] == local_data[1] + local_data[3]:  # 判断local_mtime+timestamp是否一致
                    if local_data[4] == 2:  # 判断number计次数
                        flag = 1
                        op_sql = "delete from status "
                        local_cur.execute(op_sql)
                        local_conn.commit()
                        # 重启
                    else:
                        op_sql = "update status set number = " + str(local_data[4] + 1)
                        os.system("echo '" + str(time.time()) + " write count '>> run.log")
                        local_cur.execute(op_sql)
                        local_conn.commit()
                else:
                    op_sql = ("update status set local_mtime = " + str(v_data[1]) + ",local_file_size = " +
                              str(v_data[3]) + ",timestamp = " + str(v_data[5]) + ",number = 0")
                    local_cur.execute(op_sql)
                    local_conn.commit()
    else:
        op_sql = ("update status set local_mtime = " + str(v_data[1]) + ",local_file_size = " +
                  str(v_data[3]) + ",timestamp = " + str(v_data[5]) + ",number = 0")
        local_cur.execute(op_sql)
        local_conn.commit()
local_conn.close()
conn.close()
if flag == 1:
    os.system("echo '" + str(time.time()) + " close '>> run.log")
    os.system("sh /volume1/stop.sh")
    # 重启
