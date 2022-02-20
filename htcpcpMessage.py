from email import header
from encodings import utf_8
import io
import re
from socket import socket
from typing import TextIO

version = "1.0"
htcpcpRequestStartLineRegex = re.compile("(?P<method>\\w+) (?P<uri>[\\/A-Za-z0-9:\\.\\-_~?#%]+) HTCPCP\\/(?P<version>\\d+(\\.\\d+)?)", re.IGNORECASE)
htcpcpResponseStartLineRegex = re.compile("HTCPCP\\/(?P<version>\\d+(\\.\\d+)?) (?P<status>\\d+) (?P<message>.*)", re.IGNORECASE)
htcpcpHeaderRegex = re.compile("(?P<key>[A-Z\\-]+): (?P<value>.+)", re.IGNORECASE)
coffeeSchemes = {
    "koffie": ["Afrikaans", "Dutch"],
    "q%C3%A6hv%C3%A6": ["Azerbaijani"],
    "%D9%82%D9%87%D9%88%D8%A9": ["Arabic"],
    "akeita": ["Basque"],
    "koffee": ["Bengali"],
    "kahva": ["Bosnian"],
    "kafe": ["Bulgarian", "Czech"],
    "caf%C3%E8": ["Catalan", "French", "Galician"],
    "%E5%92%96%E5%95%A1": ["Chinese"],
    "kava": ["Croatian"],
    "k%C3%A1va": ["Czech"],
    "kaffe": ["Danish", "Norwegian", "Swedish"],
    "coffee": ["English"],
    "kafo": ["Esperanto"],
    "kohv": ["Estonian"],
    "kahvi": ["Finnish"],
    "%4Baffee": ["German"],
    "%CE%BA%CE%B1%CF%86%CE%AD": ["Greek"],
    "%E0%A4%95%E0%A5%8C%E0%A4%AB%E0%A5%80": ["Hindi"],
    "%E3%82%B3%E3%83%BC%E3%83%92%E3%83%BC": ["Japanese"],
    "%EC%BB%A4%ED%94%BC": ["Korean"],
    "%D0%BA%D0%BE%D1%84%D0%B5": ["Russian"],
    "%E0%B8%81%E0%B8%B2%E0%B9%81%E0%B8%9F": ["Thai"]
}
reverseCoffeeSchemes = dict()

for key, values in coffeeSchemes.items():
    for value in values:
        reverseCoffeeSchemes[value] = key;

class HtcpcpResponse():

    status = None
    messsage = None
    body = None
    headers = dict()

    def fromFile(raw_req : TextIO):
        x = HtcpcpResponse()
        x._setStartLine(raw_req.readline())
        while ((header := raw_req.readline()) not in ["", "\n"]):
            x._setHeader(header)
        
        contentLength = x.headers.get("content-length", 0)
        x.body = raw_req.read(int(contentLength))

        return x
    
    def create(self):
        if(not self._isValid()):
            raise Exception("HTCPCP Response is invalid")
        out = "HTCPCP/{} {} {}\n".format(version, self.status, self.message)
        if(self.body):
            self.headers["content-length"] = len(self.body)
        out += "".join(["{}: {}\n".format(key, value) for key, value in self.headers.items()]) + "\n"
        if(self.body):
            out += "\n" + self.body
        return out

    def toString():
        pass
        
    def _setStartLine(self, firstLine : str):
        flMatch = htcpcpResponseStartLineRegex.match(firstLine)
        matches = flMatch.groupdict()
        self.status = matches["status"]
        self.message = matches["message"]
    
    def _setHeader(self, header : str):
        headerMatch = htcpcpHeaderRegex.match(header)
        matches = headerMatch.groupdict()
        self.headers[matches["key"].lower()] = matches["value"]

    def _isValid(self):
        return self.status and self.message

class HtcpcpRequest():

    headers = dict()
    body = None

    def fromFile(raw_req : TextIO):
        x = HtcpcpRequest()
        x._setStartLine(raw_req.readline())
        while ((header := raw_req.readline()) not in ["", "\n"]):
            x._setHeader(header)
        
        contentLength = x.headers.get("content-length", 0)
        x.body = raw_req.read(int(contentLength))

        return x

    def setUri(self, language : str, host: str, /, pot : int = None, additions : int = None):
        self.uri = "{}://{}".format(reverseCoffeeSchemes[language], host)
        if(pot):
            coffeeUri += "/pot-{}".format(pot)
        if(additions):
            coffeeUri += "?{}".format(additions)
    
    def create(self):
        if(not self._isValid()):
            raise Exception("HTCPCP Request is invalid")
        out = "{} {} HTCPCP/{}".format(self.method, self.uri, version)
        if(self.body):
            self.headers["content-length"] = len(self.body)
        out += "".join(["\n{}: {}".format(key, value) for key, value in self.headers.items()]) + "\n"
        if(self.body):
            out += "\n" + self.body

        return out
        
    def _setStartLine(self, firstLine : str):
        flMatch = htcpcpRequestStartLineRegex.match(firstLine)
        matches = flMatch.groupdict()
        self.method = matches["method"]
        self.uri = matches["uri"]
    
    def _setHeader(self, header : str):
        headerMatch = htcpcpHeaderRegex.match(header)
        matches = headerMatch.groupdict()
        self.headers[matches["key"].lower()] = matches["value"]

    def _isValid(self):
        return self.uri != None and self.method != None

if __name__== "__main__":
    x = HtcpcpRequest()
    x.setUri("English", "localhost", pot = 0)
    x.method = "BREW"
    print(x.create())
    print("----------------------")
    y = HtcpcpRequest.fromFile(io.StringIO(x.create()))
    print(y.create())
    print("----------------------")
    x.body = "No"
    print(x.create())
    print("----------------------")
    y = HtcpcpRequest.fromFile(io.StringIO(x.create()))
    print(y.create())

    print("----------------------")
    print("----------------------")

    a = HtcpcpResponse()
    a.status = 200
    a.message = "OK"
    print(a.create())
    print("----------------------")
    b = HtcpcpResponse.fromFile(io.StringIO(a.create()))
    print(b.create())
    print("----------------------")
    a.body = "No"
    print(a.create())
    print("----------------------")
    b = HtcpcpResponse.fromFile(io.StringIO(a.create()))
    print(b.create())