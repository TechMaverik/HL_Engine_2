"""network_tool_sample.py"""
from HL_Engine_2 import HL_Engine_Network_Processing

class Network:
    """Network Sample  Class"""
    ip="192.168.1."

    def __init__(self):
        self.processor=HL_Engine_Network_Processing.NetworkProcessEngine()

    def network_scanner_tool(self):
        self.processor.scan_wifi(self.ip)

tool=Network()
tool.network_scanner_tool()


