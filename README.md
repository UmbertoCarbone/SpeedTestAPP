# Speed App - Test Velocità Internet

Applicazione moderna per testare la velocità della connessione internet con interfaccia grafica.

## 🏗️ Architettura del Progetto

Struttura modulare professionale Python:

```
Connessione_python/
├── main.py                          # Entry point dell'applicazione
├── icon.ico                         # Icona dell'applicazione
├── base.py                          # [DEPRECATO] Versione monolitica originale
│
├── ui/                              # Interfaccia utente
│   ├── __init__.py
│   ├── app_window.py               # Finestra principale (coordina tutti i componenti)
│   │
│   └── widgets/                    # Componenti UI riutilizzabili
│       ├── __init__.py
│       ├── theme_button.py         # Bottone cambio tema (☀️/🌙)
│       ├── results_panel.py        # Panel risultati (ping/download/upload/errori/progress)
│       └── control_panel.py        # Bottoni controllo (avvia/interrompi/azzera)
│
├── services/                       # Business logic
│   ├── __init__.py
│   └── speedtest_service.py       # Servizio per test di velocità
│
└── utils/                          # Utilities
    ├── __init__.py
    └── animations.py               # Animazione pallini (...)
```

## 🎯 Vantaggi della Struttura Modulare

### 1. **Separazione delle Responsabilità**
- **UI** (ui/): Solo interfaccia grafica
- **Business Logic** (services/): Solo logica speedtest
- **Utilities** (utils/): Funzioni riutilizzabili

### 2. **Riusabilità**
I componenti possono essere riutilizzati in altri progetti:
```python
from ui.widgets.theme_button import ThemeButton
from utils.animations import DotAnimator
```

### 3. **Testabilità**
Ogni modulo può essere testato separatamente:
```python
# Test del servizio speedtest
service = SpeedTestService()
service.run_test(callbacks...)

# Test dell'animator
animator = DotAnimator(callback)
animator.start("ping", widget)
```

### 4. **Manutenibilità**
- Vuoi cambiare l'animazione? → Modifica solo `utils/animations.py`
- Vuoi cambiare il servizio speedtest? → Modifica solo `services/speedtest_service.py`
- Vuoi cambiare il tema del bottone? → Modifica solo `ui/widgets/theme_button.py`

## 📦 Moduli Principali

### `main.py`
Entry point dell'applicazione. Configura il tema e avvia l'app.

### `ui/app_window.py`
Finestra principale che:
- Coordina tutti i componenti UI
- Gestisce lo stato dell'applicazione
- Collega UI e business logic tramite callbacks

### `ui/widgets/`
Componenti UI autonomi e riutilizzabili:
- **ThemeButton**: Bottone per cambiare tema
- **ResultsPanel**: Visualizza risultati del test
- **ControlPanel**: Bottoni di controllo (avvia/stop/reset)

### `services/speedtest_service.py`
Servizio che incapsula tutta la logica speedtest:
- Esegue test in modo sincrono o asincrono
- Gestisce callbacks per ogni fase
- Supporta interruzione del test

### `utils/animations.py`
Gestisce l'animazione dei pallini:
- DotAnimator class per animazioni cicliche
- Callback-based per aggiornare l'UI

## 🚀 Come Eseguire

### Sviluppo
```bash
python main.py
```

### Distribuzione
Vedi [BUILD.md](BUILD.md) per creare l'installer professionale.

## 📚 Pattern Utilizzati

### 1. **Callback Pattern**
I componenti comunicano tramite callbacks:
```python
ControlPanel(parent, 
    on_start=self._handle_start,
    on_stop=self._handle_stop,
    on_reset=self._handle_reset
)
```

### 2. **Dependency Injection**
I componenti ricevono le dipendenze nel costruttore:
```python
def __init__(self, parent, on_start, on_stop, on_reset):
    self.on_start = on_start  # Iniettato dall'esterno
```

### 3. **Observer Pattern**
L'animator notifica l'UI tramite callback:
```python
animator = DotAnimator(update_callback)
animator.start("ping", widget)
```

### 4. **Service Layer**
La business logic è separata dall'UI:
```python
speedtest_service = SpeedTestService()
speedtest_service.run_test_async(callbacks, on_complete)
```

## 🎨 Confronto con React

| Python (questo progetto) | React |
|-------------------------|-------|
| `ui/widgets/` | `src/components/` |
| `services/` | `src/services/` |
| `utils/` | `src/utils/` |
| `main.py` | `index.js` |
| `__init__.py` | `index.js` (barrel exports) |
| Callback props | Props & callbacks |
| Class-based components | Function/Class components |

## 🔧 Come Estendere

### Aggiungere un Nuovo Widget
1. Crea file in `ui/widgets/nuovo_widget.py`
2. Implementa la classe
3. Importa in `app_window.py`
4. Usa nel metodo `_create_widgets()`

```python
# ui/widgets/nuovo_widget.py
class NuovoWidget:
    def __init__(self, parent):
        self.button = customtkinter.CTkButton(parent, ...)
    
    def grid(self, **kwargs):
        self.button.grid(**kwargs)
```

### Aggiungere un Nuovo Servizio
1. Crea file in `services/nuovo_service.py`
2. Implementa la logica
3. Importa in `app_window.py`

```python
# services/nuovo_service.py
class NuovoService:
    def do_something(self, callback):
        # Logica...
        callback(result)
```

## 📝 Note

- **`base.py`** è la versione originale monolitica ed è mantenuto per riferimento
- **`main.py`** è il nuovo entry point per la versione modulare
- Tutti i file hanno docstring dettagliate
- Il codice segue le convenzioni PEP 8

## 🛠️ Dipendenze

- `customtkinter` - UI moderna
- `speedtest-cli` - Test velocità
- `threading` - Operazioni asincrone

## 🎓 Cosa Hai Imparato

- ✅ Struttura modulare Python professionale
- ✅ Package e `__init__.py`
- ✅ Separazione UI / Business Logic
- ✅ Pattern callback e dependency injection
- ✅ Organizzazione codice scalabile
- ✅ Documentazione con docstrings

Questa struttura è simile a progetti React/Vue ma adattata alle best practices Python!
