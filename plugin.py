# AmbiBox hardware for Domoticz
#
# Author: kentra
# Tested on Domoticz V3.6708
"""
<plugin key="Ambibox" name="Ambibox - Ambient light" author="kentra" version="1.0.0" wikilink="http://www.domoticz.com/wiki/plugins/plugin.html" externallink="https://github.com/kentra/domoticz-ambibox-plugin">
    <params>
        <param field="Address" label="IP Address" width="200px" required="true" default="127.0.0.1"/>
        <param field="Port" label="Port" width="30px" required="true" default="3636"/>
        <param field="Mode1" label="Debug" width="75px">
            <options>
                <option label="True" value="True"/>
                <option label="False" value="False"  default="true" />
            </options>
        </param>
    </params>
</plugin>
"""
import Domoticz
import base64
import colorsys
from lib import ambibox
def stringToBase64(s):
    return base64.b64encode(s.encode('utf-8')).decode("utf-8")

class BasePlugin:
    global lastColor
    #lastColor = '0'
    def __init__(self):
        #self.var = 123
        return

    def onStart(self):
        Domoticz.Log("onStart called")
        global colorPallet
        colorPallet = Domoticz.Device(Name="AmbientLight", Unit=2, Switchtype=7, Type=241, Subtype=2)
        colorPallet.Create()
        Domoticz.Log("Devices created.")
        # global ambiConnect

    def onStop(self):
        Domoticz.Log("onStop called")

    def onConnect(self, Status, Description):
        Domoticz.Log("onConnect called")

    def onMessage(self, Data, Status, Extra):
        Domoticz.Log("onMessage called")

    def onCommand(self, Unit, Command, Level, Hue):
        global colorPallet
        global lastColor
        Domoticz.Log(str(Command))
        if not ambibox.ping():
            # Connect
            if ambibox.connect(Parameters['Address'], Parameters['Port']):
                Domoticz.Log('Connected to: ' + Parameters['Address'] + ':' + Parameters['Port'])
            else:
                Domoticz.Error('Could not connect to ' + Parameters['Address'] + ':' + Parameters['Port'])
        if str(Command) == 'On':
            colorPallet.Update(nValue=1, sValue=str(Command), SignalLevel=50, Image=8)
            if lastColor != '0':
                ambibox.setColor(lastColor.split(',')[0], lastColor.split(',')[1], lastColor.split(',')[2])
            global lastColor
            #lastColor = '1'
        if str(Command) == 'Off':
            colorPallet.Update(nValue=0, sValue=str(Command), SignalLevel=50, Image=8)
            ambibox.disconnect()
            global lastColor
            #lastColor = '0'
        if str(Command) == 'Set Color':
            color = int(Level)
        if str(Command) == 'Set Brightness':
            brightness = int(Level)
        if str(Command) == 'Set Level' and color:
            brightness = int(Level)
        #Set Color
        if str(Command) not in ['On', 'Off', 'Set Color'] and ambibox.ping():
            try:
                global brightness
                global color
                rgb = colorsys.hls_to_rgb(color / 359, brightness, 1)
                ambibox.setColor(str(int(rgb[1])), str(int(rgb[2])), str(int(rgb[0])))
                global lastColor
                lastColor = str(int(rgb[1])) + ',' + str(int(rgb[2])) + ',' + str(int(rgb[0]))
                Domoticz.Debug('Red: ' + str(rgb[0])  + ' Green: ' + str(rgb[1]) + ' Blue: ' + str(rgb[2]))
            except:
                Domoticz.Error("Failed to set color")

    def onNotification(self, Data):
        Domoticz.Log("onNotification: " + str(Data))

    def onDisconnect(self):
        Domoticz.Log("onDisconnect called")

    def onHeartbeat(self):
        global lastColor
        if ambibox.ping():
            Domoticz.Debug('Keepalive: Keeping connection alive')
            ambibox.setColor(lastColor.split(',')[0], lastColor.split(',')[1], lastColor.split(',')[2])
        elif not ambibox.ping():
            Domoticz.Debug('Keepalive: No connection')

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
