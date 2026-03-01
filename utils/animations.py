"""
Modulo per gestire le animazioni dell'interfaccia.
Fornisce funzionalità per animare i pallini durante i test.
"""

class DotAnimator:
    """Gestisce l'animazione dei pallini (1 -> 2 -> 3 pallini)"""
    
    def __init__(self, update_callback):
        """
        Inizializza l'animatore.
        
        Args:
            update_callback: Funzione da chiamare per aggiornare il testo (riceve fase e dots)
        """
        self.update_callback = update_callback
        self._running = False
        self._dot_count = 0
        self._current_phase = None
        self._after_id = None
        
    def start(self, phase, widget):
        """
        Avvia l'animazione per una fase specifica.
        
        Args:
            phase: Nome della fase (ping, download, upload)
            widget: Widget che gestisce il metodo after()
        """
        # Ferma eventuali animazioni precedenti
        self.stop()
        
        self._current_phase = phase
        self._running = True
        self._dot_count = 0
        self._widget = widget
        self._animate()
        
    def stop(self):
        """Ferma l'animazione"""
        self._running = False
        if self._after_id and hasattr(self, '_widget'):
            try:
                self._widget.after_cancel(self._after_id)
                self._after_id = None
            except:
                pass
        
    def _animate(self):
        """Metodo interno che aggiorna ciclicamente i pallini"""
        if not self._running:
            return
            
        # Incrementa il contatore (da 1 a 3, poi ricomincia)
        self._dot_count = (self._dot_count % 3) + 1
        # Crea la stringa dei pallini
        dots = "." * self._dot_count
        
        # Chiama il callback per aggiornare l'UI
        self.update_callback(self._current_phase, dots)
        
        # Richiama dopo 500ms
        self._after_id = self._widget.after(500, self._animate)
