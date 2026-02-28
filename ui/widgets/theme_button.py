"""
Widget per il bottone di cambio tema (dark/light mode).
"""

import customtkinter


class ThemeButton:
    def __init__(self, parent, initial_theme="dark"):
        """
        Crea il bottone tema.

        Args:
            parent: Widget padre
            initial_theme: Tema iniziale ("dark" o "light")
        """
        self.current_theme = initial_theme
        self.button = customtkinter.CTkButton(
            parent,
            text="☀️" if initial_theme == "dark" else "🌙",
            fg_color="#232323" if initial_theme == "dark" else "#EBEBEB",  # Sfondo identico alla finestra
            hover_color="#232323" if initial_theme == "dark" else "#EBEBEB", # Nessun effetto hover
            border_width=0,  # Nessun bordo
            text_color="#FFD600" if initial_theme == "dark" else "#00BFFF",
            command=self._toggle_theme,
            width=35,
            height=35,
            font=("Segoe UI Emoji", 18),
            corner_radius=8,
        )

    def grid(self, **kwargs):
        """Posiziona il bottone nella griglia"""
        self.button.grid(**kwargs)

    def _toggle_theme(self):
        """Cambia il tema tra scuro e chiaro, aggiorna colore e emoji"""
        if self.current_theme == "dark":
            customtkinter.set_appearance_mode("light")
            self.current_theme = "light"
            self.button.configure(
                text="🌙",
                fg_color="#EBEBEB",
                hover_color="#EBEBEB",
                border_width=0,
                text_color="#488BA1",  # luna celeste
            )
        else:
            customtkinter.set_appearance_mode("dark")
            self.current_theme = "dark"
            self.button.configure(
                text="☀️",
                fg_color="#232323",
                hover_color="#232323",
                border_width=0,
                text_color="#FFD600",  # sole giallo
            )

    def set_enabled(self, enabled: bool):
        """Abilita o disabilita il bottone tema"""
        state = "normal" if enabled else "disabled"
        self.button.configure(state=state)
