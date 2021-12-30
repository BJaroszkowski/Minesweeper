# Minesweeper

Nostalgia driven projects of recreating the old version of Minesweeper as closely as possible (at least in terms of functionality) in PyGame.

![](https://bjaroszkowski.github.io/img/saper.png)

Can be run directly by executing

```
python3 -m venv venv
. venv/bin/activate (or equivalent based on OS)
python -m pip install -r requirements.txt
python source_code/main.py
```

One can also generate binary by

```
python -m pip install pyinstaller
pyinstaller source_code/final.spec
```

Given that path to source_code folder was set correctly in final.spec file the
binary (called `minesweeper`) should be available in `dist` folder.
