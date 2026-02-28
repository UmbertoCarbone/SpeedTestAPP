"""
Panel per i bottoni di controllo (avvia, interrompi, azzera).
"""

import customtkinter

class ControlPanel:
    """Panel che contiene i bottoni di controllo del test"""
    
    def __init__(self, parent, on_start, on_stop, on_reset):
        """
        Crea il panel di controllo.
        
        Args:
            parent: Widget padre
            on_start: Callback per l'avvio del test
            on_stop: Callback per l'interruzione del test
            on_reset: Callback per l'azzeramento dei risultati
        """
        self.on_start = on_start
        self.on_stop = on_stop
        self.on_reset = on_reset
        
        # Bottone "Avvia Speedtest" (verde)
        self.start_button = customtkinter.CTkButton(
            parent,
            text="Avvia Speedtest",
            command=self._handle_start,
            width=160,
            height=40,
            fg_color="green",
            hover_color="green"
        )
        self.start_button.grid(row=5, column=0, padx=(20, 5), pady=(20, 5), sticky="ew")
        
        # Bottone "Interrompi test" (rosso, inizialmente disabilitato)
        self.stop_button = customtkinter.CTkButton(
            parent,
            text="Interrompi test",
            command=self._handle_stop,
            width=160,
            height=40,
            fg_color="red",
            hover_color="red",
            state="disabled"
        )
        self.stop_button.grid(row=5, column=1, padx=(5, 20), pady=(20, 5), sticky="ew")
        
        # Bottone "Azzera risultati" (inizialmente disabilitato)
        self.reset_button = customtkinter.CTkButton(
            parent,
            text="Azzera risultati",
            command=self._handle_reset,
            width=340,
            height=40,
            state="disabled"
        )
        self.reset_button.grid(row=6, column=0, columnspan=2, padx=20, pady=(5, 20), sticky="ew")
    
    def _handle_start(self):
        """Gestisce il click su Avvia"""
        self.on_start()
    
    def _handle_stop(self):
        """Gestisce il click su Interrompi"""
        self.on_stop()
    
    def _handle_reset(self):
        """Gestisce il click su Azzera"""
        self.on_reset()
    
    def set_testing_state(self):
        """Configura lo stato dei bottoni durante il test"""
        self.start_button.configure(state="disabled")
        self.stop_button.configure(state="normal")
        self.reset_button.configure(state="disabled")
    
    def set_idle_state(self, enable_reset=False):
        """Configura lo stato dei bottoni quando non c'è test in corso"""
        self.start_button.configure(state="normal")
        self.stop_button.configure(state="disabled")
        if enable_reset:
            self.reset_button.configure(state="normal")
        else:
            self.reset_button.configure(state="disabled")
