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

pytestmark = pytest.mark.module_name("P5 - RF - CC")
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
        def ok_nok_cc1(self):
            # Envoie la commande par USB et récupère la réponse de la Pico
            valeur_reelle = device.read_status_rf_cc1()
            return valeur_reelle
        
        def ok_nok_cc2(self):
            valeur_reelle = device.read_status_rf_cc2()
            return valeur_reelle
        
        def ok_nok_cc3(self):
            valeur_reelle = device.read_status_rf_cc3()
            return valeur_reelle
        
        def ok_nok_cc4(self):
            valeur_reelle = device.read_status_rf_cc4()
            return valeur_reelle
        
        def ok_nok_cc5(self):
            valeur_reelle = device.read_status_rf_cc5()
            return valeur_reelle

    yield PicodeControl()
    device.close()

# -------------------- TESTS RF --------------------------

@pytest.mark.case_name("RF [CC1] : 150.9 MHz ")
def test_rf_cc1(fpga, picode, record_property):

    for idx in range(10):
        fpga.send_CMD_RF(CMDS_RF_NS[7], Way.NS, idx)
    
    # Demande au Picode si la tension est présente
    resultat = picode.ok_nok_cc1()
    
    # Si False, le voyant passe au ROUGE dans HardPy
    assert resultat == True, "CC1 non fonctionnel"
    time.sleep(1)

@pytest.mark.case_name("RF [CC2] : 228 MHz ")
def test_rf_cc2(fpga, picode, record_property):

    for idx in range(10):
        fpga.send_CMD_RF(CMDS_RF_NS[0], Way.NS, idx)

    resultat = picode.ok_nok_cc2()

    assert resultat == True, "CC2 non fonctionnel"
    time.sleep(1)

@pytest.mark.case_name("RF [CC3] : 298.7 MHz ")
def test_rf_cc3(fpga, picode, record_property):

    for idx in range(10):
        fpga.send_CMD_RF(CMDS_RF_NS[1], Way.NS, idx)

    resultat = picode.ok_nok_cc3()

    assert resultat == True, "CC3 non fonctionnel"
    time.sleep(1)

@pytest.mark.case_name("RF [CC4] : 382.2 MHz ")
def test_rf_cc4(fpga, picode, record_property):

    for idx in range(10):
        fpga.send_CMD_RF(CMDS_RF_NS[2], Way.NS, idx)

    resultat = picode.ok_nok_cc4()

    assert resultat == True, "CC4 non fonctionnel"
    time.sleep(1)

@pytest.mark.case_name("RF [CC5] : 444 MHz ")
def test_rf_cc5(fpga, picode, record_property):

    for idx in range(10):
        fpga.send_CMD_RF(CMDS_RF_NS[5], Way.NS, idx)

    resultat = picode.ok_nok_cc5()

    assert resultat == True, "CC5 non fonctionnel"
    time.sleep(1)

#------------------------Fin Test RF----------------------------------------
    