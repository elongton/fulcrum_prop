import fulcrum_electronics as fe
import busio
import board


i2c_bus = busio.I2C(board.SCL, board.SDA)
angleSensor = fe.Sensor(i2c_bus)
motorController = fe.MotorController(i2c_bus, 7, 500)



sampleFreq = 0.02


def options():
        print('''
        Select your choice:
        (1): Calibrate Sensor
        (2): Set Throttle Range
        (3): Startup Motor
        '''
        )
        choice = input('Choice: ')
        pass


def main():
        options()
        pass
main()