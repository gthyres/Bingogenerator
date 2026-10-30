# Bingogenerator 

1) "Bingogenerator.exe" - allt Du behöver i windows.
2) "Bingo portable på plats.zip" - packa upp och kör .bat-fil för att skapa en portabel .exe-fil. Kräver python på datorn
3) "bingoPy oGUI.zip" - packa upp och installera i Windows fån en .batfil, Kräver pyton på datorn.
4) "bingo_generator.py"- körs i python
5) "index.html" - kör via webben                   

Grafiskt program som skapar bingospelplaner som PDF (6 spelplaner per liggande A4,
9 x 3 rutor, varje siffra 1-90 exakt en gång per A4).

## Portabel version för USB-minne (ingen installation)

1. Bygg `Bingogenerator.exe` med `build_portable.bat` (kräver Python på byggdatorn), eller ladda ner
   artefakten `Bingogenerator_Portable` från GitHub Actions (se nedan).
2. Kopiera `Bingogenerator.exe` till USB-minnet.
3. Dubbelklicka på den på vilken Windows-dator som helst – inget Python eller installation behövs.
   PDF-filer sparas som standard bredvid programmet på USB-minnet.

**Välja var filen hamnar:** `build_portable.bat` (eller GitHub-artefakten `Bingogenerator_Portable_Setup`)
skapar även `Bingogenerator_Portable_Setup.exe`. Kör den, klicka *Bläddra…* och välj valfri mapp, t.ex.
USB-minnet (`E:\Bingogenerator`) eller en OneDrive-mapp. Den packar bara upp `Bingogenerator.exe` dit –
inga genvägar, inga registerposter och ingen avinstallerare (ta bort mappen för att avinstallera).

Obs: första starten kan ta några sekunder (filen packar upp sig själv), och Windows SmartScreen
kan varna för ett okänt program – välj *Mer info* > *Kör ändå*.

## Filer

| Fil | Syfte |
|---|---|
| `bingo_core.py` | Generatorlogiken (från din ursprungliga `bingo_generator.py`) |
| `bingo_gui.py` | Grafiskt gränssnitt (Tkinter) |
| `build_portable.bat` | Bygger en enda portabel `.exe` för USB-minne |
| `build_windows.bat` | Bygger `.exe` med PyInstaller och installationsprogram med Inno Setup |
| `installer.iss` | Inno Setup-skript |
| `.github/workflows/build.yml` | Bygger installationsprogrammet automatiskt på GitHub (om du inte vill installera något själv) |

## Bygga installationsprogrammet (Windows)

Slutanvändaren behöver **inte** Python. Python behövs bara på den dator där du bygger.

**Alternativ A – på din egen Windows-dator**
1. Installera Python 3.10+ (https://python.org) och Inno Setup 6 (https://jrsoftware.org/isinfo.php).
2. Dubbelklicka `build_windows.bat` i den här mappen.
3. Färdigt installationsprogram: `installer_output\Bingogenerator_Setup.exe`

**Alternativ B – via GitHub (inget behöver installeras lokalt)**
1. Lägg mappen i ett GitHub-repo.
2. Öppna fliken *Actions* > *Build Windows installer* > *Run workflow*.
3. Ladda ner `Bingogenerator_Setup` under *Artifacts*.

Installationsprogrammet installerar för den aktuella användaren (ingen administratör krävs),
skapar Startmenygenväg och valfri skrivbordsgenväg samt avinstallerare.

## Köra utan att bygga
```
pip install reportlab
python bingo_gui.py
