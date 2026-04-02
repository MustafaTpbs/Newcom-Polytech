import picod

class PicoDevice:
    def __init__(self, port='/dev/ttyACM0'):
        # Initialisation de la connexion picod
        self.p = picod.pico(device=port)

        PIN_SOURCE = 8
        self.p.gpio_open(PIN_SOURCE)
        self.p.gpio_set_output(PIN_SOURCE, 1)

        # Définition des pins d'entrée de la pico - TEST RF
        self.gp_ct1 = 0 # Pin 1 physique (CT1)
        self.gp_ct2 = 1 # Pin 2 physique (CT2)
        self.gp_ct3 = 2 # Pin 4 physique (CT3)
        self.gp_cc1 = 3 # Pin 5 physique (CC1)
        self.gp_cc2 = 4 # Pin 6 physique (CC2)
        self.gp_cc3 = 5 # Pin 7 physique (CC3)
        self.gp_cc4 = 6 # Pin 9 physique (CC4)
        self.gp_cc5 = 7 # Pin 10 physique (CC5)

        # Définition des pins de sortie de la pico - TEST MODULATION
        self.adc_out = 16

        if not self.p.connected:
            raise ConnectionError(f"Pico non détectée sur {port}")

        # Ouverture et configuration des GPIO
        self.p.gpio_open(self.gp_cc1)
        self.p.gpio_open(self.gp_cc2)
        self.p.gpio_open(self.gp_cc3)
        self.p.gpio_open(self.gp_cc4)
        self.p.gpio_open(self.gp_cc5)
        self.p.gpio_open(self.gp_ct1)
        self.p.gpio_open(self.gp_ct2)
        self.p.gpio_open(self.gp_ct3)

        self.p.gpio_open(self.adc_out)
        
        # Configuration en entrée des pins
        self.p.gpio_set_input(self.gp_cc1)
        self.p.gpio_set_input(self.gp_cc2)
        self.p.gpio_set_input(self.gp_cc3)
        self.p.gpio_set_input(self.gp_cc4)
        self.p.gpio_set_input(self.gp_cc5)
        self.p.gpio_set_input(self.gp_ct1)
        self.p.gpio_set_input(self.gp_ct2)
        self.p.gpio_set_input(self.gp_ct3)

        self.p.gpio_set_input(self.adc_out)
        
    def read_status_rf_cc1(self):
        res1, level_cc1 = self.p.gpio_read(self.gp_cc1)
            
        if res1 == 0 :
            return (level_cc1 == 1)
        
    def read_status_rf_cc2(self):
        res1, level_cc2 = self.p.gpio_read(self.gp_cc2)
            
        if res1 == 0 :
            return (level_cc2 == 1)
        
    def read_status_rf_cc3(self):
        res1, level_cc3 = self.p.gpio_read(self.gp_cc3)
            
        if res1 == 0 :
            return (level_cc3 == 1)
        
    def read_status_rf_cc4(self):
        res1, level_cc4 = self.p.gpio_read(self.gp_cc4)
            
        if res1 == 0 :
            return (level_cc4 == 1)
        
    def read_status_rf_cc5(self):
        res1, level_cc5 = self.p.gpio_read(self.gp_cc5)
            
        if res1 == 0 :
            return (level_cc5 == 1)
        
    def read_status_rf_ct1(self):
        res1, level_ct1 = self.p.gpio_read(self.gp_ct1)
            
        if res1 == 0 :
            return (level_ct1 == 1)
        
    def read_status_rf_ct2(self):
        res1, level_ct2 = self.p.gpio_read(self.gp_ct2)
            
        if res1 == 0 :
            return (level_ct2 == 1)
        
    def read_status_rf_ct3(self):
        res1, level_ct3 = self.p.gpio_read(self.gp_ct3)
            
        if res1 == 0 :
            return (level_ct3 == 1)

    def read_status_modulation(self): #à faire
        return True
    
    def read_retard(self): #impossible
        return True
    
    def read_voltage_5V(self):
        return True #à faire
    def read_voltage_minus5V(self):
        return True #à faire
    def read_voltage_12V(self):
        return True #à faire
    def read_voltage_minus12V(self):
        return True #à faire

    def close(self):
        self.p.close()