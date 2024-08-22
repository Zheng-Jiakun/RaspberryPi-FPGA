import RPi.GPIO as GPIO
import time

class FPGA:
    def __init__(self, pin_config):
        self.pin_fpga_data = pin_config['data']
        self.pin_fpga_addr = pin_config['addr']
        self.pin_fpga_rw = pin_config['rw']
        self.pin_fpga_clk = pin_config['clk']

        if pin_config['mode'] == 'BCM':
            GPIO.setmode(GPIO.BCM)
        else:
            GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.pin_fpga_rw, GPIO.OUT)
        GPIO.setup(self.pin_fpga_clk, GPIO.OUT)
        for pin in self.pin_fpga_addr:
            GPIO.setup(pin, GPIO.OUT)

    def __set_mode(self, mode):
        if mode == "WRITE":
            GPIO.output(self.pin_fpga_rw, GPIO.LOW)
            for pin in self.pin_fpga_data:
                GPIO.setup(pin, GPIO.OUT)
        elif mode == "READ":
            GPIO.output(self.pin_fpga_rw, GPIO.HIGH)
            for pin in self.pin_fpga_data:
                GPIO.setup(pin, GPIO.IN)
        else:
            print("Not correct mode")

    def __set_address(self, addr):
        for n, pin in enumerate(self.pin_fpga_addr):
            if addr & (0x01 << n) == 0x00:
                GPIO.output(pin, GPIO.LOW)
            else:
                GPIO.output(pin, GPIO.HIGH)

    def write_byte(self, addr, data):
        self.__set_mode("WRITE")
        GPIO.output(self.pin_fpga_clk, GPIO.LOW)
        self.__set_address(addr)
        for n, pin in enumerate(self.pin_fpga_data):
            if data & (0x01 << n) == 0x00:
                GPIO.output(pin, GPIO.LOW)
            else:
                GPIO.output(pin, GPIO.HIGH)
        GPIO.output(self.pin_fpga_clk, GPIO.HIGH)
        time.sleep(0.001)
        GPIO.output(self.pin_fpga_clk, GPIO.LOW)
        time.sleep(0.001)

    def read_byte(self, addr):
        data = 0x00
        self.__set_mode("READ")
        GPIO.output(self.pin_fpga_clk, GPIO.LOW)
        time.sleep(0.001)
        self.__set_address(addr)
        GPIO.output(self.pin_fpga_clk, GPIO.HIGH)
        time.sleep(0.001)
        for n, pin in enumerate(self.pin_fpga_data):
            if GPIO.input(pin) == GPIO.HIGH:
                data |= (0x01 << n)
            else:
                data &= ~(0x01 << n)
        GPIO.output(self.pin_fpga_clk, GPIO.LOW)
        return data

    def __del__(self):
        GPIO.cleanup()

if __name__ == "__main__":
    pin_config = {
                    'clk': 21,
                    'rw': 20,
                    'addr': [9, 10, 11, 14, 15, 19],
                    'data': [0, 1, 2, 3, 4, 5, 7, 8],
                    'mode': 'BCM'
                }
    fpga = FPGA(pin_config)

    fpga.write_byte(0x00, 0x12)

    data = fpga.read_byte(0x00)
    print(data)
