import threading, time, sys
from scapy.all import *


listening_ip = '192.168.0.220'
PORT = 502

functioncode_dictionary = {
    "0x01": "ReadCoilsRequest",
    "0x02": "ReadDiscreteInputsRequest",
    "0x03": "ReadHoldingRegistersRequest",
    "0x04": "ReadInputRegistersRequest",
    "0x05": "WriteSingleCoilRequest",
    "0x06": "WriteSingleRegisterRequest",
    "0x07": "ReadExceptionStatusRequest",
    "0x08": "DiagnosticsRequest",
    "0x0B": "BGetCommEventCounterRequest",
    "0x0C": "CGetCommEventLogRequest",
    "0x0F": "FWriteMultipleCoilsRequest",
    "0x10": "WriteMultipleRegistersRequest",
    "0x11": "ReportSlaveIdRequest",
    "0x14": "ReadFileRecordRequest",
    "0x15": "WriteFileRecordRequest",
    "0x16": "MaskWriteRegisterRequest",
    "0x17": "ReadWriteMultipleRegistersRequest",
    "0x18": "ReadFIFOQueueRequest"
}

diagnostic_sub_functions = {
    "0x00": "Return Query Data",
    "0x01": "Restart Communications Option",
    "0x02": "Return Diagnostic Register",
    "0x03": "Change ASCII Input Delimiter",
    "0x04": "Force Listen Only Mode",
    "0x0A": "Clear Counters and Diagnostic Register",
    "0x0B": "Return Bus Message Count",
    "0x0C": "Return Bus Communication Error Count",
    "0x0D": "Return Bus Exception Error Count",
    "0x0E": "Return Slave Message Count",
    "0x0F": "Return Slave No Response Count",
    "0x10": "Return Slave NAK Count",
    "0x11": "Return Slave Busy Count",
    "0x12": "Return Bus Character Overrun Count",
    "0x14": "Clear Overrun Counter and Flag"
}


subfun = 4
# Modbus ADU
class ModbusTCP(Packet):
    name = "Modbus/TCP"
    fields_desc = [ ShortField("Transaction Identifier", 1),
                    ShortField("Protocol Identifier", 0),
                    ShortField("Length", 6),
                    XByteField("Unit Identifier", 247),
                    ]

# Modbus PDU
class Modbus(Packet):
    name = "Modbus"
    fields_desc = [ XByteField("Function Code", 8),
                    ShortField("subFunc", subfun),
                    ShortField("Reference Number", 1),
                    ShortField("Word Count", 2),
                    ]


def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((listening_ip, PORT))
    server.listen(5)
    print(f'[*] Listening on {listening_ip}:{PORT}')

    while True:
        client, address = server.accept()
        print(f'[*] Accepted connection from {address[0]}:{address[1]}')
        client_handler = threading.Thread(target=handle_client, args=(client,))
        client_handler.start()

def handle_client(client_socket):
    with client_socket as sock:
        request = sock.recv(4096)
        print(request)
        # Converts the Data Received into a list of strings
        pdu_hex_list = [('0x'+(hex(x)[2:]).capitalize().zfill(2)) for x in request]
        # Looks at the functioncode_dictionary list to find the function code being used
        print(functioncode_dictionary[pdu_hex_list[7]])
        
        if(pdu_hex_list[7] == "0x08"):
            print(diagnostic_sub_functions[pdu_hex_list[9]])
        elif(pdu_hex_list[7] == "0x05"):
            print(pdu_hex_list[9])
            print(pdu_hex_list[11])
            
        sock.send(bytes(ModbusTCP()/Modbus()))

if __name__ == '__main__':
    main()
