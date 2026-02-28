"""
Speed App - Applicazione per testare la velocità della connessione internet.

Entry point dell'applicazione.
"""

import customtkinter
from ui.app_window import AppWindow

def main():
    """Funzione principale che avvia l'applicazione"""
    # Imposta il tema scuro come default
    customtkinter.set_appearance_mode("dark")
    
    # Crea e avvia l'applicazione
    app = AppWindow()
    app.mainloop()

if __name__ == "__main__":
    main()
