import csv
import time
import tkinter as tk
from tkinter import scrolledtext

class Tir:
    def __init__(self, geliş_zamanı, ülke, _20_ton_adet, _30_ton_adet, yük_miktarı, maliyet):
        self.geliş_zamanı = geliş_zamanı
        self.ülke = ülke
        self._20_ton_adet = _20_ton_adet
        self._30_ton_adet = _30_ton_adet
        self.yük_miktarı = yük_miktarı
        self.maliyet = maliyet

class Gemi:
    def __init__(self, geliş_zamanı, gemi_adı, kapasite, gidecek_ülke):
        self.geliş_zamanı = geliş_zamanı
        self.gemi_adı = gemi_adı
        self.kapasite = kapasite
        self.gidecek_ülke = gidecek_ülke

class IstifAlan:
    def __init__(self, kapasite):
        self.kapasite = kapasite
        self.total = 0
        self.indirilen_yukler = []
        self.ulke_listesi = []

    def indir(self, tir):
        if self.total + tir.yük_miktarı <= self.kapasite:
            self.total += tir.yük_miktarı
            self.indirilen_yukler.append(tir.yük_miktarı)
            self.ulke_listesi.append(tir.ülke)
            return True
        else:
            return False

    def gemiye_yukle(self, gemi):
        if self.ulke_listesi and gemi.gidecek_ülke in self.ulke_listesi:
            indeks = self.ulke_listesi.index(gemi.gidecek_ülke)
            yuk = self.indirilen_yukler.pop(indeks)
            self.ulke_listesi.pop(indeks)
            self.total -= yuk
            return yuk
        else:
            return 0


class Liman:
    def __init__(self, root):
        self.root = root
        self.istif1 = IstifAlan(750)
        self.istif2 = IstifAlan(750)
        self.tir_listesi = []
        self.gemi_listesi = []
        self.indirilen_yukler = []
        self.yuklenen_yukler = []

    def tir_bilgisi_okuma(self, dosya_yolu):
        with open(dosya_yolu, newline='', encoding='latin-1') as dosya:
            csv_reader = csv.reader(dosya)
            next(csv_reader)  # Başlık satırını atla
            for row in csv_reader:
                geliş_zamanı, tır_plakası, ülke, _20_ton_adet, _30_ton_adet, yük_miktarı, maliyet = row
                tir = Tir(geliş_zamanı, ülke, int(_20_ton_adet), int(_30_ton_adet), int(yük_miktarı), int(maliyet))
                self.tir_listesi.append(tir)

    def gemi_bilgisi_okuma(self, dosya_yolu):
        with open(dosya_yolu, newline='', encoding='latin-1') as dosya:
            csv_reader = csv.reader(dosya)
            next(csv_reader)  # Başlık satırını atla
            for row in csv_reader:
                geliş_zamanı, gemi_adı, kapasite, gidecek_ülke = row
                gemi = Gemi(geliş_zamanı, gemi_adı, int(kapasite), gidecek_ülke)
                self.gemi_listesi.append(gemi)

    def gemiye_yukle_ve_gonder(self, gemi, istif):
        while istif.total < istif.kapasite * 0.95 and istif.indirilen_yukler:
            yuk = istif.gemiye_yukle(gemi)
            if yuk > 0:
                self.yuklenen_yukler.append(yuk)
            else:
                break
        return istif.total

    def indir_ve_istifle(self, tir, istif1, istif2):
        if istif1.indir(tir):
            self.indirilen_yukler.append(tir.yük_miktarı)
        elif istif2.indir(tir):
            self.indirilen_yukler.append(tir.yük_miktarı)

    def main(self):
        self.tir_bilgisi_okuma('C:\\Users\\emirh\\Desktop\\olaylar.csv')
        self.gemi_bilgisi_okuma('C:\\Users\\emirh\\Desktop\\gemiler.csv')

        for tir in self.tir_listesi:
            self.indir_ve_istifle(tir, self.istif1, self.istif2)

            if self.istif1.total == self.istif1.kapasite or self.istif2.total == self.istif2.kapasite:
                for gemi in self.gemi_listesi:
                    if gemi.gidecek_ülke in self.istif1.ulke_listesi:
                        indeks = self.istif1.ulke_listesi.index(gemi.gidecek_ülke)
                        yuk = self.istif1.indirilen_yukler.pop(indeks)
                        self.istif1.ulke_listesi.pop(indeks)
                        self.istif1.total -= yuk
                        self.gemiye_yukle_ve_gonder(gemi, self.istif1)

                    elif gemi.gidecek_ülke in self.istif2.ulke_listesi:
                        indeks = self.istif2.ulke_listesi.index(gemi.gidecek_ülke)
                        yuk = self.istif2.indirilen_yukler.pop(indeks)
                        self.istif2.ulke_listesi.pop(indeks)
                        self.istif2.total -= yuk
                        self.gemiye_yukle_ve_gonder(gemi, self.istif2)

            time.sleep(1)  # Simülasyonu biraz yavaşlatmak için

            self.root.update_idletasks()
            self.root.update()

            self.root.after(100, self.main)


def start_simulation():
    root = tk.Tk()
    root.title("Liman Simülasyonu")

    text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=80, height=20)
    text_area.pack(expand=tk.YES, fill=tk.BOTH)

    liman = Liman(root)

    def update_text():
        nonlocal text_area
        text_area.delete(1.0, tk.END)
        text_area.insert(tk.END, f"İndirilen Yükler: {liman.indirilen_yukler}\n")
        text_area.insert(tk.END, f"Yüklenen Yükler: {liman.yuklenen_yukler}\n")
        text_area.after(100, update_text)

    update_text()

    root.after(100, liman.main)
    root.mainloop()


if __name__ == "__main__":
    start_simulation()
