from IPython.display import display, HTML, clear_output
from IPython import get_ipython
from ipywidgets import widgets
from pathlib import Path
import os

home = Path.home()
src = home / '.gutris1'
css_multi = src / 'multi.css'
mark = src / 'marking.py'
img = src / 'loading.png'

A1111 = src / 'A1111.py'
Forge = src / 'Forge.py'
ComfyUI = src / 'ComfyUI.py'

os.chdir(home)
src.mkdir(parents=True, exist_ok=True)

x = [
    f"curl -sLo {css} https://github.com/gutris1/segsmaker/raw/main/script/multi/multi.css",
    f"curl -sLo {img} https://github.com/gutris1/segsmaker/raw/main/script/loading.png",
    f"curl -sLo {mark} https://github.com/gutris1/segsmaker/raw/main/script/multi/marking.py",
    f"curl -sLo {A1111} https://github.com/gutris1/segsmaker/raw/main/script/multi/A1111.py",
    f"curl -sLo {Forge} https://github.com/gutris1/segsmaker/raw/main/script/multi/Forge.py",
    f"curl -sLo {ComfyUI} https://github.com/gutris1/segsmaker/raw/main/script/multi/ComfyUI.py"]
    
for y in x:
    get_ipython().system(y)

def load_css(css_multi):
    with open(css_multi, "r") as file:
        data = file.read()

    display(HTML(f"<style>{data}</style>"))

def selection(btn):
    multi_panel.close()
    clear_output()

    with output:
        if btn == 'A1111':
            get_ipython().run_line_magic('run', f'{A1111}')

        elif btn == 'Forge':
            get_ipython().run_line_magic('run', f'{Forge}')

        elif btn == 'ComfyUI':
            get_ipython().run_line_magic('run', f'{ComfyUI}')

options = ['A1111', 'Forge', 'ComfyUI']
buttons = []

for btn in options:
    button = widgets.Button(description='')
    button.add_class(btn.lower())
    button.on_click(lambda x, btn=btn: selection(btn))
    buttons.append(button)

output = widgets.Output()

multi_panel = widgets.HBox(
    buttons, layout=widgets.Layout(
        width='600px',
        height='380px'))
multi_panel.add_class('multi-panel')

load_css(css_multi)
display(multi_panel, output)
