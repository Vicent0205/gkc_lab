import socket
import time
import numpy as np
import cv2 


def bytes2cv(im):
    return cv2.imdecode(np.array(bytearray(im), dtype='uint8'), cv2.IMREAD_UNCHANGED)  # 从二进制图片数据中读取


def cv2bytes(im):
    return np.array(cv2.imencode('.png', im)[1]).tobytes()


class PID_Controller:
    def __init__(self,kp,ki,kd,output_min=-20,output_max=20):
        # 初始化PID的三个参数，以及误差项
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.error = 0 # 误差
        self.last_error = 0 # 上一时刻误差
        self.error_sum = 0 # 误差累加，代替积分
        self.error_diff = 0 # 误差差分，代替微分
        
        # 初始化最大输出与最小输出
        self.output_min = output_min
        self.output_max = output_max
        self.output = 0 # 初始化控制器输出

    def constrain(self, output):
        # 控制器输出阈值限制
        print(f'i sum: {self.error_sum}')
        if self.error_sum > 8:
            self.error_sum = 0
        if output > self.output_max:
            output = self.output_max
        elif output < self.output_min:
            output = self.output_min
        else:
            output = output
        return output

    def get_output(self, error):
        # 使用位置式PID获取输出
        self.error = error
        self.error_sum += self.error # 误差累加
        self.error_diff = self.error - self.last_error # 误差差分
        self.last_error = self.error

        output = self.kp * self.error + self.ki * self.error_sum + self.kd * self.error_diff
        self.output = self.constrain(output)

        return self.output