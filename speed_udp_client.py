#client
import socket
import time

HOST = '192.168.27.77'
PORT = 7890



def send_speed(HOST, PORT,send_data):
    client = socket.socket(type=socket.SOCK_DGRAM)
    while True:
        send_data = b'8 6'
        # if send_data == "":
        #     break
        client.sendto(send_data,(HOST, PORT))
        print(f'speed sent successfully!')

        time.sleep(0.02)

    # re_data , address = client.recvfrom(1024)
    # print("server: ", re_data.decode('utf-8'))

    client.close()

if __name__ == '__main__':
    send_speed(HOST, PORT)