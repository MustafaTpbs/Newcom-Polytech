import pytest
import hardpy
import serial
import logging
from rh_com_piste.com_FPGA import Com_FPGA
from rh_com_piste.antennes import Way
from rh_com_piste.walsh import FunctionsWalsh
from rh_com_piste.cmd_RF import CMDS_RF_NS
import time
from pico_driver import PicoDevice

pytestmark = pytest.mark.module_name("P3 - RF - CT")
log = logging.getLogger(__name__)

@pytest.fixture(scope="module")
def fpga():
    """Prépare la connexion avec le Rack Pist une seule fois pour tout le test"""
    device = Com_FPGA("/dev/ttyUSB0", 460800)
    device.ACTIVE_COM() # Allume la communication
    return device # Donne l'accès au FPGA aux fonctions de test

@pytest.fixture(scope="module")
def picode():
    """
    Interface avec la Pico via USB.
    """
    # On crée l'accès physique à la Pico via le port USB de la VM
    device = PicoDevice("/dev/ttyACM0")

    class PicodeControl:
        def ok_nok_ct1(self):
            valeur_reelle = device.read_status_rf_ct1()
            return valeur_reelle
        
        def ok_nok_ct2(self):
            valeur_reelle = device.read_status_rf_ct2()
            return valeur_reelle
        
        def ok_nok_ct3(self):
            valeur_reelle = device.read_status_rf_ct3()
            return valeur_reelle

    yield PicodeControl()
    device.close()

# -------------------- TESTS RF --------------------------

@pytest.mark.case_name("RF [CT1] : 150.9 MHz ")
def test_rf_ct1(fpga, picode, record_property):

    for idx in range(10):
        fpga.send_CMD_RF(CMDS_RF_NS[7], Way.NS, idx)

    resultat = picode.ok_nok_ct1()

    assert resultat == True, "CT1 non fonctionnel"
    time.sleep(1)

# CT2 n'est pas testé 

@pytest.mark.case_name("RF [CT3] : 270.6 MHz ")
def test_rf_ct3(fpga, picode, record_property):

    for idx in range(10):
        fpga.send_CMD_RF(CMDS_RF_NS[4], Way.NS, idx)

    resultat = picode.ok_nok_ct3()

    assert resultat == True, "CT3 non fonctionnel"
    time.sleep(1)

#------------------------Fin Test RF----------------------------------------

