import telnetlib
import time
def connect(ip, port=3636):
    global tn
    tn = telnetlib.Telnet(ip, port, 3600)
    tn.read_until(b'')
    tn.write(b'lock\n')
def setColor(red='255', green='0', blue='100', num=206):
    payload = 'setcolor:'
    for i in range(1, num):
        payload += str(i) + '-' + red + ',' + green + ',' + blue + ';'
    tn.write(payload.encode())
    tn.write(b'\n\r')

def disconnect(num=206):
    payload = 'setcolor:'
    for i in range(1, num):
        payload += str(i) + '-0,0,0;'
    tn.write(payload.encode())
    tn.write(b'\n')
    tn.write(b'unlock\n')
    tn.write(b'exit\n')
    tn.close()

def ping():
    try:
        tn.write(b'\n\r')
    except:
        return 'Not Connected'