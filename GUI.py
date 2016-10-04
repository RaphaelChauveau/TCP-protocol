from tkinter import *
import socket

TITLE_FONT = ("Helvetica", 18, "bold")


class App(Tk):
    tcp = None
    source_ip = socket.gethostbyname(socket.gethostname())

    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)

        label = Label(self, text="Local IP : "+self.source_ip)
        label.pack()

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (ClosedFrame, ListenFrame, SYNReceivedFrame, SYNSentFrame, EstablishedFrame, FinWait1Frame,
                  FinWait2Frame, TimeWaitFrame, CloseWaitFrame, LastAckFrame):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("ClosedFrame")

    def set_tcp(self, tcp):
        self.tcp = tcp

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()

    def change_state_closed(self, *args):  # on a besoin du *args pour le call via event
        self.show_frame("ClosedFrame")

    def change_state_listen(self, *args):
        self.show_frame("ListenFrame")

    def change_state_syn_received(self, *args):
        self.show_frame("SYNReceivedFrame")

    def change_state_syn_sent(self, *args):
        self.show_frame("SYNSentFrame")

    def change_state_established(self, *args):
        self.show_frame("EstablishedFrame")

    def change_state_fin_wait_1(self, *args):
        self.show_frame("FinWait1Frame")

    def change_state_fin_wait_2(self, *args):
        self.show_frame("FinWait2Frame")

    def change_state_time_wait(self, *args):
        self.show_frame("TimeWaitFrame")

    def change_state_close_wait(self, *args):
        self.show_frame("CloseWaitFrame")

    def change_state_last_ack(self, *args):
        self.show_frame("LastAckFrame")

    def create_button_last_ack(self):
        self.frames["FinWait2Frame"].create_button_last_ack()

    def delete_button_last_ack(self):
        self.frames["FinWait2Frame"].delete_button_last_ack()


class ClosedFrame(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        label = Label(self, text="State : Closed", font=TITLE_FONT)
        label.pack(side="top", fill="x", pady=10)

        labelframe = LabelFrame(self, text="Passive OPEN")
        labelframe.pack()
        labal2 = Label(labelframe, text="source port : ")
        labal2.pack()
        spinbox = Spinbox(labelframe, from_=0, to_=9999)
        spinbox.delete(0, "end")
        spinbox.insert(0, 4242)
        spinbox.pack()
        button = Button(labelframe, text="Open",
                        command=lambda: controller.tcp.closed_open(int(spinbox.get())))
        button.pack()

        labelframe2 = LabelFrame(self, text="Active OPEN")
        labelframe2.pack()

        labal4 = Label(labelframe2, text="source port : ")
        labal4.pack()
        spinbox3 = Spinbox(labelframe2, from_=0, to_=9999)
        spinbox3.delete(0, "end")
        spinbox3.insert(0, 4343)
        spinbox3.pack()

        labal5 = Label(labelframe2, text="destination ip address : ")
        labal5.pack()
        entry = Entry(labelframe2)
        entry.pack()

        labal3 = Label(labelframe2, text="destination port : ")
        labal3.pack()
        spinbox2 = Spinbox(labelframe2, from_=0, to_=9999)
        spinbox2.delete(0, "end")
        spinbox2.insert(0, 4242)
        spinbox2.pack()

        button2 = Button(labelframe2, text="Send",
                         command=lambda: controller.tcp.closed_send(int(spinbox2.get()), int(spinbox3.get()),
                                                                    entry.get()))
        button2.pack()


class ListenFrame(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        label = Label(self, text="State : Listen", font=TITLE_FONT)
        label.pack(side="top", fill="x", pady=10)

        labelframe = LabelFrame(self, text="SEND")
        labelframe.pack()
        label2 = Label(labelframe, text="destination port : ")
        label2.pack()
        spinbox = Spinbox(labelframe, from_=0, to_=9999)
        spinbox.pack()
        button = Button(labelframe, text="Send SYN",
                        command=lambda: controller.tcp.listen_send_syn(int(spinbox.get())))
        button.pack()

        button2 = Button(self, text="Receive SYN",
                         command=lambda: controller.show_frame("SYNReceivedFrame"))
        button2.pack()


class SYNSentFrame(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        label = Label(self, text="State : SYN-Sent", font=TITLE_FONT)
        label.pack(side="top", fill="x", pady=10)


class SYNReceivedFrame(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        label = Label(self, text="State : SYN-Received", font=TITLE_FONT)
        label.pack(side="top", fill="x", pady=10)
        button = Button(self, text="Send SYN + ACK",
                        command=lambda: controller.tcp.syn_received_send_syn_ack())
        button.pack()


class EstablishedFrame(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        self.listbox = None
        label = Label(self, text="State : Established", font=TITLE_FONT)
        label.pack(side="top", fill="x", pady=10)

        labelframe = LabelFrame(self, text="Send data")
        labelframe.pack()
        entry = Entry(labelframe)
        entry.pack()

        def send_button_clicked():
            controller.tcp.established_send_data(entry.get())
            entry.delete(0, END)

        button = Button(labelframe, text="Send", command=send_button_clicked)
        button.pack()

        button = Button(self, text="Close, Send FIN",
                        command=lambda: controller.tcp.established_close())
        button.pack()

        bar = Scrollbar(self)
        bar.pack(side=RIGHT, fill=Y)

        self.listbox = Listbox(self)
        self.listbox.pack()

        self.listbox.config(yscrollcommand=bar.set)
        bar.config(command=self.listbox.yview)

    def showmessage(self, message):
        self.listbox.insert(END, message)
        #label2 = Label(self, text=message, font=TITLE_FONT)
        #label2.pack()


class FinWait1Frame(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        label = Label(self, text="State : Fin-Wait-1", font=TITLE_FONT)
        label.pack(side="top", fill="x", pady=10)


class FinWait2Frame(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        label = Label(self, text="State : Fin-Wait-2", font=TITLE_FONT)
        label.pack(side="top", fill="x", pady=10)

        self.button = Button(self, text="Send ACK", command=lambda: self.controller.tcp.fin_wait2_send_ack(), state="disabled")
        self.button.pack()

    def create_button_last_ack(self):
        self.button.config(state="normal")

    def delete_button_last_ack(self):
        self.button.config(state="disabled")


class TimeWaitFrame(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        label = Label(self, text="State : Time-Wait", font=TITLE_FONT)
        label.pack(side="top", fill="x", pady=10)


class CloseWaitFrame(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        label = Label(self, text="State : Close-Wait", font=TITLE_FONT)
        label.pack(side="top", fill="x", pady=10)

        def send_fin(button):
            controller.tcp.close_wait_send_fin()
            button.config(text="Send ACK", command=lambda: send_ack(button))

        def send_ack(button):
            controller.tcp.close_wait_send_ack()
            button.config(text="Send Fin", command=lambda: send_fin(button))

        button = Button(self, text="Send ACK",
                        command=lambda: send_ack(button))
        button.pack()


class LastAckFrame(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        label = Label(self, text="State : Last-Ack", font=TITLE_FONT)
        label.pack(side="top", fill="x", pady=10)


def startapp():
    app = App()
    app.mainloop()
