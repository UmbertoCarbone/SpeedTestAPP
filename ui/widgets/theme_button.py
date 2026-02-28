"""
Widget per il bottone di cambio tema (dark/light mode).
"""

import customtkinter

class ThemeButton:
    """Bottone per cambiare tra modalità scura e chiara"""
    
    def __init__(self, parent, initial_theme="dark"):
        """
        Crea il bottone tema.
        
        Args:
            parent: Widget padre
            initial_theme: Tema iniziale ("dark" o "light")
        """
        self.current_theme = initial_theme
        
        # Crea il bottone
        self.button = customtkinter.CTkButton(
            parent,
            text="☀️" if initial_theme == "dark" else "🌙",
            command=self._toggle_theme,
            width=35,
            height=35,
            font=("Segoe UI Emoji", 18),
            corner_radius=8
        )
    
    def grid(self, **kwargs):
        """Posiziona il bottone nella griglia"""
        self.button.grid(**kwargs)
    
    def _toggle_theme(self):
        """Cambia il tema tra scuro e chiaro"""
        if self.current_theme == "dark":
            customtkinter.set_appearance_mode("light")
            self.current_theme = "light"
            self.button.configure(text="🌙")
        else:
            customtkinter.set_appearance_mode("dark")
            self.current_theme = "dark"
            self.button.configure(text="☀️")
