from datetime import datetime

class logger:

    def __init__(self,file):
        self.file = file+"_log.txt"
        self._log = []
        self.logging_on = True

    def log(self,message):
        _time = datetime.now ( ).strftime ( '%Y-%m-%d %H:%M:%S' )
        if self.logging_on == True:
            self._log.append ( str ( _time ) + ": " + message )
        return
    def write_log(self):
        if self.logging_on == True:
            f = open(self.file,'a+')
            for message in self._log:
                f.write(message + '\r\n')
            f.close()
        self._log = []