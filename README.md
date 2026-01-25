# hello-world

the standard way of starting - hello, World!
Hi everyone!
This is just another text file. We have all been excactly here - getting our feets wet in a new domain.

## Poker screenshot (macOS)

Nedenfor er to versioner, der tager **kun det aktive vindue** og gemmer PNG i `~/Desktop/poker_screenshots`.

### Version 1: Filnavn fra dialog

**Hvorfor denne løsning?**
- Kræver ingen ekstra installationer.
- Bruger macOS’ indbyggede værktøjer.

**Kørsel**
```bash
./scripts/poker_screenshot_v1.sh
```

Du bliver bedt om at indtaste spillerens navn. Filen bliver gemt som:
`<navn>_YYYYMMDD_HHMMSS.png`.

### Version 2: Filnavn fra OCR (automatisk)

**Hvorfor denne løsning?**
- Finder spillerens navn automatisk ud fra teksten i vinduet.
- Bruger OCR på to steder (spillerlisten i højre side og navnet nederst).

**Engangsinstallation (simple termer)**
1. Installér Homebrew (hvis du ikke allerede har det): https://brew.sh
2. Installér OCR-motoren Tesseract:
   ```bash
   brew install tesseract
   ```
3. Installér Python-biblioteker:
   ```bash
   python3 -m pip install pillow pytesseract
   ```

**Kørsel**
```bash
./scripts/poker_screenshot_v2.py
```

**Justering af OCR-områder**
Skærmen kan være lidt forskellig i størrelse/zoom. Hvis navnet ikke findes korrekt:
- Kør med `--debug-crops` for at gemme de udklip, der OCR-scannes.
- Justér procent-områderne i scriptet (`player_list_box` og `legend_box`).

```bash
./scripts/poker_screenshot_v2.py --debug-crops
```

## Overvejelser (ikke-teknisk sprog)

- **Sprogvalg**: Vi bruger macOS’ indbyggede funktioner, fordi de allerede findes på en Mac og er stabile.
- **Stabilitet**: Version 1 er mest robust, fordi den kun spørger dig om navnet.
- **Automatik**: Version 2 kan spare tid, men kræver at vi rammer det rigtige område i billedet.
- **Identifikation af navn**: Vi kigger to steder i billedet, hvor navnet typisk står. Det øger chancen for at finde det rigtige.
- **Justering**: Hvis layoutet ændrer sig (fx nyt tema), kan vi nemt rette de to “områder”, vi aflæser.
