from  rh_com_piste.cmd_RF import Cmd_RF
from  rh_com_piste.UART_MM import Uart_MM
from rh_com_piste.bits_manipulation import *
from rh_com_piste.walsh import FunctionsWalsh
from rh_com_piste.antennes import Way


class Com_FPGA():
  def __init__(self,port,baudrate,simumode=False) -> None:
   
    self.simumode = simumode
    if not simumode:
      self.com = Uart_MM(port = port,baudrate=baudrate)
    else:
      self.simumode = simumode
      self.file = open(port,'w+')
      
  def WRITE_TO_FILE(self,adr,data):
    self.file.write(f'{adr} {data}\n')
    self.file.flush()
  
  def SEP_CMD_SIMU(self,):
    #assert self.simumode != False, "This function can only be used in simu"
    if self.simumode:
      self.WRITE_TO_FILE(0xFF,0xFF)
  
  def ACTIVE_COM(self):
    if not self.simumode:
      self.com.write((15 << 4) + 0,0)

  def DISABLE_COM(self):
    if not self.simumode:
      self.com.write((15 << 4) + 0,1)
    
  def reset_bus(self):
    for freq in range(10):
      self.com.write((freq << 4) + 0,0)
      self.com.write((freq << 4) + 1,0)
      self.com.write((freq << 4) + 2,0)

  # CMD RF
  def send_CMD_RF(self, cmd : Cmd_RF ,way : Way, idx = 0):
    # idx corespond au mapping dans le FPGA
    # Il y'a 10 séquences de 5ms qui tourne en boucle
    # idx se définie sur le 4 bits de poids fort 
    adr = (idx << 4) + 0 + way.value
    #print(cmd.CMD_GAIN_m,cmd.CMD_GAIN,cmd.CMD_RESEAU_m,cmd.CMD_RESEAU)
    data = (cmd.CMD_GAIN_m << 12) + ( cmd.CMD_GAIN << 8) + (cmd.CMD_RESEAU_m << 4) + cmd.CMD_RESEAU
    
    if not self.simumode:
      self.com.write(adr,data)
    if self.simumode: 
       # simu file
      self.WRITE_TO_FILE(129+way.value,data)
  
  def send_RETARD_MONO(self,adr_ant,retard, way : Way, idx = 0):
    assert adr_ant < 50 , "adr ant should be < to 50"
    assert retard <= 1024 , "Retard should be <= to 1024"
    print("ant",adr_ant)
    data = (retard << 6) + adr_ant
    
    print("retard + ant",hex(data),decToBin(data,16))

    *_, data_m = to_mirror_inverted(decToBin(data,16))
    # Make an error if 666
    if retard == 666:
      data_m = data

    adr = (idx << 4) + 1 + way.value
    if not self.simumode:
      self.com.write(adr,data)
      adr = (idx << 4) + 2 + way.value
      self.com.write(adr,data_m)
    else:
      self.WRITE_TO_FILE(130+way.value,data)
      self.WRITE_TO_FILE(131+way.value,data_m)
     
    #self.valid_RETARD(way)
      
#  def send_RETARD(self,adr_ant,retard, way : Way):
#    print(adr_ant)
#    assert adr_ant < 50 , "adr ant should be < to 50"
#    assert retard <= 1024 , "Retard should be <= to 1024"
#
#    data = (retard << 6) + adr_ant
#    print(hex(data))
#
#    *_, data_m = to_mirror_inverted(decToBin(data,16))
#    
#    # Make an error if 666
#    if retard == 666:
#      data_m = data
#      
#    for f in range(9):
#      adr = (f << 4) + 1 + way.value
#      if not self.simumode:
#        self.com.write(adr,data)
#        
#        adr = (f << 4) + 2 + way.value
#        self.com.write(adr,data_m)
#      else:
#          if f == 0:
#            self.WRITE_TO_FILE(130+way.value,data)
#            self.WRITE_TO_FILE(131+way.value,data_m)
#     
#    self.valid_RETARD(way)

  def valid_RETARD(self, way : Way, idx = 0):

    data = 0x3f
    *_, data_m = to_mirror_inverted(decToBin(data,16))
    
    if not self.simumode:
      adr = (idx << 4) + 1 + way.value
      self.com.write(adr,data)
      adr = (idx << 4) + 2 + way.value
      self.com.write(adr,data_m)
    else:
      self.WRITE_TO_FILE(130+way.value,data)
      self.WRITE_TO_FILE(131+way.value,data_m)

#  def retard_INERTE(self, way : Way):
#
#    data = 0x28
#    *_, data_m = to_mirror_inverted(decToBin(data,16))
#    
#    for f in range(10):
#      if not self.simumode:
#        adr = (f << 4) + 1 + way.value
#        self.com.write(adr,data)
#        adr = (f << 4) + 2 + way.value
#        self.com.write(adr,data_m)
#      else:
#        if f == 0:
#          self.WRITE_TO_FILE(130+way.value,data)
#          self.WRITE_TO_FILE(131+way.value,data_m)

  def send_FONCTION_WALSH(self, cmdwalsh : FunctionsWalsh, way : Way, idx = 0):
    data =  cmdwalsh.value
    *_, data_m = to_mirror_inverted(decToBin(data,16))

    if not self.simumode:
      adr = (idx << 4) + 1 + way.value
      self.com.write(adr,data)
      adr = (idx << 4) + 2 + way.value
      self.com.write(adr,data_m)
    else:
        self.WRITE_TO_FILE(130+way.value,data)
        self.WRITE_TO_FILE(131+way.value,data_m)



