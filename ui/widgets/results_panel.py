"""
Panel per visualizzare i risultati del test (ping, download, upload, errori, progress).
"""

import customtkinter

class ResultsPanel:
    """Panel che contiene tutti i widget per mostrare i risultati del test"""
    
    def __init__(self, parent):
        """
        Crea il panel dei risultati.
        
        Args:
            parent: Widget padre
        """
        self.parent = parent
        
        # Label per il ping (riga 0, colonna 0)
        self.label_ping = customtkinter.CTkLabel(parent, text="Ping: - ms")
        self.label_ping.grid(row=0, column=0, padx=20, pady=(20, 5), sticky="w")
        
        # Label per il download (riga 1, colonna 0)
        self.label_download = customtkinter.CTkLabel(parent, text="Download: - Mbps")
        self.label_download.grid(row=1, column=0, padx=20, pady=5, sticky="w")
        
        # Label per l'upload (riga 2, colonna 0)
        self.label_upload = customtkinter.CTkLabel(parent, text="Upload: - Mbps")
        self.label_upload.grid(row=2, column=0, padx=20, pady=5, sticky="w")
        
        # Label per gli errori (riga 3, occupa 2 colonne)
        self.label_error = customtkinter.CTkLabel(
            parent, 
            text="", 
            text_color="red", 
            font=("Roboto", 14, "bold")
        )
        self.label_error.grid(row=3, column=0, columnspan=2, padx=20, pady=5, sticky="w")
        
        # Barra di avanzamento (riga 4, occupa 2 colonne)
        self.progress_bar = customtkinter.CTkProgressBar(parent, width=340)
        self.progress_bar.grid(row=4, column=0, columnspan=2, padx=20, pady=(5, 10), sticky="ew")
        self.progress_bar.set(0)
        self.progress_bar.grid_remove()  # Nasconde la barra inizialmente
    
    def update_ping(self, value):
        """Aggiorna il valore del ping"""
        if isinstance(value, str):
            self.label_ping.configure(text=value)
        else:
            self.label_ping.configure(text=f"Ping: {int(value)} ms")
    
    def update_download(self, value):
        """Aggiorna il valore del download"""
        if isinstance(value, str):
            self.label_download.configure(text=value)
        else:
            self.label_download.configure(text=f"Download: {value:.2f} Mbps")
    
    def update_upload(self, value):
        """Aggiorna il valore dell'upload"""
        if isinstance(value, str):
            self.label_upload.configure(text=value)
        else:
            self.label_upload.configure(text=f"Upload: {value:.2f} Mbps")
    
    def update_error(self, message):
        """Mostra un messaggio di errore"""
        self.label_error.configure(text=message)
    
    def update_progress(self, value):
        """Aggiorna la barra di avanzamento (0.0 - 1.0)"""
        # Mostra la barra quando viene aggiornata
        self.progress_bar.grid(row=4, column=0, columnspan=2, padx=20, pady=(5, 10), sticky="ew")
        self.progress_bar.set(value)
    
    def reset(self):
        """Resetta tutti i valori ai default"""
        self.label_ping.configure(text="Ping: - ms")
        self.label_download.configure(text="Download: - Mbps")
        self.label_upload.configure(text="Upload: - Mbps")
        self.label_error.configure(text="")
        self.progress_bar.set(0)
        self.progress_bar.grid_remove()  # Nasconde la barra
