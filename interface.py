##################################################################################################
##################################################################################################
##################################################################################################
#Cette interface est prévue pour fonctionner en étant situer dans votre répertoire de test Hardpy#
##################################################################################################
##################################################################################################
##################################################################################################
#Bien se placer dans le répertoire de test Harpy pour que les chemins soient corrects

import sys
import os
import json
import glob
import subprocess
import shutil
from pathlib import Path
from datetime import datetime
from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QLineEdit, QLabel, QStackedWidget, QMessageBox)
from PySide6.QtCore import Qt, QUrl, QTimer
from PySide6.QtWebEngineWidgets import QWebEngineView
from inventree.api import InvenTreeAPI

class InterfaceHardPy(QWidget):
    def __init__(self):
        super().__init__()
        
        # --- Configuration InvenTree ---
        self.SERVER_ADDRESS = 'http://192.168.2.1'#Mettre l'adresse de votre serveur inventree
        self.MY_USERNAME = 'cedri' #Mettez votre identifiant
        self.MY_PASSWORD = 'Sedan2003!' #Mettez votre mot de passe
        self.cwd = Path.cwd() #Bien se placer dans le répertoire de test Harpy pour que les chemins soient corrects
        
        # Utilisation de chemins POSIX pour Linux (/reports)
        self.reports_wd = self.cwd / "reports"
        
        # Création du dossier reports s'il n'existe pas
        os.makedirs(self.reports_wd, exist_ok=True)
        
        self.product_id = ""
        self.api = None
        
        # 1. Vérification de la connexion avant de charger l'interface
        if not self.init_inventree():
            sys.exit(1)

        self.initUI()

    def init_inventree(self):
        """Initialise la connexion à l'API InvenTree au démarrage."""
        try:
            self.api = InvenTreeAPI(self.SERVER_ADDRESS, username=self.MY_USERNAME, password=self.MY_PASSWORD)
            print("Connecté à InvenTree")
            return True
        except Exception as e:
            QMessageBox.critical(
                None, 
                "Erreur Fatale - InvenTree Inaccessible",
                f"Impossible de se connecter au serveur : {self.SERVER_ADDRESS}\n\n"
                f"Erreur : {str(e)}\n\n"
                "L'interface va se fermer. Vérifiez que les containers Docker sont lancés."
            )
            return False

    def initUI(self):
        self.setWindowTitle("HardPy Operator Panel (Linux)")
        self.resize(1200, 900)
        self.setStyleSheet("background-color: #E0E0E0;") 

        self.stacked_widget = QStackedWidget(self)
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(self.stacked_widget)

        self.creer_page_accueil()
        self.creer_page_test()
        self.creer_page_fin()

    def creer_page_accueil(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        
        self.input_id = QLineEdit()
        self.input_id.setPlaceholderText("Entrez l'ID du Stock Item InvenTree...")
        self.input_id.setStyleSheet("color: black; padding: 15px; font-size: 16px; border-radius: 8px; border: 1px solid #CCC;")
        self.input_id.setFixedWidth(400)

        btn_valider = QPushButton("DÉMARRER LE TEST")
        btn_valider.setStyleSheet("""
            QPushButton { background-color: #0078D7; color: white; padding: 15px; font-weight: bold; border-radius: 8px; }
            QPushButton:hover { background-color: #005A9E; }
        """)
        btn_valider.setFixedWidth(250)
        btn_valider.clicked.connect(self.lancer_test)

        layout.addStretch()
        layout.addWidget(self.input_id, alignment=Qt.AlignCenter)
        layout.addSpacing(20)
        layout.addWidget(btn_valider, alignment=Qt.AlignCenter)
        layout.addStretch()
        self.stacked_widget.addWidget(page)

    def creer_page_test(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(0, 0, 0, 0)

        header = QHBoxLayout()
        header.setContentsMargins(10, 5, 10, 5)
        
        btn_refresh = QPushButton("🔄 Actualiser")
        btn_refresh.setFixedWidth(120)
        btn_refresh.clicked.connect(lambda: self.navigateur.reload())
        
        self.label_id_test = QLabel("ID Stock: ---")
        self.label_id_test.setStyleSheet("font-weight: bold; font-size: 14px; color: black;")

        header.addWidget(btn_refresh)
        header.addStretch()
        header.addWidget(self.label_id_test)
        layout.addLayout(header)

        self.navigateur = QWebEngineView()
        layout.addWidget(self.navigateur, stretch=1) 

        btn_fin = QPushButton("VALIDER FIN DE TEST ET ENVOYER RÉSULTATS")
        btn_fin.setStyleSheet("background-color: #D83B01; color: white; padding: 20px; font-weight: bold; font-size: 16px;")
        btn_fin.clicked.connect(self.terminer_test)
        layout.addWidget(btn_fin)

        self.stacked_widget.addWidget(page)

    def creer_page_fin(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        self.label_id_fin = QLabel("Test Terminé")
        self.label_id_fin.setStyleSheet("font-size: 24px; font-weight: bold; color: black;")
        self.label_id_fin.setAlignment(Qt.AlignCenter)
        
        btn_restart = QPushButton("RETOUR À L'ACCUEIL")
        btn_restart.setFixedWidth(200)
        btn_restart.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        
        layout.addStretch()
        layout.addWidget(self.label_id_fin)
        layout.addSpacing(20)
        layout.addWidget(btn_restart, alignment=Qt.AlignCenter)
        layout.addStretch()
        self.stacked_widget.addWidget(page)

    def lancer_test(self):
        if not self.input_id.text().strip():
            QMessageBox.critical(self, "Erreur", "L'identifiant du Stock Item est requis.")
            return
        
        self.product_id = self.input_id.text().strip()
        self.label_id_test.setText(f"Stock Item ID : {self.product_id}")

        # Lancement de HardPy avec détection de terminal Linux
        try:
            commande = f'gnome-terminal -- bash -c "hardpy run Harpy; exec bash"'
            subprocess.Popen(commande, cwd=self.cwd, shell=True)
        except Exception as e:
            print(f"Erreur lancement terminal : {e}")

        self.stacked_widget.setCurrentIndex(1)
        # On attend que le serveur HardPy démarre
        QTimer.singleShot(3000, lambda: self.navigateur.setUrl(QUrl("http://localhost:8000/")))

    def terminer_test(self):
        """Génère les JSON spécifiques, les envoie à InvenTree, puis nettoie."""
        
        liste_fichiers = glob.glob(os.path.join(str(self.reports_wd), "*.json"))
        fichiers_bruts = [f for f in liste_fichiers if not os.path.basename(f).startswith(self.product_id + "_")]
        
        if not fichiers_bruts:
            QMessageBox.warning(self, "Erreur", "Aucun fichier JSON de résultat brut trouvé.")
            return
        
        chemin_json_brut = max(fichiers_bruts, key=os.path.getctime)
        horodatage = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        try:
            with open(chemin_json_brut, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            # 1. TRAITEMENT GLOBAL
            statut_global_texte = data.get("status", "failed")
            is_global_success = (statut_global_texte == "passed")
            
            nom_fichier_global = f"{self.product_id}_global_{horodatage}.json"
            chemin_fichier_global = os.path.join(str(self.reports_wd), nom_fichier_global)
            
            with open(chemin_fichier_global, 'w', encoding='utf-8') as f_out:
                json.dump(data, f_out, indent=4)

            with open(chemin_fichier_global, 'rb') as f_attach:
                self.api.post(
                    'stock/test/',
                    data={
                        'stock_item': self.product_id,
                        'test': 'Validity',
                        'result': is_global_success,
                        'notes': f"Résultat global : {statut_global_texte.upper()}"
                    },
                    files={'attachment': f_attach}
                )

            # 2. TRAITEMENT MODULES
            modules_data = data.get("modules", {})
            for module_key, module_info in modules_data.items():
                nom_module = module_info.get("name", module_key)
                statut_module = module_info.get("status", "failed")
                is_module_success = (statut_module == "passed")
                
                nom_fichier_module = f"{self.product_id}_{module_key}_{horodatage}.json"
                chemin_fichier_module = os.path.join(str(self.reports_wd), nom_fichier_module)
                
                with open(chemin_fichier_module, 'w', encoding='utf-8') as f_mod_out:
                    json.dump(module_info, f_mod_out, indent=4)
                
                with open(chemin_fichier_module, 'rb') as f_mod_attach:
                    self.api.post(
                        'stock/test/',
                        data={
                            'stock_item': self.product_id,
                            'test': nom_module, 
                            'result': is_module_success,
                            'notes': f"Sous-module : {module_key} - Statut : {statut_module.upper()}"
                        },
                        files={'attachment': f_mod_attach}
                    )
                
                try:
                    os.remove(chemin_fichier_module)
                except Exception as e:
                    print(f"Avertissement: Impossible de supprimer {chemin_fichier_module} : {e}")

            try:
                os.remove(chemin_json_brut)
            except Exception as e:
                print(f"Avertissement: Impossible de supprimer le fichier brut original : {e}")

            self.label_id_fin.setText(f"Résultats envoyés avec succès pour l'ID {self.product_id}")
            self.stacked_widget.setCurrentIndex(2)
            
        except Exception as e:
            QMessageBox.critical(self, "Erreur Transmission", f"Échec de l'envoi à InvenTree : {str(e)}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = InterfaceHardPy()
    window.show()
    sys.exit(app.exec())