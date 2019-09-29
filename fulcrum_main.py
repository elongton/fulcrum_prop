import fulcrum_electronics as fe
from database.db_manager import DBManager
import database.fulcrum_values as fv
import busio
import board

#initialize values
sampleFreq = 0.02

#initialize objects
# i2c_bus = busio.I2C(board.SCL, board.SDA)
# angleSensor = fe.Sensor(i2c_bus)
# motorController = fe.MotorController(i2c_bus, 7, 500)
db = DBManager()
db.update_calibration(23)
db.update_throttle_limits(200, 300)
print(db.retrieve_fulcrum_values(id=1))

#routines
def options():
        print('''
        Select your choice:
        (1): Calibrate Sensor
        (2): Set Throttle Range
        (3): Startup Motor
        (4): View Fulcrum Prop Settings
        (5): Quit
        '''
        )
        optionSwitch()

def optionSwitch():
        choice = input('Choice: ')
        if choice == '1':
                # angleSensor.calibrate(sampleFreq)
                options()
        elif choice == '2':
                # motorController.setThrottleRange()
                options()
        elif choice == '3':
                print(choice + ' worked')
        elif choice == '4':
                print('exiting')
                pass
        elif choice == '5':
                print('exiting')
                pass
        else:
                print('nothing selected, try again')
                optionSwitch()

def main():
        # options()
        pass
main()