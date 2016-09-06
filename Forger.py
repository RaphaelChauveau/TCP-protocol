class Packet:

    # 16 bit
    source_port = 0
    destination_port = 0

    # 32 bit
    sequence_number = 0
    reception_ack = 0

    # 4 bit
    data_offset = 0

    # 6 bit
    reserved = 0

    # 1 bit
    urg = 0
    ack = 0
    psh = 0
    rst = 0
    syn = 0
    fin = 0

    # 16 bit
    window = 0
    checksum = 0
    urgent_data = 0

    # variable (multiple de 8 bit)
    options = 0

    # variable (entete multiple de 32 bit)
    padding = 0

    payload = 0

    def __init__(self, source_port, destination_port, syn, ack):
        self.source_port = source_port
        self.destination_port = destination_port
        self.syn = syn
        self.ack = ack

    def to_string(self):
        str_source_port =
        packet = \
            "a"\
            "b"
        print packet

if __name__ == "__main__":
    toto = Packet(0, 0, 0, 0)
    toto.to_string()
