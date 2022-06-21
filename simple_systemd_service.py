import dbus


class SimpleSystemDServiceAccess(object):

    def __init__(self,name, mode = 'fail') -> None:
        '''
            provide service name (bla.service)
            for possible modes refer to (StartUnit description) : https://www.freedesktop.org/wiki/Software/systemd/dbus/
        '''
        self.name = name
        self.mode = mode
        self.sysbus = dbus.SystemBus()
        self.systemd1 = dbus.SystemBus().get_object('org.freedesktop.systemd1', '/org/freedesktop/systemd1')
        self.manager = dbus.Interface(self.systemd1, 'org.freedesktop.systemd1.Manager')

    def StartService(self):
        '''
        Will Start an Systemd Service if available
        
        (Admin Rights needed !)
        if service is not available or name is wrong dbus will rise an Exception !
        '''
        self.manager.StartUnit(self.name,self.mode)

    def StopService(self):
        '''
        Will Stop an Systemd Service if available

        (Admin Rights needed !)
        if service is not available or name is wrong dbus will rise an Exception !
        '''
        self.manager.StopUnit(self.name,self.mode)

    def RestartService(self):
        '''
        Will Restart an Systemd Service if available
        
        (Admin Rights needed !)
        if service is not available or name is wrong dbus will rise an Exception !
        '''
        self.manager.RestartUnit(self.name,self.mode)
    

    def IsRunning(self) -> bool:
        '''
        Will check if an service is running.
        Code is an copy from stackoverflow (https://stackoverflow.com/questions/43499880/how-to-extract-service-state-via-systemd-dbus-api)

        will return True if service is running, and false is Service is not running
        '''
        status = False
        try:
            service = self.sysbus.get_object('org.freedesktop.systemd1',object_path=self.manager.GetUnit(self.name))
            interface = dbus.Interface(service,dbus_interface='org.freedesktop.DBus.Properties')
            ActiveState = interface.Get('org.freedesktop.systemd1.Unit', 'ActiveState')
            LoadState = interface.Get('org.freedesktop.systemd1.Unit', 'LoadState')
            if LoadState == 'loaded' and ActiveState == 'active':
                status = True
        except dbus.exceptions.DBusException:
            # dbus will rise Exception if not running ...
            pass
        
        return status