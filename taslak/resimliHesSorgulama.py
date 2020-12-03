
import threading
from PyQt5.QtGui import QColor, QMovie, QPixmap
from PyQt5.QtWidgets import QFileDialog, QLabel, QMessageBox, QMainWindow, QApplication, QDialog, QWidget
from PyQt5 import uic
from PyQt5.QtCore import Qt

import sys, time, os

from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from threading import Thread


class MWindow(QMainWindow):
    
    def __init__(self):
        super(MWindow, self).__init__()
        
        #*Firefox webdriver çalışması için aktif dizin path'de yoksa ekleniyor.
        dizin = os.getcwd()
        if dizin not in sys.path:
            sys.path.append(dizin)
        
       
       
        uic.loadUi("hesGui.ui", self)
        
        self.setFixedSize(550,350)
        self.hata.hide()
        self.radioButtonClicked()
        self.veritabanindan.clicked.connect(self.radioButtonClicked)
        self.eDevletten.clicked.connect(self.radioButtonClicked)
        self.temizle.clicked.connect(self.formuTemizle)
        self.sorgula.clicked.connect(self.hesSorgula)
        self.actionEkle.triggered.connect(lambda : self.ekleGuncelle("ekle"))
        self.actionGuncelle.triggered.connect(lambda : self.ekleGuncelle("guncelle"))
        self.actionSil.triggered.connect(self.sil)
        self.show()

        


    def hataMesaji(self, mesaj):
        self.hata.setText(mesaj)
        self.hata.show()
        self.formuTemizle()
        t = threading.Timer(5, self.hata.hide)
        t.start()
    
    
    def yukleniyorAnimasyonuBaslat(self):
        self.loadingWindow = QWidget(self)
        self.loadingWindow.resize(200,200)
        self.loadingWindow.move(int(self.width()/2-self.loadingWindow.width()/2) , int(self.height()/2-self.loadingWindow.height()/2))
        self.loadingWindow.setWindowFlag(Qt.FramelessWindowHint)
        label = QLabel(self.loadingWindow)
        self.movie = QMovie("loading.gif")
        label.setMovie(self.movie)
        self.movie.start()
        self.loadingWindow.show()
        self.setDisabled(True)
    
    
    def yukleniyorAnimasyonuKapat(self):
        self.setEnabled(True)
        self.loadingWindow.close()
        
        
    def hesSorgula(self):
        
        if self.hesKodu.text() == "":
            self.hataGoster("HES kodunu girmelisiniz.")
            return
        
        if self.eDevletten.isChecked() == True:
            
            if self.kullaniciAdi.text() != "" and self.sifre.text() != "":
                
                self.mThread = Thread(target=self.eDevlettenSorgula, args=(self.kullaniciAdi.text(),
                                                        self.sifre.text(),
                                                        self.hesKodu.text()))

                self.mThread.start()
                
                #TODO Resim sorgusu veritabanından yapılacak
                
                #self.resim.setPixmap(QPixmap("resim10.jpg"))
                
                
                self.yukleniyorAnimasyonuBaslat()
                

                    
                
            
            else:
                #*Kullanıcı adı veya şifresi boş
                self.hataGoster("e-Devlet kullanıcı adı ve şifresini girmelisiniz.")
                return
        else:
            #TODO Veritabanından sorgu yapılacak.
            pass
    
        
    
    def formuTemizle(self):
        self.hesKodu.setText("")
        #self.kullaniciAdi.setText("")
        #self.sifre.setText("")
        self.tcKimlikNo.setText("")
        self.durum.setText("")
        self.labelHesKodu.setText("")
        
        # TODO Placeholder profil resmi eklenecek.
        #self.resim.setPixmap(QPixmap("resim10.jpg"))
        
    
    def radioButtonClicked(self):
        if self.veritabanindan.isChecked():
            self.sifre.setText("")
            self.kullaniciAdi.setText("")
            self.kullaniciAdi.hide()
            self.labelKullaniciAdi.hide()
            self.sifre.hide()
            self.labelSifre.hide()
        else:
            self.kullaniciAdi.show()
            self.labelKullaniciAdi.show()
            self.sifre.show()
            self.labelSifre.show()
    

    
    def ekleGuncelle(self, eylem):
        self.eklenenResim = ""
        
        self.widget = QDialog(self)
        uic.loadUi("ekleGuncelle.ui", self.widget)
        
        self.widget.setFixedSize(450, 280)
        
        if eylem == "ekle":
            self.widget.setWindowTitle("Ekle")
            self.widget.widgetHesKodu.setText(self.labelHesKodu.text())
            self.widget.widgetTcKimlikNo.setText(self.tcKimlikNo.text())
            self.widget.widgetDurum.setText(self.durum.text())
        else:
            self.widget.setWindowTitle("Güncelle")
            if self.tcKimlikNo.text() == "" or self.labelHesKodu.text() == "" :
                self.hataGoster("Güncellenecek kişiyi önce sorgulamanız gerekli.")
                return
            else:
                self.widget.widgetHesKodu.setText(self.labelHesKodu.text())
                self.widget.widgetTcKimlikNo.setText(self.tcKimlikNo.text())
                self.widget.widgetDurum.setText(self.durum.text())
                self.widget.widgetResim.setPixmap(self.resim.pixmap())
                self.widget.widgetKaydet.setText("Güncelle")
        

        

        
        self.widget.widgetIptal.clicked.connect(self.widget.destroy)
        self.widget.widgetKaydet.clicked.connect(self.kaydet)
        self.widget.widgetResimEkle.clicked.connect(self.resimEkle)

        
        self.widget.exec_()
        
    
    
    def resimEkle(self):
        
        resimAdi, _ = QFileDialog.getOpenFileName(self.widget, "Resim seç...", "C:\\")
        try:
            if resimAdi != "":
                mResim = QPixmap(resimAdi)
                self.widget.widgetResim.setPixmap(mResim)
                self.eklenenResim = resimAdi
                print(resimAdi)
        except:
            return



    def sil(self):
        if self.tcKimlikNo.text() == "" or self.labelHesKodu.text() == "":
            self.hataGoster("Silinecek kişiyi sorgulamanız gerekli.")
            return
        
        #TODO Burada veritabanından eleman silinecek.

    
    def kaydet(self):
        kimlikNo = self.widget.widgetTcKimlikNo.text()
        hesKodu = self.widget.widgetHesKodu.text()
        durum = self.widget.widgetDurum.text()
        
        if self.widget.widgetKaydet.text() == "Kaydet":
            #*Bilgilerde eksiklik varsa durdurulacak.
            bilgilerTam = hesKodu != "" and kimlikNo !="" and durum != "" and self.eklenenResim != ""
            if not bilgilerTam:
                self.hataGoster("Bilgileri eksiksiz girmelisiniz.")
                return
            #TODO Yeni kayıt kaydedilecek
            
        else:
            bilgilerTam = hesKodu != "" and kimlikNo != "" and durum != ""
            if not bilgilerTam:
                self.hataGoster("Bilgileri eksiksiz girmelisiniz.")
                return
            #TODO Eski kayıt güncellenecek
            

    
    
    def hataGoster(self, hata):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText(hata)
        msg.setWindowTitle("Hata")
        msg.exec_()
        
        
    def sonucGeldimi(self):
        try: 
            br=self.br
            tc_sonu = br.find_elements_by_class_name("compact")[0].find_elements_by_tag_name("dd")[0].get_attribute("innerText")
            hes = br.find_elements_by_class_name("compact")[0].find_elements_by_tag_name("dd")[1].get_attribute("innerText")
            durum = br.find_elements_by_class_name("compact")[0].find_elements_by_tag_name("dd")[2].get_attribute("innerText")
            return (tc_sonu, hes, durum)

        except:
            return (False, False, False)
    
    
    def eDevlettenSorgula(self,tcKimlik, sifre, hesKodu):

        self.TIMEOUT = 10
        url = "https://giris.turkiye.gov.tr/Giris/"
        url1 = "https://www.turkiye.gov.tr/saglik-bakanligi-hes-kodu-sorgulama"


        options = Options()
        options.add_argument('--headless')

        self.br = Firefox(options=options)
        br= self.br
        br.get(url)
        """
        hes1 = "F1D9954714"
        hes2 = "A8U2525219"
        hes3 = "U2A9438817"
        """
        br.find_element_by_id("tridField").send_keys(tcKimlik)
        br.find_element_by_id("egpField").send_keys(sifre)
        br.find_elements_by_class_name("submitButton")[0].click()

        sayac = 0
        br.get(url1)
        #! Burada hata verirse edevlet girişi yapılamadı demek oluyor.
        
        try:

            br.find_element_by_id("hes_kodu").send_keys(hesKodu)
            br.find_elements_by_class_name("submitButton")[0].click()
                
            
            while(True):
                tc_sonu, hes, durum = self.sonucGeldimi()
                if tc_sonu or sayac > self.TIMEOUT:
                    break
                sayac += 1
                time.sleep(1)


            br.find_elements_by_class_name("userMenuButton")[0].click()
            br.find_elements_by_class_name("logout")[0].click()
            br.close()
            
            #return tc_sonu, hes, durum
            self.yukleniyorAnimasyonuKapat()
            
            if tc_sonu:
                self.labelHesKodu.setText(hes)
                self.tcKimlikNo.setText(tc_sonu)
                self.durum.setText(durum)
            else:
                #self.labelHesKodu.setText("Hatalı HES")
                self.hataMesaji("Hatalı HES kodu!")
            
            
        except:
            br.close()
            self.yukleniyorAnimasyonuKapat()
            #self.labelHesKodu.setText("Giriş başarısız")
            self.hataMesaji("E-Devlet girişi başarısız!")
            

        



if __name__  == "__main__":
    app = QApplication(sys.argv)
    window = MWindow()
    sys.exit( app.exec_() )