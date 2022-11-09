"""setup.py"""
from HL_Engine_EnvironmentSetup import *
from HL_CommonDependency import *

display_message(WELCOME_MSG)
installer = EnvironmentalSetup()
installer.setup_libraries()
display_message(INSTALLATION_COMPLETED)
