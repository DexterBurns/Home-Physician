from Adafruit_PureIO.smbus import SMBus  # pip install adafruit-blinka
from Raspberry_Pi_Master_for_ESP32_I2C_SLAVE.packer import Packer
from Raspberry_Pi_Master_for_ESP32_I2C_SLAVE.unpacker import Unpacker
import time


slave_address = 0x08  # slave address is 4
register = 66  # register to write is 0x01
value = 66


def write_from_rpi_to_esp32():
    try:
        # prepare the data
        packed = None
        with Packer() as packer:
            #packer.write(register)
            packer.write(value)
            packer.end()
            packed = packer.read()
            print(packed)
        # change 1 of SMBus(1) to bus number on your RPI
        with SMBus(1) as smbus:
            smbus.write_bytes(slave_address, bytearray(packed))
    except Exception as e:
        print("ERROR: {}".format(e))
        
def read_from_rpi_to_esp32():
    try:
        # prepare the data
        packed = None
        with Packer() as packer:
            packer.write(value)
            packer.end()
            packed = packer.read()
            print("in packer")

        # change 1 of SMBus(1) to bus number on your RPI
        raw_list = None
        with SMBus(1) as smbus:
            smbus.write_bytes(slave_address, bytearray(packed)) #how would the slave know whether to write or receive?
            time.sleep(0.3)  # wait i2c process the request
            raw_list = list(smbus.read_bytes(slave_address, 5))  # the read_bytes contains the data format: first, length, data, crc8, end bytes
            rawList = smbus.read_byte(slave_address)
            #print(rawList)
            print(raw_list)
            print("in smbus")

        # let's clean received data
        unpacked = None
        with Unpacker() as unpacker:
            print("unpacker 1")
            unpacker.write(raw_list)
            print("unpacker 2")
            unpacked = unpacker.read()
            print("in unpacker")
        return unpacked

    except Exception as e:
        print("ERROR: {}".format(e))

write_from_rpi_to_esp32()
time.sleep(5)
#read_from_rpi_to_esp32()



