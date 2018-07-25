import modbus
import threading
import time

class Inverter( modbus.GatewayInstrument ):
    mutex = threading.Lock()

    def __init__(self, gatewayAddress, gatewayPort, slaveAddress,):
        modbus.GatewayInstrument.__init__(self, gatewayAddress, gatewayPort, slaveAddress)

    

    def flag(self,number, pos):
        return 1 if number&(1<<pos)!=0 else 0
        
        
    def getFreq(self):
        
        try:
            with self.mutex:
                reply=self.read_register(4,functioncode=3)/100.
        except:
            raise
        return reply
    

    def getRPM(self):
        
        try:
            with self.mutex:
                reply=self.read_register(0x14,functioncode=3)/100.
        except:
            raise
        return reply


    def getCurrent(self):
        
        try:
            with self.mutex:
                reply=self.read_register(0x8,functioncode=3)/10.
        except:
            raise
        return reply


    def getPower(self):
        
        try:
            with self.mutex:
                reply=self.read_register(0x0C,functioncode=3)/10.
        except:
            raise
        return reply

    def getFirmware(self):
        
        try:
            with self.mutex:
                reply=self.read_register(0x02,functioncode=3)/10.
        except:
            raise
        return reply



    def getState(self):

        P=self.getPower()
        I=self.getCurrent()
        n=self.getRPM()
        f=self.getActFreq()
        
        state={"Power":P, "Current":I, "RPM":n, "Frequency":f}
        return(state)

    def setFreq(self,value):
        
        with self.mutex:
            return self.write_register(4, int(float(value)*100), functioncode=6)


    def getStatus(self):
        
        try:
            with self.mutex:
                reply=self.read_register(0x0D,functioncode=3)
        except:
            raise
        return reply

    def getActFreq(self):
        
        try:
            with self.mutex:
                reply=self.read_register(9,functioncode=3)/100.
        except:
            raise
        return reply


    def runMotor(self):
        with self.mutex:
            return self.write_register(5, 2, functioncode=6)

    def stopMotor(self):
        with self.mutex:
            return self.write_register(5, 1, functioncode=6)

    def setPWM(self, PWM):
        with self.mutex:
            return self.write_register(5, PWM, functioncode=6)
    
    def setKasAwar(self, value):
        if value == 1:
            orMask=0x02
        else:
            orMask=0x00
        with self.mutex:
            reply=self.mask_write_register(2,or_mask=orMask, and_mask=0xFFFD)
        return  reply

    def setDKG(self, value):
        if value == 1:
            orMask=0x01
        else:
            orMask=0x00
        with self.mutex:
            reply=self.mask_write_register(2,or_mask=orMask, and_mask=0xFFFE)
        return reply
    
    def readOutputs(self):
        with self.mutex:
            reply=self.read_register(2,functioncode=3)
        return reply

    def readRegisters(self, slaveID, startingAddress, noOfPoints):
        with self.mutex:
            currentSlave=self.address
            self.address=slaveID
            reply= self.read_registers(startingAddress,noOfPoints)
            self.address=currentSlave
        return reply

    def presetRegister(self, slaveID, registerAddress, presetData):
        with self.mutex:
            currentSlave=self.address
            self.address=slaveID
            reply= self.write_register(registerAddress,presetData,functioncode=6)
            self.address=currentSlave
        return reply     
   
    def MaskPresetRegister(self, slaveID, registerAddress, andMask, orMask):
        with self.mutex:
            currentSlave=self.address
            self.address=slaveID
            reply= self.mask_write_register(registerAddress,or_mask=orMask,and_mask=andMask)
            self.address=currentSlave
        return reply

    def close(self):

        self.serial.close()
#modbus.minimalmodbus._checkResponseByteCount=modbus._checkResponseByteCount
modbus.minimalmodbus._predictResponseSize=modbus._predictResponseSize
if __name__ == '__main__':

    modbus.minimalmodbus._print_out( 'TESTING Inverter MODBUS MODULE')

    a = Inverter('192.168.20.119',4002, 1)
    a.debug = False
  
    

    
    try:
        modbus.minimalmodbus._print_out( 'Firmware:                  {0}'.format( a.getFirmware()) )
        modbus.minimalmodbus._print_out( 'Freq Preset:            {0}'.format( a.getFreq() ))
        modbus.minimalmodbus._print_out( 'Freq Preset 1.5:        {0}'.format( a.setFreq(2.5) ))
        modbus.minimalmodbus._print_out( 'Freq Preset:            {0}'.format( a.getFreq() ))
        modbus.minimalmodbus._print_out( 'Status:                 {0:b}'.format( a.getStatus() ))
        modbus.minimalmodbus._print_out( 'Freq :            {0}'.format( a.getActFreq() ))
        modbus.minimalmodbus._print_out( 'RunMotor:                 {0}'.format( a.runMotor() ))
        modbus.minimalmodbus._print_out( 'Status:                 {0:b}'.format( a.getStatus() ))
        modbus.minimalmodbus._print_out( 'Freq :            {0}'.format( a.getActFreq() ))
        
        modbus.minimalmodbus._print_out( 'state:                 {0}'.format( a.getState() ))      
        modbus.minimalmodbus._print_out( 'Freq :            {0}'.format( a.getActFreq() ))
        modbus.minimalmodbus._print_out( 'Status:                 {0:b}'.format( a.getStatus() ))
        modbus.minimalmodbus._print_out( 'StopMotor:                 {0}'.format( a.stopMotor() ))
        modbus.minimalmodbus._print_out( 'Status:                 {0:b}'.format( a.getStatus() ))
        modbus.minimalmodbus._print_out( 'state:                 {0}'.format( a.getState() ))   
        time.sleep(3)
        modbus.minimalmodbus._print_out( 'state:                 {0}'.format( a.getState() ))       
    
      #  modbus.minimalmodbus._print_out( 'Status:                    {0}'.format( a.readStatus() ))
      #  modbus.minimalmodbus._print_out( 'SetPWM0:                   {0}'.format( a.setPWM(0) ))       
        # modbus.minimalmodbus._print_out( 'Status:                    {0}'.format( a.readStatus() ))
        # modbus.minimalmodbus._print_out( 'Outputs:                    {}'.format(a.readOutputs()))
        # modbus.minimalmodbus._print_out( 'SetKASAwar1:                {}'.format( a.setKasAwar(1) ))  
        # modbus.minimalmodbus._print_out( 'Outputs:                    {}'.format(a.readOutputs()))      
        # modbus.minimalmodbus._print_out( 'Status:                    {0}'.format( a.readStatus() ))
        # modbus.minimalmodbus._print_out( 'SetKASAwar0:                {}'.format( a.setKasAwar(0) ))   
        # modbus.minimalmodbus._print_out( 'Outputs:                    {}'.format(a.readOutputs()))   
        # modbus.minimalmodbus._print_out( 'SetDKG1:                    {}'.format( a.setDKG(1) ))  
        # modbus.minimalmodbus._print_out( 'Outputs:                    {}'.format(a.readOutputs()))      
        # modbus.minimalmodbus._print_out( 'Status:                    {0}'.format( a.readStatus() ))
        # modbus.minimalmodbus._print_out( 'SetDKG0:                {}'.format( a.setDKG(0) ))   
        # modbus.minimalmodbus._print_out( 'Outputs:                    {}'.format(a.readOutputs()))   
        # modbus.minimalmodbus._print_out( 'Status:                     {0}'.format( a.readStatus() ))

    finally:
 
        a.close()

    modbus.minimalmodbus._print_out( 'DONE!' )

pass 