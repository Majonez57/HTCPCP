from email import header
from encodings import utf_8
import io
import re
from socket import socket

htcpcpResponseStartLineRegex = re.compile("(?<method>\\w+) (?<uri>[\\/A-Z]+) (?<protocol>\\w+)\\/(?<version>\\d+(\\.\\d+)?)")
htcpcpHeaderRegex = re.compile("(?<key>[A-Z\\-]+): (?<value>.+)")

class htcpcpResponse():

    def __init__(self) -> None:
        pass

class HtcpcpRequest():

    headers = dict();

    def __init__(self, socket : socket):
        stringData = str(socket, utf_8)

        dataLines = stringData.split("\n")
        self._setStartLine(dataLines.pop(0))
        while ((header := dataLines.pop(0)) != ""):
            self._setHeader(header)
        
        contentLength = self.headers.get("content-length", 0)
        this.body = 
        
    def _setStartLine(self, firstLine : str):
        flMatch = htcpcpResponseStartLineRegex.match(firstLine)
        matches = flMatch.groupdict()
        self.method = matches["method"]
        self.uri = matches["uri"]
        self.protocol = matches["protocol"]
        self.version = matches["version"]
    
    def _setHeader(self, header : str):
        headerMatch = htcpcpHeaderRegex.match(header)
        matches = headerMatch.groupdict()
        self.headers[matches["key"].lower()] = matches["value"]
            