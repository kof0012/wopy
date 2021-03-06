import pymysql

class SQL():
    #数据库初始化
    def __init__(self):
        #数据库连接相关信息
        hosts    = 'localhost'  
        username = 'root'
        password = '123456'
        database = 'caicai'
        charsets = 'utf8'

        self.connection = False
        try:
            self.conn = pymysql.connect(host = hosts,user = username,passwd = password,db = database,charset = charsets)
            self.cursor = self.conn.cursor()
            self.cursor.execute("set names "+charsets)
        except Exception as e:
            print ("Cannot Connect To Mysql!/n",e)
        else:
            self.connection = True

    def escape(self,string):
        return '%s' % string
    #插入数据到数据库   
    def insert(self,tablename=None,**values):
        tablename = self.escape(tablename)
        if self.connection:
            try:
                if values:
                    _keys = ",".join(self.escape(k) for k in values)
                    _values = ",".join(['%s']*len(values))
                    sql_query = "replace into %s (%s) values (%s)" % (tablename,_keys,_values)
                    self.cursor.execute(sql_query,list(values.values()))
                else:
                    sql_query = "replace into %s default values" % tablename
                    self.cursor.execute(sql_query)
                self.conn.commit()
                return True
            except Exception as e:
                print ("An Error Occured: ",e)
                return False
            
