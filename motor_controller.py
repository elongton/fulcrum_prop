
from adafruit_pca9685 import PCA9685
from time import sleep
from threading import Thread


class MotorController(PCA9685, Thread):
    def __init__(self, i2c, motorChannel:int, pwmFrequency:int, sampleFreq:float, startupValue:int):
        PCA9685.__init__(self, i2c)
        Thread.__init__(self)
        self.motorChannel = motorChannel
        self.frequency = pwmFrequency
        self.sampleFreq = sampleFreq
        self.startupValue = startupValue
        self.manualValue = 4500
        self.started = True
        self.controller = 1
        
    #override the Thread run method (this is the only one you can override)
    def run(self):
        for x in range(100):
            value = round(x/100 * self.startupValue)
            self.channels[self.motorChannel].duty_cycle = value
            # print(value)
            sleep(self.sampleFreq)
        while self.started:
            if self.controller == 0:
                self.setThrottle(self.startupValue - 300)
            elif self.controller == 1:
                self.setThrottle(self.startupValue)
            elif self.controller == 2:
                self.setThrottle(self.manualValue)
            else:
                self.setThrottle(0)
            sleep(self.sampleFreq)
        print('run loop ended')
        

    def stopMotor(self):
        self.started = False
        self.channels[self.motorChannel].duty_cycle = 0

    def setThrottle(self, value:int):
        self.channels[self.motorChannel].duty_cycle = value

    def setThrottleRange(self):
        print('SET THROTTLE RANGE: ESC must be de-energized.')
        upperValue = input('SET THROTTLE RANGE: Enter upper value: ')
        self.setThrottle(int(upperValue))
        input('SET THROTTLE RANGE: Now energize the ESC and wait for beep.')
        lowerValue = input('SET THROTTLE RANGE: Enter lower value: ')
        self.setThrottle(int(lowerValue))
        return [lowerValue, upperValue]
        