from motor_controller import MotorController
from sensor import Sensor
from database.db_manager import DBManager
import busio
import board

#initialize
sampleFreq = 0.02
db = DBManager()
i2c_bus = busio.I2C(board.SCL, board.SDA)
angleSensor = Sensor(i2c_bus)
motorStartupValue = db.retrieve_fulcrum_values(id=1)[1]+500
motorController = MotorController(i2c_bus, 7, 500, sampleFreq, motorStartupValue)

#routines
def options(step):
        if step == 0:
                print('''
                Select your choice:
                (1): Quit
                (2): Calibrate Sensor
                (3): Set Throttle Range
                (4): Fulcrum Prop Values
                (5): Startup Motor
                (6): Kill Motor
                '''
                )
                optionSwitch(0)
        elif step == 1:
                print('''
                Select your choice:
                (1): Manual Mode
                (2): Pause Motor
                '''
                )
                optionSwitch(1)

def optionSwitch(step):
        choice = input('Choice: ')
        if step == 0:
                if choice == '1':
                        print('exiting')
                        pass
                elif choice == '2':
                        calibration = angleSensor.calibrate(sampleFreq)
                        db.update_calibration(calibration)
                        options(0)
                elif choice == '3':
                        [lowerValue, upperValue] = motorController.setThrottleRange()
                        db.update_throttle_limits(lowerValue, upperValue)
                        options(0)
                elif choice == '4':
                        fulcrumValues = db.retrieve_fulcrum_values(id=1)
                        print(f'\nCalibration Offset: {fulcrumValues[0]}')
                        print(f'Throttle Low: {fulcrumValues[1]}')
                        print(f'Throttle High: {fulcrumValues[2]}')
                        input('\nPress return to continue...')
                        options(0)
                elif choice == '5':
                        if motorController.is_alive():
                                motorController.controller = 1
                        else:
                                motorController.start()
                        options(1)
                elif choice == '6':
                        motorController.stopMotor()
                        pass
                else:
                        print('nothing selected, try again')
                        optionSwitch(0)
        elif step == 1:
                if choice == '1':
                        motorController.controller = 2 #manual controller
                        controllerManualInput = motorController.manualValue
                        while controllerManualInput != 'q':
                                motorController.manualValue = int(controllerManualInput)
                                controllerManualInput = input("You may input a throttle value - 4000 to 6500, 'q' will quit: ")
                        options(1)
                elif choice == '2':
                        motorController.controller = 0 #stop
                        options(0)
                else:
                        print('nothing selected, try again')
                        optionSwitch(0)
def main():
        options(0)
        pass
main()
