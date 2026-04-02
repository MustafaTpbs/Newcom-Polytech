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

pytestmark = pytest.mark.module_name("MODULATION - Bouton adressable - retard") #Les noms doivent être exactement les memes que sur inventree
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
        
        def ok_nok_modulation(self):
            # On utilise la même manière de faire pour les autres tests
            valeur_reelle = device.read_status_modulation()
            return valeur_reelle
        
        def ok_nok_retard(self): #à faire
            valeur_reelle = device.read_retard()
            return valeur_reelle

    yield PicodeControl()
    device.close()

#------------------------Début test Modulation------------------------------

@pytest.mark.case_name("MODULATION [MODH/MODV]")
def test_modulation(fpga, picode, record_property):
    
    for i in range(10):
        fpga.send_FONCTION_WALSH(FunctionsWalsh.MODE_6, Way.NS, idx=i)
    
    resultat = picode.ok_nok_modulation()
    
    assert resultat == True, "La modulation n'est pas passée à l'état attendu."
    
    time.sleep(2)
    
#------------------------Fin test Modulation------------------------------


#----------------Début test bouton adressable & retard -------------------

@pytest.mark.case_name("Bouton adressable/retard : Régler le switch sur 00000000")
def test_bouton_adressable(fpga, picode, record_property):
    """
    Vérifie que le retard décale bien le signal vers la droite par rapport au 100Hz.
    L'antenne doit avoir ses switchs sur 0.
    """
    # On met un signal carré (Walsh) pour mesurer un décalage
    for i in range(10):
        fpga.send_FONCTION_WALSH(FunctionsWalsh.MODE_0, Way.NS, idx=i)
    
    # On envoie le retard
    fpga.send_RETARD_MONO(0, 128, Way.NS)
    fpga.valid_RETARD(Way.NS) 
    
    # Demande au Picode si le retard est appliqué
    resultat = picode.ok_nok_retard()
    
    # Verdict : Vérifie si le Picode a bien vu le décalage
    assert resultat == True, "Le retard n'a pas été détecté. Vérifiez l'ID des switchs."

    time.sleep(1)

    #----------------Fin test bouton adressable & retard -------------------


    