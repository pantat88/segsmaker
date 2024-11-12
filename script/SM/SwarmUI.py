from IPython.display import display, HTML, clear_output, Image
from ipywidgets import widgets
from IPython import get_ipython
from pathlib import Path
import subprocess, time, os, shlex, json, shutil, sys
from nenen88 import say, download, tempe


repo = f"git clone https://github.com/mcmonkeyprojects/SwarmUI"

HOME = Path.home()
SRC = HOME / '.gutris1'
CSS = SRC / 'setup.css'
IMG = SRC / 'loading.png'
MARK = SRC / 'marking.py'
STP = HOME / '.conda/setup.py'

tmp = Path('/tmp')
vnv = tmp / 'venv'
WEBUI = HOME / 'SwarmUI'
MODELS = WEBUI / 'Models'


def load_css():
    with open(CSS, "r") as f:
        d = f.read()
    display(HTML(f"<style>{d}</style>"))


def tmp_cleaning():
    for item in tmp.iterdir():
        if item.is_dir() and item != vnv:
            shutil.rmtree(item)
        elif item.is_file() and item != vnv:
            item.unlink()


def req_list():
    return [
        f"rm -rf {HOME}/tmp {HOME}/.cache/*",
        f"rm -rf {MODELS}/Stable-Diffusion/tmp_ckpt",
        f"rm -rf {MODELS}/Lora/tmp_lora {MODELS}/controlnet {MODELS}/clip",
        f"ln -vs /tmp {HOME}/tmp",
        f"ln -vs /tmp/ckpt {MODELS}/Stable-Diffusion/tmp_ckpt",
        f"ln -vs /tmp/lora {MODELS}/Lora/tmp_lora",
        f"ln -vs /tmp/controlnet {MODELS}/controlnet",
        f"ln -vs /tmp/clip {MODELS}/clip"
    ]


