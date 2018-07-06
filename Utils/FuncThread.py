import threading

class FuncThread(threading.Thread):
    '''
    class to create new thread for continuously measuring, this will not be 
    interrupted by the data plotting. 
    '''
    def __init__(self,t,*a):
        self._t=t
        self._a=a
        threading.Thread.__init__(self)
    
    def run(self):
        self._t(*self._a)