from email import message
import tkinter as tk

from tkinter import Toplevel, ttk, font
from tkinter import messagebox

class Interfaz(tk.Tk):
    __sinIVA = None
    __IVA = None
    __conIVA = None
    __band = None
    def __init__(self):
        super().__init__()
        super().title('Ejercicio 2')
        fuente = font.Font(font='Arial', weight='normal')
        #INICIALIZACIÓN
        self.__sinIVA = tk.StringVar()
        self.__IVA = tk.StringVar()
        self.__conIVA = tk.StringVar()
        self.__band = tk.IntVar()
        self.frame1 = tk.Frame(self)
        self.frame2 = tk.Frame(self.frame1, borderwidth=2, relief='groove')
        self.sinLBL = tk.Label()
        self.ivaLBL = tk.Label()
        self.conLBL = tk.Label()
        self.ctext1 = tk.Entry()
        #...
        self.boton1 = tk.Button()
        self.boton2 = tk.Button()
        self.iva1 = ttk.Radiobutton(self.frame2, text='IVA 21%', value=0, variable=self.__band, command=self.calcular)
        self.iva2 = ttk.Radiobutton(self.frame2, text='IVA 10.5%', value = 1, variable=self.__band, command=self.calcular)
    def  calcular(self):
        try:
            if(self.__band == 0):
                iva = float(self.__sinIVA.get())*0.21
                resultado = float(self.__sinIVA.get()) + iva
                self.__IVA.set('{:.3}'.format(iva))
                self.__conIVA.set('{:.3}'.format(resultado))
            elif(self.__band == 1):
                iva = float(self.__sinIVA.get())*0.105
                resultado = float(self.__sinIVA.get()) + iva
                self.__IVA.set('{:.3}'.format(iva))
                self.__conIVA.set('{:.3}'.format(resultado))
            else:
                pass
        except ValueError:
            messagebox.showerror('ERROR: valor ingresado')