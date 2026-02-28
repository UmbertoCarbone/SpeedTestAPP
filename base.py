# Importa la libreria customtkinter per creare l'interfaccia grafica moderna
import customtkinter
# Importa la libreria speedtest per eseguire i test di velocità
import speedtest
# Importa threading per eseguire operazioni in background senza bloccare l'interfaccia
import threading

# Definisce la classe principale dell'applicazione che eredita da CTk (finestra principale)
class App(customtkinter.CTk):
    def __init__(self):
        # Chiama il costruttore della classe base CTk
        super().__init__()
        # Imposta il titolo della finestra
        self.title("Speed App")
        # Imposta la dimensione iniziale della finestra (larghezza x altezza)
        self.geometry("400x350")
        # Imposta la dimensione minima della finestra (non può essere più piccola)
        self.minsize(400, 350)
        # Imposta la dimensione massima della finestra (non può essere più grande)
        self.maxsize(400, 350)
        # Imposta l'icona della finestra usando un file .ico
        self.iconbitmap("icon.ico")
        # Configura la colonna 0 della griglia per espandersi (weight=1)
        self.grid_columnconfigure(0, weight=1)
        # Configura la riga 3 della griglia per espandersi, spingendo il bottone verso il basso
        self.grid_rowconfigure(3, weight=1)
        
        # Variabile per tenere traccia del tema corrente
        self.current_theme = "dark"
        
        # Crea il bottone per cambiare tema (in alto a destra)
        self.theme_button = customtkinter.CTkButton(
            self, 
            text="☀️", 
            command=self.toggle_theme, 
            width=35, 
            height=35, 
            font=("Segoe UI Emoji", 18),
            corner_radius=8
        )
        # Posiziona il bottone del tema in alto a destra
        self.theme_button.grid(row=0, column=1, padx=20, pady=(20, 5), sticky="e")

        # Crea la label per mostrare il ping
        self.label_ping = customtkinter.CTkLabel(self, text="Ping: - ms")
        # Posiziona la label del ping nella griglia (riga 0, colonna 0)
        self.label_ping.grid(row=0, column=0, padx=20, pady=(20, 5), sticky="w")
        # Crea la label per mostrare la velocità di download
        self.label_download = customtkinter.CTkLabel(self, text="Download: - Mbps")
        # Posiziona la label del download nella griglia (riga 1, colonna 0)
        self.label_download.grid(row=1, column=0, padx=20, pady=5, sticky="w")
        # Crea la label per mostrare la velocità di upload
        self.label_upload = customtkinter.CTkLabel(self, text="Upload: - Mbps")
        # Posiziona la label dell'upload nella griglia (riga 2, colonna 0)
        self.label_upload.grid(row=2, column=0, padx=20, pady=5, sticky="w")
        
        # Crea una label per gli errori (testo rosso e grassetto)
        self.label_error = customtkinter.CTkLabel(self, text="", text_color="red", font=("Roboto", 14, "bold"))
        # Posiziona la label degli errori nella griglia (riga 3, occupa 2 colonne)
        self.label_error.grid(row=3, column=0, columnspan=2, padx=20, pady=5, sticky="w")
        
        # Crea una barra di avanzamento per mostrare il progresso del test
        self.progress_bar = customtkinter.CTkProgressBar(self, width=340)
        # Posiziona la barra di avanzamento nella griglia (riga 4, occupa 2 colonne)
        self.progress_bar.grid(row=4, column=0, columnspan=2, padx=20, pady=(5, 10), sticky="ew")
        # Imposta la barra a 0 (vuota) all'inizio
        self.progress_bar.set(0)

        # Crea il bottone verde "Avvia Speedtest"
        self.button = customtkinter.CTkButton(self, text="Avvia Speedtest", command=self.button_callback, width=160, height=40, fg_color="green", hover_color="green")
        # Posiziona il bottone nella griglia (riga 5, colonna 0)
        self.button.grid(row=5, column=0, padx=(20, 5), pady=(20, 5), sticky="ew")
        # Crea il bottone rosso "Interrompi test" (disabilitato all'inizio)
        self.stop_button = customtkinter.CTkButton(self, text="Interrompi test", command=self.stop_test, fg_color="red", state="disabled", width=160, height=40, hover_color="red")
        # Posiziona il bottone stop nella griglia (riga 5, colonna 1)
        self.stop_button.grid(row=5, column=1, padx=(5, 20), pady=(20, 5), sticky="ew")
        
        # Crea il bottone per azzerare i risultati (disabilitato all'inizio)
        self.reset_button = customtkinter.CTkButton(self, text="Azzera risultati", command=self.reset_results, state="disabled", width=340, height=40)
        # Posiziona il bottone reset nella griglia (riga 6, occupa 2 colonne)
        self.reset_button.grid(row=6, column=0, columnspan=2, padx=20, pady=(5, 20), sticky="ew")

        # Variabile per tenere traccia se l'utente ha richiesto l'interruzione del test
        self._stop_requested = False
        # Durata in secondi di ogni fase del test (ping, download, upload)
        self.test_duration = 10
        # Variabili per l'animazione dei pallini
        self._animation_running = False
        self._dot_count = 0
        self._current_phase = None
        # Variabile per tracciare se è stato completato almeno un test
        self._test_completed = False  

    # Metodo chiamato quando si preme il bottone "Avvia Speedtest"
    def button_callback(self):
        # Disabilita il bottone "Avvia Speedtest" per evitare click multipli
        self.button.configure(state="disabled")
        # Abilita il bottone "Interrompi test" per permettere l'interruzione
        self.stop_button.configure(state="normal")
        # Disabilita il bottone "Azzera risultati" durante il test
        self.reset_button.configure(state="disabled")
        # Reset della variabile di interruzione (nessuna richiesta di stop)
        self._stop_requested = False
        # Cancella eventuali messaggi di errore precedenti
        self.label_error.configure(text="")
        # Resetta la barra di avanzamento a 0
        self.progress_bar.set(0)
        # Avvia il test in un thread separato per non bloccare l'interfaccia
        threading.Thread(target=self.run_speedtest, daemon=True).start()

    # Metodo chiamato quando si preme il bottone "Interrompi test"
    def stop_test(self):
        # Imposta la variabile a True per segnalare che il test deve essere interrotto
        self._stop_requested = True        # Segna che il test NON è stato completato (è stato interrotto)
        self._test_completed = False        # Ferma l'animazione dei pallini
        self._stop_animation()
        # Resetta la label del ping al valore iniziale
        self.label_ping.configure(text="Ping: - ms")
        # Resetta la label del download al valore iniziale
        self.label_download.configure(text="Download: - Mbps")
        # Resetta la label dell'upload al valore iniziale
        self.label_upload.configure(text="Upload: - Mbps")
        # Cancella eventuali messaggi di errore
        self.label_error.configure(text="")
        # Resetta la barra di avanzamento a 0
        self.progress_bar.set(-1)
        # Aggiorna l'interfaccia per mostrare le modifiche
        self.update()

    # Metodo che esegue il test di velocità (viene eseguito in un thread separato)
    def run_speedtest(self):
        try:
            # ===== FASE 1: TEST DEL PING =====
            # Avvia l'animazione dei pallini per il ping
            self._start_animation("ping")
            
            # Crea un'istanza dell'oggetto Speedtest per eseguire i test
            # Usa secure=False per evitare problemi SSL
            st = speedtest.Speedtest(secure=True)
            # Imposta un timeout più lungo
            st.timeout = 10
            # Trova il server migliore da usare per il test
            st.get_best_server()
            
            # Ottiene il valore del ping dal test (già eseguito da get_best_server)
            ping = st.results.ping
            # Ferma l'animazione e mostra il risultato
            self._stop_animation()
            # Mostra il valore del ping nella label (con 2 decimali)
            self.label_ping.configure(text=f"Ping: {ping:.2f} ms")
            # Aggiorna la barra di avanzamento a 33%
            self.progress_bar.set(0.33)
            # Aggiorna l'interfaccia
            self.update()
            
            # Controlla se l'utente ha richiesto l'interruzione
            if self._stop_requested:
                self.reset_buttons()
                return
            
            # ===== FASE 2: TEST DEL DOWNLOAD =====
            # Avvia l'animazione dei pallini per il download
            self._start_animation("download")
            # Esegue il test di download e converte in Mbps (diviso per 1.000.000)
            download = st.download() / 1_000_000
            # Ferma l'animazione e mostra il risultato
            self._stop_animation()
            # Mostra il valore del download nella label (con 2 decimali)
            self.label_download.configure(text=f"Download: {download:.2f} Mbps")
            # Aggiorna la barra di avanzamento a 66%
            self.progress_bar.set(0.66)
            # Aggiorna l'interfaccia
            self.update()
            
            # Controlla se l'utente ha richiesto l'interruzione
            if self._stop_requested:
                self.reset_buttons()
                return
            
            # ===== FASE 3: TEST DELL'UPLOAD =====
            # Avvia l'animazione dei pallini per l'upload
            self._start_animation("upload")
            # Esegue il test di upload e converte in Mbps (diviso per 1.000.000)
            upload = st.upload() / 1_000_000
            # Ferma l'animazione e mostra il risultato
            self._stop_animation()
            # Mostra il valore dell'upload nella label (con 2 decimali)
            self.label_upload.configure(text=f"Upload: {upload:.2f} Mbps")
            # Aggiorna la barra di avanzamento a 100%
            self.progress_bar.set(1.0)
            # Aggiorna l'interfaccia
            self.update()
            # Segna che il test è stato completato con successo
            self._test_completed = True
        except Exception as e:
            # Se si verifica un errore, mostra i dettagli per capire il problema
            # Ferma l'animazione se è in corso
            self._stop_animation()
            # Resetta tutte le label ai valori iniziali
            self.label_ping.configure(text="Ping: - ms")
            self.label_download.configure(text="Download: - Mbps")
            self.label_upload.configure(text="Upload: - Mbps")
            # Mostra il messaggio di errore specifico in rosso
            self.label_error.configure(text=f"Errore: {str(e)[:50]}")
            # Resetta la barra di avanzamento
            self.progress_bar.set(0)
            # Aggiorna l'interfaccia
            self.update()
            # Stampa l'errore completo nel terminale per debug
            print(f"Errore durante il test: {e}")
            # Segna che il test NON è stato completato con successo
            self._test_completed = False
        # Alla fine del test (o in caso di errore), riabilita i bottoni
        self.reset_buttons()

    # Metodo che riporta i bottoni allo stato iniziale
    def reset_buttons(self):
        # Riabilita il bottone "Avvia Speedtest" per permettere un nuovo test
        self.button.configure(state="normal")
        # Disabilita il bottone "Interrompi test" perché non c'è test in corso
        self.stop_button.configure(state="disabled")
        # Abilita il bottone "Azzera risultati" solo se il test è stato completato con successo
        if self._test_completed:
            self.reset_button.configure(state="normal")

    # Metodo che azzera i risultati del test
    def reset_results(self):
        # Resetta la label del ping al valore iniziale
        self.label_ping.configure(text="Ping: - ms")
        # Resetta la label del download al valore iniziale
        self.label_download.configure(text="Download: - Mbps")
        # Resetta la label dell'upload al valore iniziale
        self.label_upload.configure(text="Upload: - Mbps")
        # Cancella eventuali messaggi di errore
        self.label_error.configure(text="")
        # Resetta la barra di avanzamento a 0
        self.progress_bar.set(0)
        # Disabilita il bottone "Azzera risultati" perché non ci sono più risultati
        self.reset_button.configure(state="disabled")
        # Segna che non c'è più un test completato
        self._test_completed = False

    # Metodo che cambia il tema tra scuro e chiaro
    def toggle_theme(self):
        # Se il tema corrente è scuro, passa a chiaro
        if self.current_theme == "dark":
            customtkinter.set_appearance_mode("light")
            self.current_theme = "light"
            # Cambia il testo del bottone per indicare l'azione successiva
            self.theme_button.configure(text="🌙")
        # Altrimenti passa a scuro
        else:
            customtkinter.set_appearance_mode("dark")
            self.current_theme = "dark"
            # Cambia il testo del bottone per indicare l'azione successiva
            self.theme_button.configure(text="☀️")

    # Metodo che avvia l'animazione dei pallini per una fase specifica
    def _start_animation(self, phase):
        # Imposta la fase corrente (ping, download, upload)
        self._current_phase = phase
        # Imposta l'animazione come attiva
        self._animation_running = True
        # Inizia dal primo pallino
        self._dot_count = 0
        # Avvia il ciclo di animazione
        self._animate_dots()

    # Metodo che ferma l'animazione dei pallini
    def _stop_animation(self):
        # Imposta l'animazione come non attiva
        self._animation_running = False

    # Metodo che aggiorna ciclicamente i pallini (da 1 a 3)
    def _animate_dots(self):
        # Se l'animazione non è più attiva, esci
        if not self._animation_running:
            return
        
        # Incrementa il contatore dei pallini (da 1 a 3, poi ricomincia)
        self._dot_count = (self._dot_count % 3) + 1
        # Crea la stringa dei pallini in base al contatore
        dots = "." * self._dot_count
        
        # Aggiorna la label corretta in base alla fase
        if self._current_phase == "ping":
            self.label_ping.configure(text=f"Ping: in corso{dots}")
        elif self._current_phase == "download":
            self.label_download.configure(text=f"Download: in corso{dots}")
        elif self._current_phase == "upload":
            self.label_upload.configure(text=f"Upload: in corso{dots}")
        
        # Richiama questo metodo dopo 500ms per continuare l'animazione
        self.after(500, self._animate_dots)

# Punto di ingresso del programma
if __name__ == "__main__":
    # Crea un'istanza dell'applicazione
    app = App()
    # Avvia il ciclo principale dell'interfaccia grafica (tiene aperta la finestra)
    app.mainloop()