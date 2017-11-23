#coding=utf-8
import sys,time
import MySQLdb,redis
import paramiko
from common.common import Common
from common.getconfigs import GetConfigs

date=time.strftime('%m-%d-%H-%M',time.localtime(time.time()))
xlsx_path=sys.path[0]+'\\result\\'+date+'_backup.xlsx'

config = GetConfigs()
server_name=config.getstr('select_server','server','server')
ip=config.getstr(server_name,'ip','server')
mysql_port=config.getint(server_name,'mysql_port','server')
redis_port=config.getint(server_name,'redis_port','server')

#mysql_tables_list=['user_info','file_info','friend_info','local_user_status']
mysql_tables_list=config.getstr('mysql_tables_list','mysql_table_name','restore_table').split(',')


#connect Mysql
conn = MySQLdb.connect(host=ip,user='root',passwd='qhkj_mysql_987',port=mysql_port,charset='utf8')
conn.select_db('backup_database')
cur = conn.cursor()


def backup():
    ssh=None
    Common.create_xlsx(xlsx_path,mysql_tables_list)
    for mysql_table_name in mysql_tables_list:
        redisdb=0
        if mysql_table_name=='local_user_status':redisdb=1
        r=redis.StrictRedis(host=ip,port=redis_port,db=redisdb,password='qhkj_redis_987',encoding='utf-8')
        comm=Common(ssh,r,cur,mysql_table_name,'backup')
        comm.set_backup_name()
        comm.get_id_list()
        comm.write_xlsx(xlsx_path)
    print '********************************test end**************************************\n\n'

def restore():
    #connect SSH
    ssh_port=config.getint(server_name,'ssh_port','server')
    ssh_user=config.getstr(server_name,'ssh_user','server')
    ssh_password=config.getstr(server_name,'ssh_password','server')
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ip,ssh_port,ssh_user,ssh_password,timeout=2000)
    
    excel_name=['flush_restore_one','flush_restore_all','restore_one','restore_all']
    for i in range(4):
        xlsx_path=sys.path[0]+'\\result\\'+date+'_'+excel_name[i]+'.xlsx'
        Common.create_xlsx(xlsx_path,mysql_tables_list)
        
        flag=0
        for mysql_table_name in mysql_tables_list:
            #define array to store values
            redisdb=0
            if mysql_table_name=='local_user_status':redisdb=1
            r=redis.StrictRedis(host=ip,port=redis_port,db=redisdb,password='qhkj_redis_987',encoding='utf-8')
            comm=Common(ssh,r,cur,mysql_table_name,'restore')
            comm.set_restore_name()
            
            if i==0 or i==2:
                if i==0:r.flushdb()
                print'********************'+excel_name[i]+':'+mysql_table_name+'************************\n'
                comm.restore_table()    
            if (i==1 or i==3) and flag==0:
                if i==1:r.flushdb()
                print'******************************'+excel_name[i]+'*********************************\n'
                comm.restore_table('all')
                flag=1
            
            comm.get_id_list()
            comm.write_xlsx(xlsx_path)   
        print '********************************test end '+str(i+1)+'********************************\n\n'
        

if __name__ == "__main__":

    while(True):
        print'please input your test number:'
        print 'server_name:',server_name
        select=raw_input('0-----exit,1-----backup,2-----restore:')
        if select=='1' :
            backup()
            break
        elif select=='2':
            if server_name=='TestA' and server_name=='TestB':
                print 'not allow restore in TestA and TestB'
                break
            else:
                restore()
            break
        elif select=='0':
            print 'ok,test over'
            break
        else:
            print 'input error,Please input(0-2)'
    cur.close()
    conn.commit()
    conn.close()
 
            
    

     
