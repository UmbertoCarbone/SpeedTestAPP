"""
Finestra principale dell'applicazione.
Coordina tutti i componenti e la business logic.
"""

import customtkinter
from ui.widgets.theme_button import ThemeButton
from ui.widgets.results_panel import ResultsPanel
from ui.widgets.control_panel import ControlPanel
from services.speedtest_service import SpeedTestService
from utils.animations import DotAnimator

class AppWindow(customtkinter.CTk):
    """Finestra principale dell'applicazione Speed App"""
    
    def __init__(self):
        """Inizializza la finestra e tutti i componenti"""
        super().__init__()
        
        # Configurazione finestra
        self.title("Speed App")
        self.geometry("400x350")
        self.minsize(400, 350)
        self.maxsize(400, 350)
        self.iconbitmap("icon.ico")
        
        # Configurazione griglia
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1)
        
        # Inizializza i servizi
        self.speedtest_service = SpeedTestService()
        self.animator = DotAnimator(self._on_animation_update)
        
        # Stato dell'applicazione
        self._stop_requested = False
        self._test_completed = False
        
        # Crea i componenti UI
        self._create_widgets()
    
    def _create_widgets(self):
        """Crea tutti i widget dell'interfaccia"""
        # Bottone tema (in alto a destra)
        self.theme_button = ThemeButton(self, initial_theme="dark")
        self.theme_button.grid(row=0, column=1, padx=20, pady=(20, 5), sticky="e")
        
        # Panel risultati
        self.results_panel = ResultsPanel(self)
        
        # Panel controlli
        self.control_panel = ControlPanel(
            self,
            on_start=self._handle_start_test,
            on_stop=self._handle_stop_test,
            on_reset=self._handle_reset_results
        )
    
    def _handle_start_test(self):
        """Gestisce l'avvio del test"""
        # Configura lo stato UI
        self.control_panel.set_testing_state()
        self._stop_requested = False
        self.results_panel.reset()
        
        # Avvia animazione ping
        self.animator.start("ping", self)
        
        # Prepara i callback per il servizio speedtest
        callbacks = {
            'on_ping': self._on_ping_complete,
            'on_download': self._on_download_complete,
            'on_upload': self._on_upload_complete,
            'on_error': self._on_test_error,
            'on_progress_check': lambda: self._stop_requested
        }
        
        # Avvia il test in modo asincrono
        self.speedtest_service.run_test_async(callbacks, self._on_test_complete)
    
    def _handle_stop_test(self):
        """Gestisce l'interruzione del test"""
        self._stop_requested = True
        self._test_completed = False
        self.animator.stop()
        self.results_panel.reset()
        self.control_panel.set_idle_state(enable_reset=False)
    
    def _handle_reset_results(self):
        """Gestisce l'azzeramento dei risultati"""
        self.results_panel.reset()
        self._test_completed = False
        self.control_panel.set_idle_state(enable_reset=False)
    
    def _on_ping_complete(self, ping_value):
        """Callback chiamata quando il ping è completato"""
        self.animator.stop()
        self.results_panel.update_ping(ping_value)
        self.results_panel.update_progress(0.33)
        # Avvia animazione per download
        if not self._stop_requested:
            self.animator.start("download", self)
    
    def _on_download_complete(self, download_value):
        """Callback chiamata quando il download è completato"""
        self.animator.stop()
        self.results_panel.update_download(download_value)
        self.results_panel.update_progress(0.66)
        # Avvia animazione per upload
        if not self._stop_requested:
            self.animator.start("upload", self)
    
    def _on_upload_complete(self, upload_value):
        """Callback chiamata quando l'upload è completato"""
        self.animator.stop()
        self.results_panel.update_upload(upload_value)
        self.results_panel.update_progress(1.0)
        self._test_completed = True
    
    def _on_test_error(self, error):
        """Callback chiamata in caso di errore"""
        self.animator.stop()
        self.results_panel.reset()
        self.results_panel.update_error(f"Errore: {str(error)[:50]}")
        print(f"Errore durante il test: {error}")
        self._test_completed = False
    
    def _on_test_complete(self, success):
        """Callback chiamata al termine del test"""
        self.control_panel.set_idle_state(enable_reset=success and self._test_completed)
    
    def _on_animation_update(self, phase, dots):
        """Callback per aggiornare l'animazione dei pallini"""
        if phase == "ping":
            self.results_panel.update_ping(f"Ping: in corso{dots}")
        elif phase == "download":
            self.results_panel.update_download(f"Download: in corso{dots}")
        elif phase == "upload":
            self.results_panel.update_upload(f"Upload: in corso{dots}")

