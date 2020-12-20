import sqlite3
from PyQt5.QtGui import QPixmap



class DB:

    @staticmethod
    def veritabani():
        db = sqlite3.connect("okul.db")
        cur = db.cursor()
        
        q= """CREATE TABLE IF NOT EXISTS "ogrenciler" (
                "tc_no"	TEXT UNIQUE,
                "isim"	TEXT,
                "soyad"	TEXT,
                "okul_no"	INTEGER UNIQUE,
                "sinif"	TEXT,
                "fotograf"	BLOB,
                "hes_kodu"	TEXT UNIQUE,
                "durum"	NUMERIC,
                PRIMARY KEY("tc_no","okul_no")
                )"""
        cur.execute(q)
        db.commit()
        return db
    
    
    def resimdonustur(fonk):
        def donustur(*args):
            resim_vt_index = 5
            donus_listesi = []
            
            sonuc = fonk(*args)
            #Sorgu veritabanında bulunamadı.
            if sonuc == None:
                return donus_listesi
            
            #Tek sonuç geldi.
            if isinstance(sonuc, tuple):
                
                blob_data = sonuc[resim_vt_index]
                donus_listesi = [*sonuc]
                
                qp = QPixmap()
                qp.loadFromData(blob_data)
                donus_listesi[resim_vt_index]=qp
            
            else:
                #Liste geldi.
                for i in sonuc:
                    blob_data = i[resim_vt_index]
                    #image_data = pickle.loads(blob_data)
                    qp = QPixmap() 
                    qp.loadFromData(blob_data)
                    
                    tmp = [*i]
                    tmp[resim_vt_index] = qp
                    donus_listesi.append(tmp)   
            
            return donus_listesi
        return donustur
    
    
    def yoldanblobdata(fonk):
        # gelen liste [[],[],[]] şeklinde olacak.
        resim_vt_index = 5
        
        def donustur(*args):
            donus_listesi = []
            liste = [*args][0]
            print(len(liste))
            
            #Tek kayıt, yoldan resim okunup listeye geri ekleniyor.
            if len(liste) == 1:
                with open(liste[0][resim_vt_index], "rb") as dosya:
                    blob_data = dosya.read()
                    liste[0][resim_vt_index] = blob_data
                    
                    donus_listesi.append(tuple(liste[0]))
                    
                     
            #Kayıt birden fazla
            elif len(liste) > 1:
                for ogrenci in liste:
                    tek_ogrenci = [*ogrenci]
                    with open(tek_ogrenci[resim_vt_index], "rb") as dosya:
                        blob_data = dosya.read()
                        tek_ogrenci[resim_vt_index] = blob_data
                        
                        donus_listesi.append(tuple(tek_ogrenci))
                      
            fonk(donus_listesi)
        
        return donustur  
                
        
        
    
    
    @staticmethod
    @resimdonustur
    def tc_sonu_ile(son_uc):
    
        with DB.veritabani() as db:
            son_uc = "%{}".format(son_uc)
            #son_uc = "\"%" + son_uc + "\""
            q = """SELECT * FROM ogrenciler WHERE tc_no LIKE ?"""
            cur = db.cursor()
            cur.execute(q, (son_uc,))
            return cur.fetchall()
            

    @staticmethod
    @resimdonustur
    def hes_kodu_ile(hes):
        with DB.veritabani() as db:
            q = """SELECT * FROM ogrenciler WHERE hes_kodu= ?"""
            cur = db.cursor()
            cur.execute(q, (hes,))
            return cur.fetchone()
        
    
    @staticmethod
    @resimdonustur
    def hes_kodu_listesi_ile(hesListesi):
        with DB.veritabani() as db:
            #(?,?,?,?,?,...,?) yapısı oluşturuluyor.
            q = """SELECT * FROM ogrenciler WHERE hes_kodu IN ({})""".format(("?," * len(hesListesi))[:-1])
            cur = db.cursor()
            cur.execute(q, hesListesi)
            return cur.fetchall()

    
    @staticmethod
    @resimdonustur
    def tc_no_ile(tc_no):
        with DB.veritabani() as db:
            q= """SELECT * FROM ogrenciler WHERE tc_no= ?"""
            cur = db.cursor()
            cur.execute(q, (tc_no,))
            return cur.fetchone()
    
    @staticmethod
    @resimdonustur
    def okul_no_ile(okul_no):
        with DB.veritabani() as db:
            q= """SELECT * FROM ogrenciler WHERE okul_no= ?"""
            cur = db.cursor()
            cur.execute(q, (okul_no,))
            return cur.fetchone()
   
    @staticmethod
    def sinif_isimleri():
        with DB.veritabani() as db:
            q = """SELECT DISTINCT sinif FROM ogrenciler WHERE sinif NOTNULL"""
            cur = db.cursor()
            cur.execute(q)
            return cur.fetchall()
    
    

    @staticmethod
    @yoldanblobdata
    def toplu_kayit_ekle(liste):
        #Çalıştırılırken toplu_kayit_ekle([[ogrenci1], [ogrenci2],[ogrenci3]]) şeklinde gönderilecek.
        #dekorator [(),(),()] şekline çevirecek.
        with DB.veritabani() as db:
            cur = db.cursor()
            q = """INSERT OR REPLACE INTO ogrenciler VALUES(?,?,?,?,?,?,?,?)"""
            cur.executemany(q, liste)
            db.commit()
    
    
    @staticmethod
    def sinifa_gore_hes_kodlari():
        with DB.veritabani() as db:
            cur = db.cursor()
            q = """SELECT sinif, hes_kodu FROM ogrenciler """
            cur.execute(q)
            return cur.fetchall()
    
    
    
    @staticmethod
    def veriguncelle(okul_no,sinif,hes_kodu):
        with DB.veritabani() as con:
            cursor = con.cursor()
            cursor.execute("Update ogrenciler  SET sinif = ? ,hes_kodu = ?  WHERE okul_no = ? ", (sinif, hes_kodu, okul_no))
            con.commit()
  

    @staticmethod
    def kayitsil(okul_no):
        with DB.veritabani() as con:
            cursor = con.cursor()
            cursor.execute("Delete  From ogrenciler where okul_no = ?", (okul_no,))
            con.commit()
    
    @staticmethod
    def sinif_sil(sinif):
        with DB.veritabani() as con:
            cursor = con.cursor()
            cursor.execute("Delete  From ogrenciler where sinif = ?", (sinif,))
            con.commit()
            


    @staticmethod
    def veritabanisil():
        with DB.veritabani() as con:
            cursor = con.cursor()
            cursor.execute("Delete From ogrenciler WHERE 1=1 " )
            con.commit()
        