def webui_req():
    time.sleep(1)
    tmp_cleaning()
    os.chdir(WEBUI)

    MODELS.mkdir(parents=True, exist_ok=True)

    dirs = ['Stable-Diffusion', 'Lora', 'Embeddings', 'VAE', 'upscale_models']
    for sub in dirs:
        (MODELS / sub).mkdir(parents=True, exist_ok=True)

    req = req_list()
    for lines in req:
        subprocess.run(shlex.split(lines), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    scripts = [
        f"https://github.com/gutris1/segsmaker/raw/main/script/SM/controlnet.py {WEBUI}/asd",
        f"https://github.com/gutris1/segsmaker/raw/main/script/SM/venv.py {WEBUI}",
        f"https://github.com/gutris1/segsmaker/raw/main/script/SM/Launcher.py {WEBUI}",
        f"https://github.com/gutris1/segsmaker/raw/main/script/SM/segsmaker.py {WEBUI}",
        f"https://dot.net/v1/dotnet-install.sh {WEBUI}"
    ]

    upscalers = [
        f"https://huggingface.co/pantat88/ui/resolve/main/4x-UltraSharp.pth {MODELS}/upscale_models",
        f"https://huggingface.co/pantat88/ui/resolve/main/4x-AnimeSharp.pth {MODELS}/upscale_models",
        f"https://huggingface.co/pantat88/ui/resolve/main/4x_NMKD-Superscale-SP_178000_G.pth {MODELS}/upscale_models",
        f"https://huggingface.co/pantat88/ui/resolve/main/4x_RealisticRescaler_100000_G.pth {MODELS}/upscale_models",
        f"https://huggingface.co/pantat88/ui/resolve/main/8x_RealESRGAN.pth {MODELS}/upscale_models",
        f"https://huggingface.co/pantat88/ui/resolve/main/4x_foolhardy_Remacri.pth {MODELS}/upscale_models"]

    line = scripts + upscalers
    for item in line:
        download(item)

    dotnet = WEBUI / 'dotnet-install.sh'
    dotnet.chmod(0o755)

    netdot = "bash ./dotnet-install.sh --channel 8.0"
    subprocess.run(shlex.split(netdot), stdout=sys.stdout, stderr=sys.stdout, check=True)

    tempe()


def sd_15():
    webui_req()

    extras = [
        f"https://huggingface.co/pantat88/ui/resolve/main/embeddings.zip {MODELS}",
        f"https://huggingface.co/stabilityai/sd-vae-ft-mse-original/resolve/main/vae-ft-mse-840000-ema-pruned.safetensors {MODELS}/VAE"]

    for items in extras:
        download(items)

    get_ipython().system(f"unzip -qo {MODELS}/embeddings.zip -d {MODELS}/Embeddings")
    get_ipython().system(f"rm {MODELS}/embeddings.zip")


def sd_xl():
    webui_req()

    extras = [
        f"https://civitai.com/api/download/models/403492 {MODELS}/Embeddings",
        f"https://civitai.com/api/download/models/182974 {MODELS}/Embeddings",
        f"https://civitai.com/api/download/models/159385 {MODELS}/Embeddings",
        f"https://civitai.com/api/download/models/159184 {MODELS}/Embeddings",
        f"https://huggingface.co/stabilityai/sdxl-vae/resolve/main/sdxl_vae.safetensors {MODELS}/VAE"
    ]

    for items in extras:
        download(items)


def marking(path, fn, ui):
    txt = path / fn
    values = {
        'ui': ui,
        'launch_args': '',
        'zrok_token': '',
        'ngrok_token': '',
        'tunnel': ''
    }

    if not txt.exists():
        with open(txt, 'w') as file:
            json.dump(values, file, indent=4)

    with open(txt, 'r') as file:
        data = json.load(file)

    data.update({
        'ui': ui,
        'launch_args': '',
        'tunnel': ''
    })

    with open(txt, 'w') as file:
        json.dump(data, file, indent=4)


def webui_install(b):
    panel.close()
    clear_output()
    os.chdir(HOME)

    with loading:
        display(Image(filename=str(IMG)))

    with webui_setup:
        say(f"<b>【{{red}} Installing {WEBUI.name}{{d}} 】{{red}}</b>")
        get_ipython().system(f"{repo}")

        marking(SRC, 'marking.json', WEBUI.name)

        if b == 'button-15':
            sd_15()
        elif b == 'button-xl':
            sd_xl()

        get_ipython().run_line_magic('run', f'{MARK}')

        with loading:
            loading.clear_output(wait=True)
            get_ipython().run_line_magic('run', f'{WEBUI}/venv.py')

            os.chdir(HOME)
            loading.clear_output(wait=True)
            say("<b>【{red} Done{d} 】{red}</b>")


def go_back(b):
    panel.close()
    clear_output()

    with webui_setup:
        get_ipython().run_line_magic('run', f'{STP}')


loading = widgets.Output()
webui_setup = widgets.Output()

options = ['button-15', 'button-back', 'button-xl']
buttons = []

for btn in options:
    button = widgets.Button(description='')
    button.add_class(btn.lower())
    if btn == 'button-back':
        button.on_click(lambda x: go_back(btn))
    else:
        button.on_click(lambda x, btn=btn: webui_install(btn))
    buttons.append(button)

panel = widgets.HBox(
    buttons, layout=widgets.Layout(
        width='450px',
        height='250px'))

panel.add_class("multi-panel")


def check_webui(ui_name, path, mark):
    if path.exists():
        print(f'{ui_name} is installed, Uninstall first.')
        get_ipython().run_line_magic('run', f'{mark}')
        return True
    return False


def webui_widgets():
    if WEBUI.exists():
        git_dir = WEBUI / '.git'
        if git_dir.exists():
            os.chdir(WEBUI)
            commit_hash = os.popen('git rev-parse HEAD').read().strip()

            get_ipython().system("git pull origin master")
            get_ipython().system("git fetch --tags")

        x = [
            f"https://github.com/gutris1/segsmaker/raw/main/script/SM/controlnet.py {WEBUI}/asd",
            f"https://github.com/gutris1/segsmaker/raw/main/script/SM/venv.py {WEBUI}",
            f"https://github.com/gutris1/segsmaker/raw/main/script/SM/Launcher.py {WEBUI}",
            f"https://github.com/gutris1/segsmaker/raw/main/script/SM/segsmaker.py {WEBUI}"
        ]

        for y in x:
            download(y)

    else:
        webui_list = [
            ('A1111', HOME / 'A1111'),
            ('Forge', HOME / 'Forge'),
            ('ComfyUI', HOME / 'ComfyUI'),
            ('ReForge', HOME / 'ReForge'),
            ('FaceFusion', HOME / 'FaceFusion'),
            ('SDTrainer', HOME / 'SDTrainer')
        ]
        
        for ui_name, path in webui_list:
            if check_webui(ui_name, path, MARK):
                return

        load_css()
        display(panel, webui_setup, loading)


webui_widgets()
