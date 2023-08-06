# Seperator

# Installation

for create virtualenv
```bash
python3 -m venv seperator_env
# according to used shell one of them
# source seperator_env/bin/activate.sh
# source seperator_env/bin/activate.csh
# source seperator_env/bin/activate.fish
```
for install it

```bash
pip install seperator
```



### Usage Samples:

```python3
from seperator.lines import line,dateline

line()
line("Hello World")
line("Hello World",width=80)
line("Hello World",char='*')
line("Hello World",color='red')
line("Hello World",align=5)
line("Hello World",align=-5)
line("Hello World",margin=(5,5))



# you cannot additional
# info but other parameters are same with line
dateline()
```
```bash
────────────────────────────────────────────────────────────────────────────────
─ Hello World ──────────────────────────────────────────────────────────────────
─ Hello World ────────────────────────────────────
* Hello World ******************************************************************
─ Hello World ──────────────────────────────────────────────────────────────────
───── Hello World ──────────────────────────────────────────────────────────────
────────────────────────────────────────────────────────────── Hello World ─────
─     Hello World     ──────────────────────────────────────────────────────────
─ 08 Sep 2019 10:35:04 ───────────────────────────────────────────────────────'
```
