import random
import socket
import threading
import atexit

from napster.core.constants import MESSAGE_SIZE
from napster.core.udp.messages import ConvertToMessageType


class UDPServer:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.settimeout(0) # use non-blocking mode
        self.converter = ConvertToMessageType()
        self.queue_lock = threading.Lock()
        self.message_queue = []
        self.threads = []
        self.thread_kill_event = threading.Event()
        atexit.register(self.cleanup) # clean up threads on exit

    def __handle_message_queue(self, func):
        def process_queue():
            # print("UDP server message handler thread started")
            while self.thread_kill_event.is_set() is False:
                if self.message_queue:
                    with self.queue_lock:
                        idx = random.randint(0, len(self.message_queue) - 1)
                        message = self.message_queue.pop(idx)
                    func(self.sock, message[0], message[1])
            # print("UDP server message handler thread ended")

        thread = threading.Thread(target=process_queue, daemon=True)
        thread.name = f"UDPServerMessageHandlerThread"
        thread.start()
        self.threads.append(thread)


    def __run_receiver(self):
        def run():
            self.sock.bind((self.host, self.port))
            # print(f"UDP server listening on {self.host}:{self.port}")
            while self.thread_kill_event.is_set() is False:
                try:
                    # buffer size is MESSAGE_SIZE + some extra
                    data, addr = self.sock.recvfrom(MESSAGE_SIZE + 1024)
                    message = data.decode('utf-8')
                    with self.queue_lock:
                        self.message_queue.append((self.converter.parse_message(message), addr))
                except socket.error:
                    pass
            # print("UDP server receiver thread exiting")

        thread = threading.Thread(target=run, daemon=True)
        thread.name = "UDPServerReceiverThread"
        thread.start()
        self.threads.append(thread)

    def start(self, func):
        self.__handle_message_queue(func)
        self.__run_receiver()

    def cleanup(self):
        self.thread_kill_event.set() # signal threads to exit
        for thread in self.threads:
            thread.join()




class UDPClient:
    def __init__(self, server_ip: str, server_port: int):
        self.server_ip = server_ip
        self.server_port = server_port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.settimeout(0) # use non-blocking mode
        self.converter = ConvertToMessageType()
        self.message_queue = []
        self.queue_lock = threading.Lock()
        self.threads = []
        self.thread_kill_event = threading.Event()
        atexit.register(self.cleanup) # clean up threads on exit

    def send_message(self, message: str):
        self.sock.sendto(message.encode('utf-8'), (self.server_ip, self.server_port))

    def __handle_message_queue(self, func):
        def process_queue():
            # print("UDP client message handler thread started")
            while self.thread_kill_event.is_set() is False:
                if self.message_queue:
                    with self.queue_lock:
                        idx = random.randint(0, len(self.message_queue) - 1)
                        message = self.message_queue.pop(idx)
                    func(message[0], message[1])
            # print("UDP client message handler thread ended")

        thread = threading.Thread(target=process_queue, daemon=True)
        thread.name = "UDPClientMessageHandlerThread"
        thread.start()
        self.threads.append(thread)

    def __receive_message(self):
        def run():
            # print("UDP client receiver thread started")
            while self.thread_kill_event.is_set() is False:
                try:
                    data, addr = self.sock.recvfrom(MESSAGE_SIZE + 1024)
                    message = data.decode('utf-8')
                    with self.queue_lock:
                        self.message_queue.append((self.converter.parse_message(message), addr))
                except socket.error:
                    pass
            # print("UDP client receiver thread ended")

        thread = threading.Thread(target=run, daemon=True)
        thread.name = "UDPClientReceiverThread"
        thread.start()
        self.threads.append(thread)

    def start_receiver(self, func):
        self.__handle_message_queue(func)
        self.__receive_message()

    def cleanup(self):
        self.thread_kill_event.set() # signal threads to exit
        for thread in self.threads:
            thread.join()
