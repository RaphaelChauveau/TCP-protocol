import GUI
import TCP

if __name__ == "__main__":
    gui = GUI.App()
    tcp = TCP.TCP(gui)
    gui.set_tcp(tcp)

    gui.bind("<<CLOSED>>", gui.change_state_closed)
    gui.bind("<<LISTEN>>", gui.change_state_listen)
    gui.bind("<<SYN-RECEIVED>>", gui.change_state_syn_received)
    gui.bind("<<SYN-SENT>>", gui.change_state_syn_sent)
    gui.bind("<<ESTABLISHED>>", gui.change_state_established)

    gui.mainloop()
