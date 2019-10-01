import fulcrum_electronics as fe
from database.db_manager import DBManager
import threading
from time import sleep
import busio
import board

#initialize values
sampleFreq = 0.02

#initialize objects
i2c_bus = busio.I2C(board.SCL, board.SDA)
angleSensor = fe.Sensor(i2c_bus)
db = DBManager()
motorController = fe.MotorController(i2c_bus, 7, 500)
#routines
def options1():
        print('''
        Select your choice:
        (1): Quit
        (2): Calibrate Sensor
        (3): Set Throttle Range
        (4): Fulcrum Prop Values
        (5): Startup Motor
        '''
        )
        options1Switch()
def options2(motorThread):
        print('''
        Select your choice:
        (1): Turn Off Motor
        (2): Manual Control Mode
        '''
        )
        options2Switch(motorThread)

def options2Switch(motorThread):
        choice = input('Choice: ')
        if choice == '1':
                # motorThread.do_run = False
                # motorThread.join()
                # motorController.stopMotor()
                motorThread.started = False
                options1()

def options1Switch():
        choice = input('Choice: ')
        if choice == '1':
                print('exiting')
                pass
        elif choice == '2':
                calibration = angleSensor.calibrate(sampleFreq)
                db.update_calibration(calibration)
                options1()
        elif choice == '3':
                [lowerValue, upperValue] = motorController.setThrottleRange(sampleFreq)
                db.update_throttle_limits(lowerValue, upperValue)
                options1()
        elif choice == '4':
                fulcrumValues = db.retrieve_fulcrum_values(id=1)
                print(f'\nCalibration Offset: {fulcrumValues[0]}')
                print(f'Throttle Low: {fulcrumValues[1]}')
                print(f'Throttle High: {fulcrumValues[2]}')
                input('\nPress return to continue...')
                options1()
        elif choice == '5':
                # t = threading.Thread(target=motorController.startMotor, args=(sampleFreq, db.retrieve_fulcrum_values(id=1)[1]+500))
                # t.start()
                motorController.start()
                options2(motorController)
        else:
                print('nothing selected, try again')
                options1Switch()


# def startMotor(sampleFreq, startupValue):
#         t = threading.currentThread()
#         for x in range(100):
#                 value = round(x/100 * startupValue)
#                 # self.channels[self.motorChannel].duty_cycle = value
#                 motorController.setThrottle(value)
#                 # print(value)
#                 sleep(sampleFreq)
#         while getattr(t, "do_run", True):
#                 print('worked')
#                 motorController.setThrottle(startupValue)
#                 sleep(sampleFreq)


def main():
        options1()
        pass
main()