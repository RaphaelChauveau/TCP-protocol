import socket
import threading


class TCP:

    # var
    gui = None
    states = ["CLOSED", "LISTEN", "SYN-RECEIVED", "SYN-SENT", "ESTABLISHED"]
    current_state = states[0]

    sock = None
    client = None

    # TCB
    source_port = None
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
    def setup_send_socket(self, destination_port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect(("localhost", destination_port))

    def send_syn(self):  # TODO
        self.sock.send("SYN")

    def receive_syn(self):  # TODO
        self.sock.listen(5)
        self.client, self.client_address = self.sock.accept()
        print "connection", self.client_address

        msg = self.client.recv(255)
        print msg
        if msg == "SYN":
            self.send_syn_ack()
            return True
        return False

    def send_syn_ack(self):
        self.client.send("SYN_ACK")  # TODO notsure good address
        pass

    # CLOSED STATE
    def closed_open(self, source_port):

        if self.current_state != self.states[0]:
            print "[TCP] Error : closed_open"
            return

        if 0 < source_port < 65535:
            self.source_port = source_port

            # setup socket
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.bind(("", source_port))

            # get client
            self.change_state(self.states[1])

            def is_syn_received():
                if self.receive_syn():
                    self.change_state(self.states[2])
            threading.Thread(target=is_syn_received).start()  # TODO while !syn_received ?

        else:
            print "[TCP] Error : closed_open"

    def closed_send(self, destination_port):
        if self.current_state != self.states[0]:
            print "[TCP] Error : closed_open"
            return

        if 0 < destination_port < 65535:
            self.setup_send_socket(destination_port)
            self.send_syn()
            self.change_state(self.states[3])
        else:
            print "[TCP] Error : closed_send"

    # LISTEN STATE
    def listen_send_syn(self, destination_port):
        if self.current_state != self.states[1]:
            print "[TCP] Error : closed_open"
            return

        if 0 < destination_port < 65535:
            self.sock.close()  # clean stop listen
            self.setup_send_socket(destination_port)
            self.send_syn()
            self.change_state(self.states[3])
        else:
            print "[TCP] Error : listen_send_syn"
