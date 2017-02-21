# AmbiBox hardware for Domoticz
#
# Author: kentra
#
"""
<plugin key="Ambibox" name="Ambibox - Ambient light" author="kentra" version="1.0.0" wikilink="http://www.domoticz.com/wiki/plugins/plugin.html" externallink="https://www.google.com/">
    <params>
        <param field="Address" label="IP Address" width="200px" required="true" default="127.0.0.1"/>
        <param field="Port" label="Port" width="30px" required="true" default="3636"/>
    </params>
</plugin>
"""
import Domoticz
import base64
from lib import ambibox
def stringToBase64(s):
    return base64.b64encode(s.encode('utf-8')).decode("utf-8")

class BasePlugin:
    enabled = False
    global running
    running = '0'
    def __init__(self):
        #self.var = 123
        return

    def onStart(self):
        Domoticz.Log("onStart called")
        
        Options = "LevelActions:"+stringToBase64("||||||")+";LevelNames:"+stringToBase64("Off|Blue|Purple|Cyan|Red|White|Green")

        Domoticz.Device(Name="AmbientLight", Unit=1, TypeName="Selector Switch", Options=Options).Create()
        Domoticz.Log("Devices created.")

    def onStop(self):
        Domoticz.Log("onStop called")

    def onConnect(self, Status, Description):
        Domoticz.Log("onConnect called")

    def onMessage(self, Data, Status, Extra):
        Domoticz.Log("onMessage called")

    def onCommand(self, Unit, Command, Level, Hue):
        Domoticz.Log("onCommand called for Unit " + str(Unit) + ": Parameter '" + str(Command) + "', Level: " + str(Level))
        Domoticz.Log("Connecting to ambibox:" + Parameters['Address'] + ":" + Parameters['Port'])
        ambibox.connect(Parameters['Address'], Parameters['Port'])

        if Level == 0:
            ambibox.disconnect()
            global running
            running = "0"
        #Blue  
        elif Level == 10:
            running = '0,0,255'
            ambibox.setColor('0', '0','255')
        #Purple
        elif Level == 20:
            running = '255,0,255'
            ambibox.setColor('255', '0','255')
        #Cyan
        elif Level == 30:
            running = '0,200,255'
            ambibox.setColor('0', '200','255')
        #Red
        elif Level == 40:
            running = '255,0,0'
            ambibox.setColor('255', '0','0')
        #White
        elif Level == 50:
            running = '255,255,255'
            ambibox.setColor('255', '255','255')
        #Green
        elif Level == 60:
            running = '0,255,0'
            ambibox.setColor('0', '255','0')

    def onNotification(self, Data):
        Domoticz.Log("onNotification: " + str(Data))

    def onDisconnect(self):
        Domoticz.Log("onDisconnect called")

    def onHeartbeat(self):
        global running
        if running != '0':
            Domoticz.Log("Ambibox - Ping")
            ambibox.setColor(running.split(',')[0], running.split(',')[1], running.split(',')[2])


global _plugin
_plugin = BasePlugin()

def onStart():
    global _plugin
    _plugin.onStart()

def onStop():
    global _plugin
    _plugin.onStop()

def onConnect(Status, Description):
    global _plugin
    _plugin.onConnect(Status, Description)

def onMessage(Data, Status, Extra):
    global _plugin
    _plugin.onMessage(Data, Status, Extra)

def onCommand(Unit, Command, Level, Hue):
    global _plugin
    _plugin.onCommand(Unit, Command, Level, Hue)

def onNotification(Data):
    global _plugin
    _plugin.onNotification(Data)

def onDisconnect():
    global _plugin
    _plugin.onDisconnect()

def onHeartbeat():
    global _plugin
    _plugin.onHeartbeat()

    # Generic helper functions
def DumpConfigToLog():
    for x in Parameters:
        if Parameters[x] != "":
            Domoticz.Debug( "'" + x + "':'" + str(Parameters[x]) + "'")
    Domoticz.Debug("Device count: " + str(len(Devices)))
    for x in Devices:
        Domoticz.Debug("Device:           " + str(x) + " - " + str(Devices[x]))
        Domoticz.Debug("Device ID:       '" + str(Devices[x].ID) + "'")
        Domoticz.Debug("Device Name:     '" + Devices[x].Name + "'")
        Domoticz.Debug("Device nValue:    " + str(Devices[x].nValue))
        Domoticz.Debug("Device sValue:   '" + Devices[x].sValue + "'")
        Domoticz.Debug("Device LastLevel: " + str(Devices[x].LastLevel))
    return