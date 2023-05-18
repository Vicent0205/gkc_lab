#client pc


import socket
import time

HOST = '192.168.223.77' #destination ip
PORT = 7890 



def send_speed(HOST, PORT, Lv = 6, Rv = 8):
    client = socket.socket(type=socket.SOCK_DGRAM)

    str_data = str(Rv)+' '+str(Lv) #第一个右轮，第二个左轮
    send_data = str_data.encode()
    # if send_data == "":
    #     break
    client.sendto(send_data,(HOST, PORT))
    # print(f'speed sent successfully! data: ', str_data)

    time.sleep(0.02)

    # re_data , address = client.recvfrom(1024)
    # print("server: ", re_data.decode('utf-8'))

def send_crossing(HOST, PORT, crossing):
    client = socket.socket(type=socket.SOCK_DGRAM)

    str_data = str(crossing) #第一个右轮，第二个左轮
    send_data = str_data.encode()
    # if send_data == "":
    #     break
    client.sendto(send_data,(HOST, PORT))

if __name__ == '__main__':
    while True:
        send_speed(HOST, PORT)