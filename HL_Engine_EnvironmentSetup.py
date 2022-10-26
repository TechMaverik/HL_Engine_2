"""
HL_Engine_EnvironmentSetup.py
Author:Akhil P Jacob
HLDynamic-Integrations
"""
import subprocess
import sys
import time
from xml.dom import minidom
from HL_Constants import *


class EnvironmentalSetup:
    """Environmental Setup Class"""

    def setup_libraries(self):
        """Run setup for installing dependencies"""

        mydoc = minidom.parse(PAYLOAD_XML_PATH)
        payload = mydoc.getElementsByTagName(PAYLOAD)
        xfile = open(LOG_REPORT, "w")
        xfile.write("")
        xfile.close()
        for elem in payload:
            print(elem.firstChild.data)
            package = str(elem.firstChild.data)
            try:
                print(COMMENCING_INSTALLATION)
                subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            except:
                print(INSTALLATION_FAILED)
                xfile = open(LOG_REPORT, "a")
                xfile.write(package)
                xfile.close()
