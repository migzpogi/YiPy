import win32serviceutil
import win32service
import win32event
import servicemanager
import socket
import logging.config

class AppServerSvc (win32serviceutil.ServiceFramework):
    _svc_name_ = "TestService"
    _svc_display_name_ = "Test Service"

    def __init__(self,args):
        win32serviceutil.ServiceFramework.__init__(self,args)
        self.hWaitStop = win32event.CreateEvent(None,0,0,None)
        socket.setdefaulttimeout(60)

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)

    def SvcDoRun(self):
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                              servicemanager.PYS_SERVICE_STARTED,
                              (self._svc_name_,''))
        self.main()

    def main(self):
        rc = None
        with open("C:\\test.txt", 'w') as f:
            while rc != win32event.WAIT_OBJECT_0:
                f.write('Hello +\n')
                rc = win32event.WaitForSingleObject(self.hWaitStop, 5000)


if __name__ == '__main__':
    win32serviceutil.HandleCommandLine(AppServerSvc)

    # documentation here:
    # http: // www.chrisumbel.com / article / windows_services_in_python
    # https://stackoverflow.com/questions/32404/is-it-possible-to-run-a-python-script-as-a-service-in-windows-if-possible-how

    # sc.exe delete TestService