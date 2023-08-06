import pymysql


class sql:
    def lianjie_sql(self, sql_shujuku_name, sql_yuju,sqlserver):
        '''
        :param sql_shujuku_name:
        :param sql_yuju:
        :return:
        # self.sql_ip=sql_ip
        # self.sql_name=sql_name
        # self.sql_paword=sql_pasword
        '''

        sql=sqlserver
        '''打开数据库连接'''
        db = pymysql.connect(sql["adress"], sql["name"], sql["password"], sql_shujuku_name, charset='utf8')
        '''使用cursor()方法获取操作游标'''
        cursor = db.cursor()
        '''执行sql语句'''
        cursor.execute(sql_yuju)
        '''
        #获取一行输出结果
        data = cursor.fetchone()

        #获取输出结果
        #data_one = cursor.fetchone()
        #data_many = cursor.fetchmany()
        '''
        data_all = cursor.fetchall()
        '''关闭数据库连接'''
        db.close()
        return data_all



if __name__ == "__main__":
    sql_18 = {
        "adress": "39.107.239.18",
        "name": "root",
        "password": "wdtx.2016"

    }
    go = sql()
    sql_a = "SELECT SUM(run_time),SUM(pace)/COUNT(run_time),SUM(run_km) FROM `vd_attendance`"
    aa = go.lianjie_sql("vd_183run", sql_a,sql_18)
    pace = aa[0][1]
    run_time = aa[0][0]
    run_km = aa[0][2]
    print("数据报表，平均配速", int(pace / 60), "分", int(pace % 60), "秒")
    print("数据报表，总时长", int(run_time / 3600), "小时", int(int(run_time % 3600) / 60), "分", int(run_time % 60), "秒")
    print("数据报表，总距离", run_km, "公里")