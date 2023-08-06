'''不要随意修改类名和参数名，谁改谁背锅！！！！'''
__version__ = '0.0.7'
__metaclass__ = type
__all__ = [
    'car', 'robot'
]
'''通过固定的文件夹判断设备的种类'''

import os

if os.path.exists('/home/pi/human') == True:
    from ddcmaker import robot
    Rb = robot.robot()

if os.path.exists('/home/pi/Car') == True:
    from ddcmaker import car
    Ca = car.car()


class Robot(object):

    @staticmethod
    def left(step):
        Rb.left(step)

    @staticmethod
    def right(step):
        Rb.right(step)

    @staticmethod
    def forward(step):
        Rb.forward(step)

    @staticmethod
    def backward(step):
        Rb.backward(step)

    @staticmethod
    def up(step):
        Rb.up(step)

    @staticmethod
    def down(step):
        Rb.down(step)

    @staticmethod
    def check(step):
        Rb.check(step)

    @staticmethod
    def circle(step, radius):
        Rb.circle(step, radius)

    @staticmethod
    def nod(step):
        Rb.nod(step)

    @staticmethod
    def shaking_head(step):
        Rb.shaking_head(step)


class Car(object):

    @staticmethod
    def left(step):
        Ca.left(step)

    @staticmethod
    def right(step):
        Ca.right(step)

    @staticmethod
    def forward(step):
        Ca.forward(step)

    @staticmethod
    def backward(step):
        Ca.backward(step)
