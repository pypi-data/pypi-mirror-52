import os


def install():
    os.system('ls')
    os.system('pwd')
    path = os.getcwd()
    os.system(f'chmod +x {path}/scripts/install.sh')
    os.system(f'sh {path}/scripts/install.sh')


def update():
    # os.system('chmod +x ./mlops_propulsion_academy/scripts/update.sh')
    # os.system('sh ./mlops_propulsion_academy/scripts/update.sh')
    pass


def start():
    path = os.getcwd()
    os.system(f'chmod +x {path}/scripts/start.sh')
    os.system(f'sh {path}/scripts/start.sh')
