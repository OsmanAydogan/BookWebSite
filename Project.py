import sys
import time
import random
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QRadioButton, QMessageBox, QLineEdit
from PyQt5.QtCore import Qt 

import Words


class HizliYazmaTesti(QWidget):
    def __init__(self):
        super().__init__() 

        self.setWindowTitle("Hızlı Yazma Testi")                
        self.setStyleSheet("font-size: 20px; font-weight: bold;") 

        self.setGeometry(700, 80, 600, 900) 

        self.zorluk = 0  
        self.guncel_kelime = ""
        self.dogru_sayisi = 0
        self.hatali_sayisi = 0
        self.kelime_sayisi = 0
        self.baslangic_zamani = 0

        self.init_ui()  

    def init_ui(self):
        dikeyBox = QVBoxLayout() 

        zorluk_label = QLabel("Zorluk Seviyesi") 
        zorluk_label.setAlignment(Qt.AlignCenter)
        zorluk_label.setStyleSheet("color: red;")
        dikeyBox.addWidget(zorluk_label)

        kolay_radio = QRadioButton("Kolay (3 Harfli Kelimeler)")
        kolay_radio.setChecked(False)
        kolay_radio.toggled.connect(lambda: self.set_zorluk(3))
        dikeyBox.addWidget(kolay_radio)

        orta_radio = QRadioButton("Orta (5 Harfli Kelimeler)")
        orta_radio.toggled.connect(lambda: self.set_zorluk(5))
        dikeyBox.addWidget(orta_radio)

        zor_radio = QRadioButton("Zor (7 Harfli Kelimeler)")
        zor_radio.toggled.connect(lambda: self.set_zorluk(7))
        dikeyBox.addWidget(zor_radio)

        testi_baslat_button = QPushButton("Testi Başlat") 
        testi_baslat_button.clicked.connect(self.testi_baslat)
        dikeyBox.addWidget(testi_baslat_button) 

        self.kelime_label = QLabel() 
        dikeyBox.addWidget(self.kelime_label)

        self.giris_alani = QLineEdit()  
        self.giris_alani.returnPressed.connect(self.kelimeyi_gonder)  
        dikeyBox.addWidget(self.giris_alani)

        gonder_button = QPushButton("Gönder")
        gonder_button.clicked.connect(self.kelimeyi_gonder)
        dikeyBox.addWidget(gonder_button)

        yatay_duzenle = QHBoxLayout()

        dogru_label = QLabel("Doğru Kelime Sayısı:")
        yatay_duzenle.addWidget(dogru_label)

        self.dogru_sayisi_label = QLabel("0")
        yatay_duzenle.addWidget(self.dogru_sayisi_label)

        hatali_label = QLabel("Hatalı Kelime Sayısı:")
        yatay_duzenle.addWidget(hatali_label)

        self.hatali_sayisi_label = QLabel("0")
        yatay_duzenle.addWidget(self.hatali_sayisi_label) 

        dikeyBox.addLayout(yatay_duzenle) 

        self.setLayout(dikeyBox) 

    def set_zorluk(self, zorluk):
        self.zorluk = zorluk

    def testi_baslat(self):
        if self.zorluk == 0:
            QMessageBox.warning(self, "Hata", "Zorluk seviyesi seçiniz!")
            return

        self.dogru_sayisi = 0
        self.hatali_sayisi = 0
        self.kelime_sayisi = 0
        self.baslangic_zamani = time.time()

      


        self.kelimeyi_guncelle()

    def kelimeyi_guncelle(self):
        if self.kelime_sayisi >= 5:
            gecen_sure = time.time() - self.baslangic_zamani
            self.sonucu_goster(gecen_sure)
            return

        kelime_listesi = self.kelime_listesini_al()

        if not kelime_listesi:
            QMessageBox.warning(self, "Hata", "Geçerli bir zorluk seviyesi seçiniz!")
            return

        self.guncel_kelime = random.choice(kelime_listesi)
        self.kelime_label.setText(self.guncel_kelime)
        self.giris_alani.setText("")  
        self.giris_alani.setFocus()  

    def kelime_listesini_al(self):
        if self.zorluk == 3:
            return Words.kolay
        elif self.zorluk == 5:
            return Words.orta
        elif self.zorluk == 7:
            return Words.zor
        else:
            return 

    def kelimeyi_gonder(self):
        girilen_kelime = self.giris_alani.text()

        if girilen_kelime == self.guncel_kelime:
            self.dogru_sayisi += 1
        else:
            self.hatali_sayisi += 1

        self.dogru_sayisi_label.setText(str(self.dogru_sayisi)) 
        self.hatali_sayisi_label.setText(str(self.hatali_sayisi))

        self.kelime_sayisi += 1
        self.kelimeyi_guncelle()

    def sonucu_goster(self, gecen_sure):
        test_sonucu = "\nTest tamamlandı ✓\nToplam süre: {:.2f} saniye\nDoğru yazılan kelime sayısı: {}\nHatalı yazılan kelime sayısı: {}".format(
            gecen_sure, self.dogru_sayisi, self.hatali_sayisi)
        QMessageBox.information(self, "Test Sonucu", test_sonucu)
        self.giris_alani.setText("")
        self.dogru_sayisi_label.setText("0")
        self.hatali_sayisi_label.setText("0")

 
if __name__ == "__main__":   
    app = QApplication(sys.argv)
    test = HizliYazmaTesti()
    test.show()
    sys.exit(app.exec())
