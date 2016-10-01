import socket
import threading


class TCP:

    # var
    gui = None
    states = ["CLOSED", "LISTEN", "SYN-RECEIVED", "SYN-SENT", "ESTABLISHED"]
    current_state = states[0]

    sock_listen = None
    sock_send = None
    client = None

    # TCB
    source_port = None
    dest_port = None
    client_address = None

    def log(self, text):
        print "TCP :", text

    def __init__(self, gui):
        self.gui = gui

    def change_gui_state(self, state):  # On a besoin d'utiliser des events car Tkinter ne suporte pas les threads
        if state == self.states[0]:
            self.gui.event_generate("<<" + self.states[0] + ">>", when="tail")
        elif state == self.states[1]:
            self.gui.event_generate("<<" + self.states[1] + ">>", when="tail")
        elif state == self.states[2]:
            self.gui.event_generate("<<" + self.states[2] + ">>", when="tail")
        elif state == self.states[3]:
            self.gui.event_generate("<<" + self.states[3] + ">>", when="tail")
        elif state == self.states[4]:
            self.gui.event_generate("<<" + self.states[4] + ">>", when="tail")
        else:
            print "Error TCP : change_gui_state"

    def change_state(self, state):
        self.log("change state " + state)
        self.current_state = state
        self.change_gui_state(state)

    # UTIL
    def setup_send_socket(self):
        self.sock_send = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print self.dest_port
        self.sock_send.connect(("localhost", self.dest_port))

#CONNEXION DIALOG FERMETURE
    def send_syn(self):  # TODO
        self.sock_send.send("CONNEXION_SYN "+ str(self.source_port))

    def handle_msg(self, msg):
        print msg
        tokens = msg.split(" ")
        if tokens[0] == "CONNEXION_SYN":
            self.dest_port = int(tokens[1])
            self.setup_send_socket()

            self.change_state(self.states[2])

        elif tokens[0] == "CONNEXION_SYN_ACK":
            self.sock_send.send("CONNEXION_ACK")
            self.change_state(self.states[4])

        elif tokens[0] == "CONNEXION_ACK":
            self.change_state(self.states[4])

        elif tokens[0] == "ESTABLISHED_SEND":
            #RCV.NXT incr
            print "RECEIVED :", tokens[1]
            self.sock_send.send("ESTABLISHED_ACK")

        elif tokens[0] == "ESTABLISHED_ACK":
            #SND.UNA incr
            print "RECEIVED ACK"


    def start_listening(self):
        print "start listening start"
        self.sock_listen.listen(5)
        self.client, self.client_address = self.sock_listen.accept()
        print "connection", self.client_address

        while self.current_state != self.states[0]: #while not closed
            msg = self.client.recv(255)# might need to change the size
            self.handle_msg(msg)

    # CLOSED STATE
    def closed_open(self, source_port):

        if self.current_state != self.states[0]:
            print "[TCP] Error : closed_open"
            return

        if 0 < source_port < 65535:
            self.source_port = source_port

            # setup listen socket
            self.sock_listen = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock_listen.bind(("", source_port))
            threading.Thread(target=self.start_listening).start()

            self.change_state(self.states[1])  # LISTEN
        else:
            print "[TCP] Error : closed_open"

    def closed_send(self, destination_port, source_port):
        if self.current_state != self.states[0]:
            print "[TCP] Error : closed_open"
            return

        if 0 < destination_port < 65535 and 0 < source_port < 65535:
            self.source_port = source_port
            self.dest_port = destination_port

            # setup listen socket
            self.sock_listen = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock_listen.bind(("", source_port))
            threading.Thread(target=self.start_listening).start()

            # setup send socket
            self.setup_send_socket()

            self.send_syn()
            self.change_state(self.states[3])
        else:
            print "[TCP] Error : closed_send"

    # LISTEN STATE
    def listen_send_syn(self, destination_port):  # TODO bullshit
        if self.current_state != self.states[1]:
            print "[TCP] Error : closed_open"
            return

        if 0 < destination_port < 65535:
            self.sock_listen.close()  # clean stop listen
            self.setup_send_socket(destination_port)
            self.send_syn()
            self.change_state(self.states[3])
        else:
            print "[TCP] Error : listen_send_syn"

    # SYN-RECEIVED STATE
    def syn_received_send_syn_ack(self):
        self.sock_send.send("CONNEXION_SYN_ACK")

    # ESTABLISHED STATE
    def send_data(self, data):
        #SND.NXT incr
        print "SEND :", data
        self.sock_send.send("ESTABLISHED_SEND " + str(data))
