import rh_com_piste.bits_manipulation as bits
from rh_com_piste.frequence import FREQUENCE
class Cmd_RF():
  def __init__(self,CMD_RESEAU,CMD_GAIN,error=False) -> None:

    self.CMD_RESEAU = CMD_RESEAU
    self.CMD_GAIN = CMD_GAIN
    # miroir
    _, _, self.CMD_RESEAU_m = bits.to_mirror_inverted(bits.decToBin(CMD_RESEAU, 4)) 
    _, _, self.CMD_GAIN_m = bits.to_mirror_inverted(bits.decToBin(CMD_GAIN, 4)) 
    if error:
      self.CMD_RESEAU_m = CMD_GAIN
      self.CMD_GAIN_m = CMD_GAIN   


def get_CMD_EW(freq):
  CMD = 0x0000
  if freq < 350 :
    CMD += 0b00010001 # Set b0/b8
  if freq < 260 :
    CMD += 0b00100010 # Set b1/b9
  if freq < 385 :
    CMD += 0b01000100 # Set b2/b10
  if freq < 250 :
    CMD += 0b10001000 # Set b3/b11
  
  print('f', f , hex(CMD & 0x0f) , hex(CMD & 0XF0 >> 4 ) )
  return CMD & 0x0f , CMD & 0XF0 >> 4 

def get_CMD_NS(freq):
  if freq > 400:
    CMD = 0xFF
  elif freq > 340:
    CMD = 0xEE
  elif freq > 280:
    CMD = 0xDD
  elif freq > 250:
    CMD = 0xCC
  elif freq > 210:
    CMD = 0xBB
  if freq < 210: 
    CMD = 0xAA
  return CMD & 0x0F , CMD & 0XF0 >> 4 

CMDS_RF_EW = [None] *10
CMDS_RF_NS = [None] *10

for idx,f in enumerate(FREQUENCE):
  error = False
  if f  == 666 :
    error = True
  CMDS_RF_EW[idx] = Cmd_RF(*get_CMD_EW(f),error)
  CMDS_RF_NS[idx] = Cmd_RF(*get_CMD_NS(f),error)
  
"""
CMDS_RF_EW[0] = Cmd_RF(0xF, 0xF)
CMDS_RF_EW[1] = Cmd_RF(0x5, 0x5)
CMDS_RF_EW[2] = Cmd_RF(0x4, 0x4)
CMDS_RF_EW[3] = Cmd_RF(0x5, 0x5)
CMDS_RF_EW[4] = Cmd_RF(0x5, 0x5)
CMDS_RF_EW[5] = Cmd_RF(0x0, 0x0)
CMDS_RF_EW[6] = Cmd_RF(0x0, 0x0)
CMDS_RF_EW[7] = Cmd_RF(0xF, 0xF)
CMDS_RF_EW[8] = Cmd_RF(0xF, 0xF)
CMDS_RF_EW[9] = Cmd_RF(0x0, 0x0)

CMDS_RF_NS = [None] *10

CMDS_RF_NS[0] = Cmd_RF(0xB, 0xB)
CMDS_RF_NS[1] = Cmd_RF(0xD, 0xD)
CMDS_RF_NS[2] = Cmd_RF(0xE, 0xE)
CMDS_RF_NS[3] = Cmd_RF(0xD, 0xD)
CMDS_RF_NS[4] = Cmd_RF(0xC, 0xC)
CMDS_RF_NS[5] = Cmd_RF(0xF, 0xF)
CMDS_RF_NS[6] = Cmd_RF(0xF, 0xF)
CMDS_RF_NS[7] = Cmd_RF(0xA, 0xA)
CMDS_RF_NS[8] = Cmd_RF(0xA, 0xA)
CMDS_RF_NS[9] = Cmd_RF(0xF, 0xF)
"""