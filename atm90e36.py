import spidev
from atm90e36_registers import *

import time
import struct
import binascii
__write__ = False
__read__ = True
class ATM90E36_SPI:

    '''       
    spi - hardware or software SPI implementation
    cs - Chip Select pin
    '''

    def __init__(self, spi):
        self.spi = spi
        self.init_config()
    '''
    rw - True - read, False - write
    address - register to operate
    val - value to write (if any)
    '''

    def comm_atm90(self, RW, address, val):
        # switch MSB and LSB of value
        read_buf = bytearray(2)
        write_buf = bytearray(4)
        # Set read write flag
        address |= RW << 15

        if(RW): # 1 as MSB marks a read
            struct.pack_into('>H',read_buf,0,address)
            ''' Must wait 4 us for data to become valid '''
            time.sleep(10e-6)
            # Write address
            read_res = self.spi.xfer3(read_buf,2)
            return read_res
        else: #0 as MSB and 32 clock cycles marks a write
            struct.pack_into('>H',write_buf,0,address)
            struct.pack_into('>H',write_buf,2,val)
            self.spi.xfer(write_buf)# write all the bytes
    
    def init_config(self):
        self.comm_atm90(__write__, SoftReset, 0x789A)   # Perform soft reset
        self.comm_atm90(__write__, FuncEn0, 0x0000)     # Voltage sag
        self.comm_atm90(__write__, FuncEn1, 0x0000)     # Voltage sag
        self.comm_atm90(__write__, SagTh, 0x0001)       # Voltage sag threshold

        """ SagTh = Vth * 100 * sqrt(2) / (2 * Ugain / 32768) """
  
        #Set metering config values (CONFIG)
        self.comm_atm90(__write__, ConfigStart, 0x5678) # Metering calibration startup 
        self.comm_atm90(__write__, PLconstH, 0x0861)    # PL Constant MSB (default)
        self.comm_atm90(__write__, PLconstL, 0xC468)    # PL Constant LSB (default)
        self.comm_atm90(__write__, MMode0, 0x1087)      # Mode Config (60 Hz, 3P4W)
        self.comm_atm90(__write__, MMode1, 0x1500)      # 0x5555 (x2) # 0x0000 (1x)
        self.comm_atm90(__write__, PStartTh, 0x0000)    # Active Startup Power Threshold
        self.comm_atm90(__write__, QStartTh, 0x0000)    # Reactive Startup Power Threshold
        self.comm_atm90(__write__, SStartTh, 0x0000)    # Apparent Startup Power Threshold
        self.comm_atm90(__write__, PPhaseTh, 0x0000)    # Active Phase Threshold
        self.comm_atm90(__write__, QPhaseTh, 0x0000)    # Reactive Phase Threshold
        self.comm_atm90(__write__, SPhaseTh, 0x0000)    # Apparent  Phase Threshold
        self.comm_atm90(__write__, CSZero, 0x4741)      # Checksum 0

        #Set metering calibration values (CALIBRATION)
        self.comm_atm90(__write__, CalStart, 0x5678)    # Metering calibration startup 
        self.comm_atm90(__write__, GainA, 0x0000)       # Line calibration gain
        self.comm_atm90(__write__, PhiA, 0x0000)        # Line calibration angle
        self.comm_atm90(__write__, GainB, 0x0000)       # Line calibration gain
        self.comm_atm90(__write__, PhiB, 0x0000)        # Line calibration angle
        self.comm_atm90(__write__, GainC, 0x0000)       # Line calibration gain
        self.comm_atm90(__write__, PhiC, 0x0000)        # Line calibration angle
        self.comm_atm90(__write__, PoffsetA, 0x0000)    # A line active power offset
        self.comm_atm90(__write__, QoffsetA, 0x0000)    # A line reactive power offset
        self.comm_atm90(__write__, PoffsetB, 0x0000)    # B line active power offset
        self.comm_atm90(__write__, QoffsetB, 0x0000)    # B line reactive power offset
        self.comm_atm90(__write__, PoffsetC, 0x0000)    # C line active power offset
        self.comm_atm90(__write__, QoffsetC, 0x0000)    # C line reactive power offset
        self.comm_atm90(__write__, CSOne, 0x0000)       # Checksum 1

        #Set metering calibration values (HARMONIC)
        self.comm_atm90(__write__, HarmStart, 0x5678)   # Metering calibration startup 
        self.comm_atm90(__write__, POffsetAF, 0x0000)   # A Fund. active power offset
        self.comm_atm90(__write__, POffsetBF, 0x0000)   # B Fund. active power offset
        self.comm_atm90(__write__, POffsetCF, 0x0000)   # C Fund. active power offset
        self.comm_atm90(__write__, PGainAF, 0x0000)     # A Fund. active power gain
        self.comm_atm90(__write__, PGainBF, 0x0000)     # B Fund. active power gain
        self.comm_atm90(__write__, PGainCF, 0x0000)     # C Fund. active power gain
        self.comm_atm90(__write__, CSTwo, 0x0000)       # Checksum 2 

        #Set measurement calibration values (ADJUST)
        self.comm_atm90(__write__, AdjStart, 0x5678)    # Measurement calibration
        self.comm_atm90(__write__, UgainA, 0x0002)      # A SVoltage rms gain
        self.comm_atm90(__write__, IgainA, 0xFD7F)      # A line current gain
        self.comm_atm90(__write__, UoffsetA, 0x0000)    # A Voltage offset
        self.comm_atm90(__write__, IoffsetA, 0x0000)    # A line current offset
        self.comm_atm90(__write__, UgainB, 0x0002)      # B Voltage rms gain
        self.comm_atm90(__write__, IgainB, 0xFD7F)      # B line current gain
        self.comm_atm90(__write__, UoffsetB, 0x0000)    # B Voltage offset
        self.comm_atm90(__write__, IoffsetB, 0x0000)    # B line current offset
        self.comm_atm90(__write__, UgainC, 0x0002)      # C Voltage rms gain
        self.comm_atm90(__write__, IgainC, 0xFD7F)      # C line current gain
        self.comm_atm90(__write__, UoffsetC, 0x0000)    # C Voltage offset
        self.comm_atm90(__write__, IoffsetC, 0x0000)    # C line current offset
        self.comm_atm90(__write__, IgainN, 0xFD7F)      # C line current gain
        self.comm_atm90(__write__, CSThree, 0x02F6)     # Checksum 3

        # Done with the configuration
        self.comm_atm90(__write__, ConfigStart, 0x5678)
        self.comm_atm90(__write__, CalStart, 0x5678)    # 0x6886 #0x5678 #8765);
        self.comm_atm90(__write__, HarmStart, 0x5678)   # 0x6886 #0x5678 #8765);    
        self.comm_atm90(__write__, AdjStart, 0x5678)    # 0x6886 #0x5678 #8765);  

        self.comm_atm90(__write__, SoftReset, 0x789A)   # Perform soft reset
    
    def get_rms_voltages(self):
        VA = self.comm_atm90(__read__,UrmsA,0xFFFF)
        VB = self.comm_atm90(__read__,UrmsB,0xFFFF)
        VC = self.comm_atm90(__read__,UrmsC,0xFFFF)

        return (VA,VB,VC)

    def get_meter_status(self):
        s1 = self.comm_atm90(__read__,EnStatus0,0xFFFF)
        s2 = self.comm_atm90(__read__,EnStatus1,0xFFFF)

        return (s1,s2)


if __name__=="__main__":
    spi = spidev.SpiDev()
    spi.open(0, 1)

    spi.mode = 0b11
    spi.max_speed_hz = 200000

    eic1 = ATM90E36_SPI(spi)
    for i in range(10):
        print("Meter Status:",eic1.get_meter_status())
        print("Voltages:",eic1.get_rms_voltages())