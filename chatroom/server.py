import socket
import json
 
obj = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
obj.bind(('127.0.0.1', 12346))
 
conn_list = []
user_list = []
 
while True:
    try:
        receive_data, client_address = obj.recvfrom(1024)
        js = json.loads(receive_data.decode())
        # 登录消息
        if js['type'] == 'login':
 
            nickname = str(js['nickname'])
            if nickname in user_list:
                obj.sendto(json.dumps({'login': 'fail',
                                       'errormessage': 'the nickname is exists'}).encode(),
                           client_address)
            else:
                # 向其他用户发送通知
                for i in range(len(conn_list)):
                    obj.sendto(json.dumps(
                        {
                            'type': 'message',
                            'message': '[system]' + nickname + '已登录.'
                        }).encode(), conn_list[i])
                user_list.append(nickname)
                conn_list.append(client_address)
                print(nickname, client_address, '登录成功！')
                obj.sendto(json.dumps({'login': 'success',
                                       'nickname': nickname}).encode(), client_address)
 
        # 群发消息
        elif js['type'] == 'broadcast':
            message = js['message']
            nickname = js['nickname']
            for i in range(len(conn_list)):
                obj.sendto(json.dumps(
                    {
                        'type': 'message',
                        'message': nickname + ':' + message
                    }).encode(), conn_list[i])
 
        # 私发消息
        elif js['type'] == 'sendto':
            who = js['who']
            nickname = js['nickname']
            message = js['message']
            # 检查用户是否存在
            if who not in user_list:
                obj.sendto(json.dumps(
                    {
                        'type': 'message',
                        'message': who + ' not exist or not online.please try later.'
                    }).encode(),
                    client_address)
            else:
                obj.sendto(json.dumps(
                    {
                        'type': 'message',
                        'message': nickname + ' whisper to you: ' + message
                    }).encode(),
                    conn_list[user_list.index(who)])
 
        # 查看用户列表
        elif js['type'] == 'catusers':
            users = json.dumps(user_list)
            obj.sendto(json.dumps(
                {
                    'type': 'message',
                    'message': users,
                }).encode(),
                client_address)
 
        # 查看用户IP
        elif js['type'] == 'catip':
            who = js['who']
            if who not in user_list:
                obj.sendto(json.dumps(
                    {
                        'type': 'message',
                        'message': who + ' not exist or not online.please try later.'
                    }).encode(),
                    client_address)
            else:
                addr = json.dumps(conn_list[user_list.index(who)])
                obj.sendto(json.dumps(
                    {
                        'type': 'message',
                        'message': addr,
                    }).encode(),
                    client_address)
 
        # 离线消息
        elif js['type'] == 'offline':
            user_list.remove(js['nickname'])
            conn_list.remove(client_address)
            obj.sendto(
                (js['nickname'] + 'offline.').encode(),
                client_address)
            # 向其他用户发送通知
            for i in range(len(conn_list)):
                obj.sendto(json.dumps(
                    {
                        'type': 'message',
                        'message': '[system]' + nickname + '下线了.'
                    }).encode(), conn_list[i])
 
        # 发送文件请求
        elif js['type'] == 'filequest':
            who = js['who']
            if who not in user_list:
                obj.sendto(json.dumps(
                    {
                        'type': 'message',
                        'message': who + ' not exist or not online.please try later.'
                    }).encode(),
                    client_address)
            else:
                js['send_ip'] = client_address[0]
                js['send_port'] = client_address[1]
                obj.sendto(json.dumps(js).encode(),
                           conn_list[user_list.index(who)])
                print(js['nickname'], 'request to send file to', who)
 
        # 发送文件请求回复
        elif js['type'] == 'fileres':
            who = js['who']
            if js['fileres'] == 'yes':
                js['recv_ip'] = client_address[0]
                js['recv_port'] = client_address[1]
                print(js['nickname'], 'agree to receive file from', js['who'])
            else:
                print(js['nickname'], 'deny to receive file from', js['who'])
            obj.sendto(json.dumps(js).encode(),
                       conn_list[user_list.index(who)])
 
    except Exception as e:
        print(e)