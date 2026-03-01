"""
Modulo per gestire i test di velocità della connessione.
Incapsula tutta la logica di interazione con speedtest-cli.
"""

import sys
import os
import threading

# Fix per PyInstaller: quando l'app è "frozen" (compilata),
# sys.stdout/stderr potrebbero essere None. speedtest-cli prova
# ad accedere a .fileno() su questi oggetti, causando l'errore.
# Creiamo dei file handle fittizi se necessario.
if getattr(sys, 'frozen', False):
    # Applicazione frozen (compilata con PyInstaller)
    if sys.stdout is None or not hasattr(sys.stdout, 'fileno'):
        # Reindirizza stdout verso un file temporaneo o devnull
        sys.stdout = open(os.devnull, 'w')
    if sys.stderr is None or not hasattr(sys.stderr, 'fileno'):
        sys.stderr = open(os.devnull, 'w')
    if sys.stdin is None or not hasattr(sys.stdin, 'fileno'):
        sys.stdin = open(os.devnull, 'r')

import speedtest

class SpeedTestService:
    """Servizio per eseguire test di velocità della connessione internet"""
    
    def __init__(self):
        """Inizializza il servizio speedtest"""
        self._stop_requested = False
        
    def run_test(self, on_ping, on_download, on_upload, on_error, on_progress_check):
        """
        Esegue un test di velocità completo.
        
        Args:
            on_ping: Callback chiamata con il valore del ping (in ms)
            on_download: Callback chiamata con la velocità di download (in Mbps)
            on_upload: Callback chiamata con la velocità di upload (in Mbps)
            on_error: Callback chiamata in caso di errore (riceve l'eccezione)
            on_progress_check: Callback che ritorna True se il test deve essere interrotto
        
        Returns:
            bool: True se completato con successo, False altrimenti
        """
        try:
            # Reset flag di stop
            self._stop_requested = False
            
            # ===== FASE 1: TEST DEL PING =====
            # Crea istanza Speedtest
            st = speedtest.Speedtest(secure=True)
            
            # Trova il server migliore
            st.get_best_server()
            
            # Ottiene il ping
            ping = st.results.ping
            on_ping(ping)
            
            # Check interruzione
            if on_progress_check():
                return False
            
            # ===== FASE 2: TEST DEL DOWNLOAD =====
            download = st.download() / 1_000_000  # Converti in Mbps
            on_download(download)
            
            # Check interruzione
            if on_progress_check():
                return False
            
            # ===== FASE 3: TEST DELL'UPLOAD =====
            upload = st.upload() / 1_000_000  # Converti in Mbps
            on_upload(upload)
            
            return True
            
        except Exception as e:
            on_error(e)
            return False
    
    def run_test_async(self, callbacks, on_complete):
        """
        Esegue il test in un thread separato.
        
        Args:
            callbacks: Dizionario con i callback (on_ping, on_download, on_upload, on_error, on_progress_check)
            on_complete: Callback chiamata al termine (riceve True/False per successo)
        """
        def _run():
            success = self.run_test(**callbacks)
            on_complete(success)
        
        thread = threading.Thread(target=_run, daemon=True)
        thread.start()
    
    def request_stop(self):
        """Richiede l'interruzione del test corrente"""
        self._stop_requested = True
