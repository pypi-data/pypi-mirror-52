import os


def install():
    os.system('chmod +x ./mlops_propulsion_academy/scripts/install.sh')
    os.system('sh ./mlops_propulsion_academy/scripts/install.sh')


def update():
    # os.system('chmod +x ./mlops_propulsion_academy/scripts/update.sh')
    # os.system('sh ./mlops_propulsion_academy/scripts/update.sh')
    pass


def start():
    print('Starting')
    os.system('chmod +x ./mlops_propulsion_academy/scripts/start.sh')
    os.system('sh ./mlops_propulsion_academy/scripts/start.sh')
