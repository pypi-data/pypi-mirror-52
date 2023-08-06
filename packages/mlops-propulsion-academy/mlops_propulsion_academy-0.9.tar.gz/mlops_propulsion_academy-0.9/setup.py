from setuptools import setup

setup(name='mlops_propulsion_academy',
      version='0.9',
      description='mlops_propulsion_academy',
      author='Daniele Roncaglioni',
      author_email='danieler@propulsionacademy.com',
      license='MIT',
      packages=['mlops_propulsion_academy'],
      zip_safe=False,
      scripts=['bin/mlops_scripts', 'bin/start.sh', 'bin/install.sh',  'bin/update.sh'],
      # entry_points={
      #     'console_scripts': ['mlops_install=mlops_propulsion_academy.command_line:install',
      #                         'mlops_update=mlops_propulsion_academy.command_line:update',
      #                         'mlops_start=mlops_propulsion_academy.command_line:start'],
      # }
      )
