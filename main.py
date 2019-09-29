import fulcrum_electronics as fe
from database.db_manager import DBManager
import busio
import board

#initialize values
sampleFreq = 0.02

#initialize objects
i2c_bus = busio.I2C(board.SCL, board.SDA)
angleSensor = fe.Sensor(i2c_bus)
db = DBManager()
motorController = fe.MotorController(i2c_bus, 7, 500, sampleFreq, db.retrieve_fulcrum_values(id=1)[1]+500)

#routines
def options():
        print('''
        Select your choice:
        (1): Quit
        (2): Calibrate Sensor
        (3): Set Throttle Range
        (4): Fulcrum Prop Values
        (5): Startup Motor
        (6): Turn Off Motor
        '''
        )
        optionSwitch()

def optionSwitch():
        choice = input('Choice: ')
        if choice == '1':
                print('exiting')
                pass
        elif choice == '2':
                calibration = angleSensor.calibrate(sampleFreq)
                db.update_calibration(calibration)
                options()
        elif choice == '3':
                [lowerValue, upperValue] = motorController.setThrottleRange()
                db.update_throttle_limits(lowerValue, upperValue)
                options()
        elif choice == '4':
                fulcrumValues = db.retrieve_fulcrum_values(id=1)
                print(f'\nCalibration Offset: {fulcrumValues[0]}')
                print(f'Throttle Low: {fulcrumValues[1]}')
                print(f'Throttle High: {fulcrumValues[2]}')
                input('\nPress return to continue...')
                options()
        elif choice == '5':
                # thread1 = fe.MotorController(i2c_bus, 7, 500)
                motorController.start()
                # x = threading.Thread(target=motorController.startup, args=(sampleFreq, db.retrieve_fulcrum_values(id=1)[1]+500))
                # x.start()
                options()
        elif choice == '6':
                motorController.stopMotor()
                options()
        else:
                print('nothing selected, try again')
                optionSwitch()

def main():
        options()
        pass
main()