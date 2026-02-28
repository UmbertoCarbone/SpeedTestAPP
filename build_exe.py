# Speed App - Build Script
# Genera l'eseguibile .exe dall'applicazione Python

"""
Script per creare l'eseguibile Windows dell'applicazione Speed App.
Usa PyInstaller per convertire il codice Python in un .exe standalone.
"""

import subprocess
import sys
import os

def install_pyinstaller():
    """Installa PyInstaller se non è presente"""
    print("📦 Verifica PyInstaller...")
    try:
        import PyInstaller
        print("✅ PyInstaller già installato")
    except ImportError:
        print("⬇️ Installazione PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        print("✅ PyInstaller installato")

def create_exe():
    """Crea l'eseguibile con PyInstaller"""
    print("\n🔨 Creazione eseguibile...")
    
    # Parametri PyInstaller
    args = [
        sys.executable,                       # Python
        "-m", "PyInstaller",                  # Usa PyInstaller come modulo
        "--name=SpeedApp",                    # Nome dell'exe
        "--onefile",                          # Singolo file exe
        "--windowed",                         # Nessuna console
        "--icon=icon.ico",                    # Icona
        "--add-data=icon.ico;.",             # Includi icon.ico
        "--hidden-import=ui.widgets.theme_button",
        "--hidden-import=ui.widgets.results_panel",
        "--hidden-import=ui.widgets.control_panel",
        "--hidden-import=services.speedtest_service",
        "--hidden-import=utils.animations",
        "main.py"
    ]
    
    # Esegui PyInstaller
    result = subprocess.run(args)
    
    if result.returncode == 0:
        print("\n✅ Eseguibile creato con successo!")
        print("📁 Percorso: dist/SpeedApp.exe")
        print("\n💡 Puoi testarlo eseguendo: .\\dist\\SpeedApp.exe")
        return True
    else:
        print("\n❌ Errore durante la creazione dell'eseguibile")
        return False

def cleanup():
    """Pulisce file temporanei"""
    print("\n🧹 Pulizia file temporanei...")
    import shutil
    
    # Rimuovi cartelle temporanee
    for folder in ["build", "__pycache__"]:
        if os.path.exists(folder):
            shutil.rmtree(folder)
            print(f"  Rimosso: {folder}/")
    
    # Rimuovi .spec file
    if os.path.exists("SpeedApp.spec"):
        os.remove("SpeedApp.spec")
        print("  Rimosso: SpeedApp.spec")

def main():
    """Funzione principale"""
    print("=" * 60)
    print("🚀 BUILD SPEED APP")
    print("=" * 60)
    
    # Step 1: Installa PyInstaller
    install_pyinstaller()
    
    # Step 2: Crea exe
    success = create_exe()
    
    # Step 3: Pulizia (opzionale)
    if success:
        cleanup_choice = input("\n🧹 Vuoi pulire i file temporanei? (s/n): ")
        if cleanup_choice.lower() == 's':
            cleanup()
    
    print("\n" + "=" * 60)
    if success:
        print("✅ BUILD COMPLETATO CON SUCCESSO!")
        print("\n📦 File generato: dist/SpeedApp.exe")
        print("💡 Prossimo step: crea l'installer con Inno Setup")
    else:
        print("❌ BUILD FALLITO")
    print("=" * 60)

if __name__ == "__main__":
    main()
