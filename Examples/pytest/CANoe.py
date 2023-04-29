import win32com.client
import win32com.client.connect
import time, os

#COM
def DoEvents():
    win32com.client.connect.pythoncom.PumpWaitingMessages()
    time.sleep(.1)
def DoEventsUntil(cond):
    while not cond():
        DoEvents()


class CanoeSync(object):
    """Wrapper class for CANoe Application object"""
    Started = False
    Stopped = False
    ConfigPath = ""
    def __init__(self):
        app = win32com.client.DispatchEx('CANoe.Application')
        self.App = app
        self.Meas = app.Measurement
        self.Running = lambda : self.Meas.Running
        self.WaitForStart = lambda : DoEventsUntil(lambda: CanoeSync.Started)
        self.WaitForStop = lambda: DoEventsUntil(lambda: CanoeSync.Stopped)
        win32com.client.WithEvents(self.App.Measurement, CanoeMeasurementEvents)


    def Load(self, cfgPath):
        # current dir must point to the script file
        cfg = os.path.join(os.curdir, cfgPath)
        cfg = os.path.abspath(cfg)
        print('Opening: ', cfg)
        self.ConfigPath = os.path.dirname(cfg)
        self.Configuration = self.App.Configuration
        self.App.Open(cfg)

    def Start(self):
        if not self.Running():
            self.Meas.Start()
            self.WaitForStart()

    def Stop(self):
        if self.Running():
            self.Meas.Stop()
            self.WaitForStop()

    def SetSysvarValue(self, namespace, name, value):
        self.App.System.Namespaces.Item(namespace).Variables.Item(name).Value = value

    #Method returns arrays as lists for easier handling
    def ReadSysvarValue(self, namespace, name):        
        var=self.App.System.Namespaces.Item(namespace).Variables.Item(name)
        var=win32com.client.CastTo(var, "IVariable12")
        #for type Data
        if(var.Type == 7):
            listVar=list(var.Value)
            for i in range(0, len(listVar)):
               listVar[i] = listVar[i] & 0xFF
            return listVar
        #for type Integer or Double Array
        elif(var.Type == 4) or (var.Type == 5):
            listVar=list(var.Value)
            return listVar
        else:
            return var.Value
        
    def PrintNamespaces(self):
        for i in range(self.App.System.Namespaces.Count):
            print(str(i) + ": " + self.App.System.Namespaces.Item(i+1).Name)
  
    def GetSignalValue(self,bus_type,channel_num, msg_name, sig_name):
        #bus_type = "Eth"
        result = self.App.GetBus(bus_type).GetSignal(channel_num, msg_name, sig_name)
        #print("Signal: " + result.FullName)
        return result.Value
        
    def SetSignalValue(self,bus_type,channel_num, msg_name, sig_name, set_value):
        #bus_type = "Ethernet"
        signal = self.App.GetBus(bus_type).GetSignal(channel_num, msg_name, sig_name)
        signal.Value = set_value
        #print("Signal: " + result.FullName)
        return 
    
    def GetEnvvarValue(self,envvar_name):
        return self.App.Environment.GetVariable(envvar_name).Value
    
    def SetEnvvarValue(self,envvar_name, value):
        envvar = self.App.Environment.GetVariable(envvar_name) 
        envvar.Value = value
        time.sleep(0.5)
        return 
    
        


class CanoeMeasurementEvents(object):
    """Handler for CANoe measurement events"""
    def OnStart(self):
        CanoeSync.Started = True
        CanoeSync.Stopped = False
        print("Measurement started")
    def OnStop(self) :
        CanoeSync.Started = False
        CanoeSync.Stopped = True
        print("Measurement stopped")

