from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from scapy.all import *
import json, time


#Set the PLC's IP Address/Port
IP = "192.168.0.121"
PORT = 502


# Modbus ADU
class ModbusTCP(Packet):
    name = "Modbus/TCP"
    fields_desc = [ ShortField("Transaction Identifier", 1),
                    ShortField("Protocol Identifier", 0),
                    ShortField("Length", 6),
                    XByteField("Unit Identifier", 247),
                    ]



def WriteSingleCoilRequest_pdu():
    print("YES")
    class Modbus(Packet):
        name = "Modbus"
        fields_desc = [ XByteField("Function Code", 5),
                        ShortField("outputAddr", 25), #Any number from 0 to 65535
                        ShortField("outputValue", 255), # 0 or 255
                        ]
    return Modbus()

def diag_pdu():
    class Modbus(Packet):
        name = "Modbus"
        fields_desc = [ XByteField("Function Code", 8),
                        ShortField("subFunc", 4),
                        ShortField("Reference Number", 1),
                        ShortField("Word Count", 2),
                        ]
    return Modbus()





  
# Call to the PLC
def change_plc(new_val):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((IP, PORT))

    #Change diag_pdu to whichever type of communication you're sending
    p = Raw(ModbusTCP()/WriteSingleCoilRequest_pdu())
    s.send(bytes(p))
    response = s.recv(4096)
    str_resp = [('0x'+hex(x)[2:].zfill(2)) for x in response]
    s.close()
    return str_resp




# AJAX Function to get changes from the Dashboard
def ajax_rsp(request):
    if request.method == "POST" and request.is_ajax():
        functioncode = request.POST.get("func_code")
    name = {'name': change_plc(functioncode)}
    return HttpResponse(json.dumps({'name': name}), content_type="application/json")



def stop_train(request):
    if request.method == "POST" and request.is_ajax():
        functioncode = request.POST.get("func_code")
    name = {'name': change_plc(functioncode)}
    return HttpResponse(json.dumps({'name': name}), content_type="application/json")



def index(request):
    return render(request, 'webgui/index.html')


def train(request):
    return render(request, 'webgui/train.html')