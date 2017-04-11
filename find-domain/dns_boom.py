#有一个类
#创建表的函数
#插入数据的函数
#判断是否插入过函数
import pymysql
class Domain():
	"""docstring for domain"""
	def __init__(self,domain_name,domain_ip,table):
		self.table=table
		self.domain_ip=domain_ip
		self.domain_name=domain_name
		print(table)
		#调用创建表的函数
		self.create_table(table)
		if self.isHave(table,domain_ip):
			self.insert_db(table,domain_ip,domain_name)

	def create_table(self,table):
		coon=pymysql.connect(host="localhost",port=3306,user="root",passwd="",database="domain")
		connect=coon.cursor()
		#拆分为['baidu'.'com']
		DM=table.split('.')
		sql_create="create table if not exists "+DM[0]+" (id int auto_increment primary key,domain_ip varchar(100),domain_name varchar(100))"
		connect.execute(sql_create)
		coon.commit()
		coon.close()

	def insert_db(self,table,domain_ip,domain_name):
		coon=pymysql.connect(host="localhost",port=3306,user="root",passwd="",database="domain")
		connect=coon.cursor()
		# print(self.name,self.age,self.city)
		DM=table.split('.')
	
		# sql_insert='insert into "%s" (domain_ip,dmoin_name) values ("%s","%s")' %(DM[0],domain_ip,domain_name)
		# sql_insert="insert into "+DM[0]+" (domain_ip,dmoin_name) values (\''+ domain_ip + "','" + domain_name + "')'"
		sql_insert = 'insert into '+ DM[0]+ ' (domain_ip, domain_name) values (\'' + domain_ip + "', '" + domain_name + "')"

		connect.execute(sql_insert)
		coon.commit()
		coon.close()
	def isHave(self,table,domain_ip):
		#根据Ip去表中查询数据，如果查到了则视为已经插入过了数据
		coon=pymysql.connect(host="localhost",port=3306,user="root",passwd="",database="domain")
		connect=coon.cursor()
		DM=table.split('.')
		# sql_select_ip="select * from '%s' where domain_ip = '%s'" %(DM[0],domain_ip)
		sql_select_ip = 'select * from ' + DM[0] + ' where domain_ip = \'' + domain_ip + "'"
		print(sql_select_ip)
		connect.execute(sql_select_ip)
		result_ip=connect.fetchall()
		#判断是否存在
		if result_ip:
			return False
		else:
			return True
# if __name__ == '__main__':
	# a=Domain('www.sina.com','192.168.1.1','sina.com')
	# def select_db(self,table,domain_ip):
	# 	coon=pymysql.connect(host="localhost",port=3306,user="root",passwd="",database="python")
	# 	connect=coon.cursor()
	# 	while True:
	
	# 		sql_select_ip="select domin_ip from '%s' where id='%d'"%(self.table,i)
	# 		connect.execute(sql_select_ip)
	# 		result_ip=connect.fetchall()
	# 		sql_select_name="select domin_name from '%s' where id='%d'"%(self.table,i)
	# 		connect.execute(sql_select_name)
	# 		result_name=connect.fetchall()
	# 		# print(result)
	# 		coon.commit()
	# 		coon.close()

