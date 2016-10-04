import GUI
import TCP
from tkinter import messagebox
if __name__ == "__main__":
    gui = GUI.App()
    tcp = TCP.TCP(gui)
    gui.set_tcp(tcp)


    def on_closing():
        if messagebox.askokcancel("TCP-protocol", "Are you sure you want to terminate the connection?"):
            gui.destroy()


    gui.protocol("WM_DELETE_WINDOW", on_closing)

    gui.bind("<<CLOSED>>", gui.change_state_closed)
    gui.bind("<<LISTEN>>", gui.change_state_listen)
    gui.bind("<<SYN-RECEIVED>>", gui.change_state_syn_received)
    gui.bind("<<SYN-SENT>>", gui.change_state_syn_sent)
    gui.bind("<<ESTABLISHED>>", gui.change_state_established)
    gui.bind("<<FIN-WAIT-1>>", gui.change_state_fin_wait_1)
    gui.bind("<<FIN-WAIT-2>>", gui.change_state_fin_wait_2)
    gui.bind("<<TIME-WAIT>>", gui.change_state_time_wait)
    gui.bind("<<CLOSE-WAIT>>", gui.change_state_close_wait)
    gui.bind("<<LAST-ACK>>", gui.change_state_last_ack)

    gui.mainloop()
