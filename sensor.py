from adafruit_bno055 import BNO055
import statistics
import time
from time import sleep

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