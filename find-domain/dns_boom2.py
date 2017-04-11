import pymysql,threading,dns.resolver,time
import os
from multiprocessing import Queue
from dns_boom import Domain
#同步-》线程按顺序做
#异步-》线程互不干扰，自己运行不需等待
class DNSBrute(object):
	def __init__(self,domain_name,thread_NUM):
		#开始的域名格式:baidu.com
		self.domain_name=domain_name
		#开始的线程数量thread_NUM
		self.thread_count=self.thread_NUM=thread_NUM
		# scan_count:扫描过得数量
		#found_count:扫描到域名的数量
		self.scan_count=self.found_count =0
		#线程锁，因为有许多个线程同时操作，所以要一个线程锁
		self.lock=threading.Lock()
		#保存DNS解析对象的列表(简单方法)，一个DNS对象（里边有DNS列表里的DNS地址）解析一个线程（拿到map.sian.com）防止多个线程对一个对象的影响
		self.resolvers=[dns.resolver.Resolver() for _ in range(thread_NUM)]
		self.load_dns_servers()
		self.load_subnames()
		#查找出来IP地址的字典
		self.ip_dict={}
		self.STOP_ME=False
		# 查询结果出来的列表
		# 在查询结束之后保存数据库
		self.result=[]
		# for x in range(thread_NUM):
		# 	#创建一个DNS解析对象
		# 	new_resolver=dns.resolver.Resolver()
		# 	#添加到列表当中
		# 	self.resolver.append(new_resolver)
	
	#第一个函数从dnsservers.txt读取内容保存到列表当中
	#第二个函数从subname.txt.读取内容保存到Queue
	def load_dns_servers(self):
		dns_servers=[]
		try:
			f=open('./dns_servers.txt','r')
			# print(a)
		finally:
			if f:
				for x in f:
					server=x.strip()
					#将去掉空格的DNS地址保存到数组当当中
					dns_servers.append(server)
		# print(dns_servers)
		#保存成全局通用的
		self.dns_servers=dns_servers
		self.dns_count=len(dns_servers)


	def load_subnames(self):
		self.queue=	Queue()
		with open('./subnames.txt','r') as f :
			for x in f:
				subname=x.strip()
				a=self.queue.put(subname)
#提交查询二级域名的函数
	def scan(self):
		#获取当前线程的名字.name
		thread_id=int(threading.currentThread().getName())
		#每一个线程都对应一个解析对象,每一个解析对象都对应一个新的DNS列表
		self.resolvers[thread_id].nameservers.insert(0,self.dns_servers[thread_id% self.dns_count])#ip列变
		self.resolvers[thread_id].lifetime=10.0#不允许四舍五入
		self.resolvers[thread_id].timeout=10.0
		

		while self.queue.qsize() >0 and not self.STOP_ME:#获取队列任务数的函数,
		#STOP_ME出错仍能继续
		# queue->www,map
		# domain_name->baidu.com
		# resolver->查询百度www.baidu.com
			sub=self.queue.get()
			# 循环三次是因为解析对象中有三个dns服务器地址
			for _ in range(3):
				sub_domain=sub + '.' + self.domain_name#拼接新的二级域名map.baidu.com
				#抛出异常函数
				try:
					#通过DNS查询二级是否正确
					answers=self.resolvers[thread_id].query(sub_domain)#返回一个列表
					if answers:
						ips=','.join(answer.address for answer in answers)#用逗号拼接这些IP
						# 开启线程锁,一个DNS去解析的时候防止另外两个去解析
						self.lock.acquire()
						#发现的数量加1
						self.found_count+=1
						print(self.found_count)
						print(sub_domain,ips)
						self.result.append((sub_domain,ips))#以元组形式存储
						# print(result.append)
						self.lock.release()#释放
				except Exception as e:
					pass
			print(self.found_count,self.queue.qsize())
		self.lock.acquire()#子线程执行的函数，表示你的线程执行完毕
		self.thread_count-=1
		self.lock.release()
	
	def run(self):
		for x in range(self.thread_NUM):
			thread=threading.Thread(target=self.scan,name=str(x))
			#这个线程会在主线程结束的时候释放掉
			#若线程中在创建线程的时候当父线程结束，但子线程没结束，子线程会丢失，所以要强制使得子进程结束
			thread.setDaemon(True)
			thread.start()
			#折断代码只有用户主动退出的时候才结束
		while self.thread_count >1:
			try:
				time.sleep(0.5)
				#keyboardinterrupt 键盘 ctrl+c退出
			except KeyboardInterrupt as e:
				self.STOP_ME=True
		for x in self.result :
			print(x)
			a=Domain(x[0],x[1],self.domain_name)
			# thread.join()
	# 		f=open('./subnames.txt','r')
	# 		# print(a)
	# 	finally:
	# 		if f:
	# 			for x in f:
	# 			print(a)
	# 			f.close()
	# def threading_run():
		
if __name__ == '__main__':
	d=DNSBrute('oneasp.com',80)
	d.run()
# 	d.load_dns_servers()
# 	d.load_subnames()
# 	subnames()
