import socket
import threading
import json
import os
from cmd import Cmd
 
 
class Client(Cmd):
    """
    客户端
    """
    prompt = '>>>'
    intro = '[Welcome] 简易聊天室客户端(Cli版)\n' + '[Welcome] 输入help来获取帮助\n'
    buffersize = 1024
 
    def __init__(self, host):
        """
        构造
        """
        super().__init__()
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # self.__id = None
        self.__nickname = None
        self.__host = host
        self.thread_recv = None
        self.threadisalive = False
        # 是否在接收文件
        self.recvfile = False
        # 是否在发送文件
        self.sendfile = False
        self.filesize = None
        self.sendfilesize = None
 
        # 接收文件包计数
        self.filecount = None
        # 接收文件名
        self.filename = None
        # 发送文件名
        self.sendfilename = None
 
        # 发送者
        self.filefrom = None
        # 接收者
        self.fileto = None
 
        # 接收文件流
        self.file_recv = None
        # 发送文件流
        self.file_send = None
 
        # 接收文件地址
        self.filefrom_addr = None
        # 发送文件地址
        self.fileto_addr = None
 
    def __receive_message_thread(self):
        """
        接受消息线程
        """
        while self.threadisalive:
            # noinspection PyBroadException
            try:
                buffer, addr = self.__socket.recvfrom(1024)
                '''
                文件流由发送端直接发送，不经过服务器，故当发送端发来的消息时，将收到的数据存入文件
                '''
                if (addr != self.__host) & (addr == self.filefrom_addr) & self.recvfile:
                    self.file_recv.write(buffer)
                    self.filecount += 1
                    if self.filecount * 1024 >= self.filesize:
                        self.file_recv.close()
                        print(self.filename, 'is received.')
                        self.recvfile = False
                    continue
 
                js = json.loads(buffer.decode())
 
                # 若接收的数据为消息信息，则显示
                if js['type'] == 'message':
                    print(js['message'])
 
                # 若接收的数据为文件发送请求，则存储文件信息，并显示
                elif js['type'] == 'filequest':
                    if self.recvfile:
                        self.__socket.sendto(json.dumps({
                            'type': 'fileres',
                            'fileres': 'no',
                            'nickname': self.__nickname,
                            'who': js['nickname'],
                            'errormessage': 'is transfroming files.',
                        }).encode(), self.__host)
                        continue
                    filename = js['filename']
                    who = js['nickname']
                    filesize = js['filesize']
                    self.recvfile = True
                    self.filesize = filesize
                    self.filename = filename
                    self.filecount = 0
                    self.filefrom = who
                    self.filefrom_addr = (js['send_ip'], js['send_port'])
 
                    print('[system]:', who, ' send a file(',
                          filename, ') to you. receive? ')
 
                # 接受的数据为请求回复，若同意接收则存储服务器发来的接收方的地址，并开启发送线程
                elif js['type'] == 'fileres':
                    if js['fileres'] == 'yes':
                        print(js['recv_ip'], js['recv_port'])
                        self.fileto_addr = (js['recv_ip'], js['recv_port'])
                        thread = threading.Thread(
                            target=self.__send_file_thread)
                        thread.start()
                    else:
                        print(js['nickname'], js['errormessage'])
                        self.sendfile = False
 
            except Exception as e:
                print(e)
                print('[Client] 无法从服务器获取数据')
 
    def __send_broadcast_message_thread(self, message):
        """
        发送广播消息线程
        :param message: 消息内容
        """
        self.__socket.sendto(json.dumps({
            'type': 'broadcast',
            'nickname': self.__nickname,
            'message': message,
        }).encode(), self.__host)
 
    def __send_file_thread(self):
        """
        发送文件线程
        :param message: 消息内容
        """
        filecount = 0
        print('[system]', 'sending the file...')
        while filecount * 1024 <= self.sendfilesize:
            self.__socket.sendto(
                self.file_send.read(1024), self.fileto_addr)
            filecount += 1
        self.file_send.close()
        self.sendfile = False
        print('[system]', 'the file is sended.')
 
    def __send_whisper_message_thread(self, who, message):
        """
        发送私发消息线程
        :param message: 消息内容
        """
        self.__socket.sendto(json.dumps({
            'type': 'sendto',
            'who': who,
            'nickname': self.__nickname,
            'message': message
        }).encode(), self.__host)
 
    def send_exit(self):
        self.__socket.sendto(json.dumps({
            'type': 'offline',
            'nickname': self.__nickname,
        }).encode(), self.__host)
 
 
    def start(self):
        """
        启动客户端
        """
        self.cmdloop()
 
    def do_login(self, args):
        """
        登录聊天室
        :param args: 参数
        """
        nickname = args.split(' ')[0]
 
        # 将昵称发送给服务器，获取用户id
        self.__socket.sendto(json.dumps({
            'type': 'login',
            'nickname': nickname,
        }).encode(), self.__host)
        # 尝试接受数据
 
        buffer = self.__socket.recvfrom(1300)[0].decode()
        obj = json.loads(buffer)
        if obj['login'] == 'success':
            self.__nickname = nickname
            print('[Client] 成功登录到聊天室')
            self.threadisalive = True
            # 开启子线程用于接受数据
            self.thread_recv = threading.Thread(
                target=self.__receive_message_thread)
            self.thread_recv.setDaemon(True)
            self.thread_recv.start()
        else:
            print('[Client] 无法登录到聊天室', obj['errormessage'])
 
    def do_send(self, args):
        """
        发送消息
        :param args: 参数
        """
        if self.__nickname is None:
            print('请先登录！login nickname')
            return
        message = args
        # 开启子线程用于发送数据
        thread = threading.Thread(
            target=self.__send_broadcast_message_thread, args=(message, ))
        thread.setDaemon(True)
        thread.start()
 
    def do_sendto(self, args):
        """
        发送私发消息
        :param args: 参数
        """
        if self.__nickname is None:
            print('请先登录！login nickname')
            return
        who = args.split(' ')[0]
        message = args.split(' ')[1]
        # # 显示自己发送的消息
        # print('[' + str(self.__nickname) + '(' + str(self.__id) + ')' + ']', message)
        # 开启子线程用于发送数据
        thread = threading.Thread(
            target=self.__send_whisper_message_thread, args=(who, message))
        thread.setDaemon(True)
        thread.start()
 
    def do_catusers(self, arg):
        if self.__nickname is None:
            print('请先登录！login nickname')
            return
        catmessage = json.dumps({'type': 'catusers'})
        self.__socket.sendto(catmessage.encode(), self.__host)
 
    def do_catip(self, args):
        if self.__nickname is None:
            print('请先登录！login nickname')
            return
        who = args
        catipmessage = json.dumps({'type': 'catip', 'who': who})
        self.__socket.sendto(catipmessage.encode(), self.__host)
 
    def do_help(self, arg):
        """
        帮助
        :param arg: 参数
        """
        command = arg.split(' ')[0]
        if command == '':
            print('[Help] login nickname - 登录到聊天室，nickname是你选择的昵称')
            print('[Help] send message - 发送消息，message是你输入的消息')
            print('[Help] sendto who message - 私发消息，who是用户名，message是你输入的消息')
            print('[Help] catusers - 查看所有用户')
            print('[Help] catip who - 查看用户IP，who为用户名')
            print('[Help] sendfile who filedir - 向某用户发送文件，who为用户名，filedir为文件路径')
            print('[Help] getfile filename who yes/no - 接收文件，filename 为文件名,who为发送者，yes/no为是否接收')
        elif command == 'login':
            print('[Help] login nickname - 登录到聊天室，nickname是你选择的昵称')
        elif command == 'send':
            print('[Help] send message - 发送消息，message是你输入的消息')
        elif command == 'sendto':
            print('[Help] sendto who message - 发送私发消息，message是你输入的消息')
        else:
            print('[Help] 没有查询到你想要了解的指令')
 
    def do_exit(self, arg):  # 以do_*开头为命令
        print("Exit")
        self.send_exit()
        try:
            self.threadisalive = False
            self.thread_recv.join()
        except Exception as e:
            print(e)
        # self.__socket.close()
 
    def do_sendfile(self, args):
        who = args.split(' ')[0]
        filepath = args.split(' ')[1]
        filename = filepath.split('\\')[-1]
        # 判断是否在发送文件
        if self.sendfile:
            print('you are sending files, please try later.')
            return
        if not os.path.exists(filepath):
            print('the file is not exist.')
            return
        filesize = os.path.getsize(filepath)
        # print(who, filename, filesize)
 
        self.sendfile = True
        self.fileto = who
        self.sendfilename = filename
        self.sendfilesize = filesize
        self.file_send = open(filepath, 'rb')
 
        self.__socket.sendto(json.dumps({
            'type': 'filequest',
            'nickname': self.__nickname,
            'filename': self.sendfilename,
            'filesize': self.sendfilesize,
            'who': self.fileto,
            'send_ip': '',
            'send_port': '',
        }).encode(), self.__host)
 
        print('request send...')
 
        # fileres = self.__socket.recvfrom(1024)[0].decode()
        # js = json.loads(fileres)
 
    def do_getfile(self, args):
        filename = args.split(' ')[0]
        who = args.split(' ')[1]
        ch = args.split(' ')[2]
        # print(self.filename is not None, filename, self.filename, who, self.filefrom)
        if (self.filename is not None) & (filename == self.filename) & (who == self.filefrom):
            if ch == 'yes':
                self.file_recv = open(self.filename, 'wb')
                self.__socket.sendto(json.dumps({
                    'type': 'fileres',
                    'fileres': 'yes',
                    'nickname': self.__nickname,
                    'who': who,
                    'recv_ip': '',
                    'recv_port': '',
                }).encode(), self.__host)
                print('you agree to reveive the file(', filename, ') from', who)
 
            else:
                self.__socket.sendto(json.dumps({
                    'type': 'fileres',
                    'fileres': 'no',
                    'nickname': self.__nickname,
                    'errormessage': 'deny the file.',
                    'who': who,
                    'recv_ip': '',
                    'recv_port': '',
                }).encode(), self.__host)
                print('you deny to reveive the file(', filename, ') from', who)
                self.recvfile = False
        else:
            print('the name or sender of the file is wrong.')
 
 
c = Client(('127.0.0.1', 12346))
c.start()