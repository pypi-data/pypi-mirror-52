import logging
from socket import socket, timeout
import threading


BIND_IP = '0.0.0.0'

class HoneyPot(object):

	def __init__(self, ports, log_filepath):

		if len(ports) < 1:
			raise Exception(" no ports. ")

		self.ports =ports
		self.log_filepath = log_filepath
		self.listener_threads = {}
		self.logger = self.prepare_logger()

		self.logger.info("Emulet Initializing.....")
		self.logger.info("Ports: %s" % self.ports)
		self.logger.info("Log_filepath: %s" % self.log_filepath)

	def handel_connection(self, client_socket, port, ip, remote_ports):
		self.logger.info("%d : Listening on %s:%s: " %(remote_ports, ip, port))
		client_socket.settimeout(3)
		try:
			data = client_socket.recv(64)
			self.logger.info("%d: %s:%s: %s" %(remote_ports, ip, port, data))
			client_socket.send("Access denied.\n".encode('utf8'))
		except timeout:
			pass

		client_socket.close()

	def start_new_listener_thread(self, port):
		#create new listener
		listener = socket() # Defaults (socket.AF_INET, socket,SOCK_STREAM)
		listener.bind((BIND_IP, int(port)))
		listener.listen(5)
		while True:
			client, addr =listener.accept()
			client_handler = threading.Thread(target=self.handel_connection, args=(client, port,  addr[0], addr[1]))
			client_handler.start()
	def start_listening(self):
		for port in self.ports:
			self.listener_threads[port] = threading.Thread(target=self.start_new_listener_thread, args=(port,))
			self.listener_threads[port].start()

	def run(self):
		self.start_listening()
			# while True:
			# 	pass
	def prepare_logger(self):

		logging.basicConfig(level=logging.DEBUG,
							format='%(asctime)s %(levelname)-8s %(message)s',
							datefmt='%Y-%m-%d %H-%M-%s ',
							filename=self.log_filepath,
							filemode='w')
		logger = logging.getLogger(__name__)

		console_handler = logging.StreamHandler()
		console_handler.setLevel(logging.DEBUG)
		logger.addHandler(console_handler)
		return logger