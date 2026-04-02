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

pytestmark = pytest.mark.module_name("Alimentation")
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
        def ok_nok_voltage_5V(self):
            # Envoie la commande par USB et récupère la réponse de la Pico
            valeur_reelle = device.read_voltage_5V()
            return valeur_reelle
        def ok_nok_voltage_minus5V(self):
            # Envoie la commande par USB et récupère la réponse de la Pico
            valeur_reelle = device.read_voltage_minus5V()
            return valeur_reelle
        def ok_nok_voltage_12V(self):
            # Envoie la commande par USB et récupère la réponse de la Pico
            valeur_reelle = device.read_voltage_12V()
            return valeur_reelle
        def ok_nok_voltage_minus12V(self):
            # Envoie la commande par USB et récupère la réponse de la Pico
            valeur_reelle = device.read_voltage_minus12V()
            return valeur_reelle
        
    yield PicodeControl()
    device.close()
        
@pytest.mark.case_name("5V")
def test_voltage5V(fpga, picode, record_property):
    
    #à faire
    resultat = picode.ok_nok_voltage_5V()
    
    assert resultat == True, "La tension de 5V n'a pas été mesuré"
    
    time.sleep(2)

@pytest.mark.case_name("-5V")
def test_voltage_minus5V(fpga, picode, record_property):
    
    #à faire
    resultat = picode.ok_nok_voltage_minus5V()
    
    assert resultat == True, "La tension de -5V n'a pas été mesuré"
    
    time.sleep(2)

@pytest.mark.case_name("12V")
def test_voltage12V(fpga, picode, record_property):
    
    #à faire
    resultat = picode.ok_nok_voltage_12V()
    
    assert resultat == True, "La tension de 12V n'a pas été mesuré"
    
    time.sleep(2)

@pytest.mark.case_name("-12V")
def test_voltage_minus12V(fpga, picode, record_property):
    
    #à faire
    resultat = picode.ok_nok_voltage_minus12V()
    
    assert resultat == True, "La tension de -12V n'a pas été mesuré"
    
    time.sleep(2)