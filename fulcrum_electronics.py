from adafruit_bno055 import BNO055
from adafruit_pca9685 import PCA9685
import statistics
from time import sleep
import time
import threading


class Sensor(BNO055):
    def __init__(self, i2c):
        super().__init__(i2c)
        self.calibratedAngle = 0
        
    def calibrate(self, sampleFreq:float):
        print('CALIBRATION: Let rod hang down, perpendicular to the floor')
        input('Press return to continue...')
        print('CALIBRATION: Now calibrating BNO055 IMU - Angle Sensor')
        timedCalibration = 0
        t0 = time.time()
        angleList = []
        while timedCalibration < 5:
            angleList.append(self.euler[2])
            sleep(sampleFreq)
            timedCalibration = time.time() - t0
        avgAngle = statistics.mean(angleList)
        self.calibratedAngle = 0 - avgAngle
        print('Average sensed angle was: {}'.format(avgAngle))
        print('Now put back in safety position.')
        input('Press return to continue...')
        return self.calibratedAngle
    
    def sensedAngle(self):
        return self.euler[2] + self.calibratedAngle
    
    def sensedRate(self):
        return self.euler[3]

class MotorController(PCA9685, threading.Thread):
# class MotorController(PCA9685):
    def __init__(self, i2c, motorChannel:int, pwmFrequency:int):
        PCA9685.__init__(self, i2c)
        threading.Thread.__init__(self)
        self.i2c = i2c
        self.motorChannel = motorChannel
        self.pwmFrequency = pwmFrequency
        self.startupSequence = False
        self.started = True



    def run(self):
        print('starting')
        i=0
        while self.started:
            i = i+30
            # print(i)
            self.setThrottle(i)
            sleep(0.02)
        print('finished')

    def stopMotor(self):
        self.startupSequence = False
        self.channels[self.motorChannel].duty_cycle = 0

    def setThrottle(self, value:int):
        self.channels[self.motorChannel].duty_cycle = value

    def setThrottleRange(self, sampleFreq):
        print('SET THROTTLE RANGE: ESC must be de-energized.')
        upperValue = input('SET THROTTLE RANGE: Enter upper value: ')
        upperValueThread = threading.Thread(target=self.constantThrottle, args=(sampleFreq, int(upperValue)))
        upperValueThread.start()
        # self.setThrottle(int(upperValue))
        input('SET THROTTLE RANGE: Now energize the ESC and wait for beep.')
        lowerValue = input('SET THROTTLE RANGE: Enter lower value: ')
        upperValueThread.do_run = False
        upperValueThread.join()
        lowerValueThread = threading.Thread(target=self.constantThrottle, args=(sampleFreq, int(lowerValue)))
        lowerValueThread.start()
        # self.setThrottle(int(lowerValue))
        input('SET THROTTLE RANGE: Throttle range set, press enter to turn off signal to ESC.')
        lowerValueThread.do_run = False
        lowerValueThread.join()
        return [lowerValue, upperValue]
        

    def startMotor(self, sampleFreq, startupValue):
        t = threading.currentThread()
        self.startupSequence = True
        for x in range(100):
            value = round(x/100 * startupValue)
            self.setThrottle(value)
            sleep(sampleFreq)
        print('ramp up complete')
        while getattr(t, "do_run", True):
            self.setThrottle(startupValue)
            sleep(sampleFreq)
        print('motor startup stopped')
            
    def constantThrottle(self, sampleFreq, value):
        t = threading.current_thread()
        print(value)
        while getattr(t, "do_run", True):
            self.setThrottle(value)
            sleep(sampleFreq)
        # sleep(sampleFreq)
        print(f'quit - {value}')
