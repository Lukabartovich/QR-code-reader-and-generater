import qrcode
import yagmail
import random
import os
from time import strftime

import cv2
import webbrowser

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder

Builder.load_file('layout6.kv')


class Home(Screen):
    def scan(self):
        self.manager.current = 'scan'

    def generate(self):
        self.manager.current = 'generate'


class Scan(Screen):
    def start(self):
        self.ids.camera.play = True
        self.ids.camera.opacity = 1

    def capture(self):
        file_name = strftime('%Y%m%d-%H%M%S')
        self.ids.camera.export_to_png(f'files/{file_name}.png')
        # print(file_name)
        image = cv2.imread(f'files/{file_name}.png')
        detector = cv2.QRCodeDetector()

        url, coords, pixels = detector.detectAndDecode(image)
        if url:
            list1 = []
            string = ''

            list1.extend(url)
            if len(list1) > 8:
                for i in range(8):
                    string = string + list1[i]
                if string == 'https://' or string == 'http://':
                    self.manager.current = 'result'
                    self.manager.current_screen.ids.result_label.text = url
                    webbrowser.open(url)
                else:
                    self.manager.current = 'result'
                    self.manager.current_screen.ids.result_label.text = url
                    # print(url)
            else:
                self.manager.current = 'result'
                self.manager.current_screen.ids.result_label.text = url
                # print(url)

    def back(self):
        self.manager.current = 'home'


class Result(Screen):
    def back(self):
        self.manager.current = 'scan'
        self.manager.current_screen.ids.camera.play = False
        self.manager.current_screen.ids.camera.opacity = 0


class Generate(Screen):
    def make(self, i):
        qr = qrcode.make(i)
        self.filename = strftime('%Y%Y%m%d-%H%M%S')
        os.mkdir('qrs')
        qr.save(f'qrs/{self.filename}.jpeg')

    def generate(self):
        self.i_t = self.ids.input.text
        if len(self.i_t) > 0:
            self.make(self.i_t)
            file = 'qrs/' + str(self.filename) + '.jpeg'
            # print(file)

            self.manager.current = 'qr'
            self.manager.current_screen.ids.qr.source = file


class QR(Screen):
    def back(self):
        self.manager.current = 'home'

    def send(self):
        self.file = self.ids.qr.source
        # print(self.file)

        with open('name.txt', 'w') as file:
            file.write(self.file)

        self.manager.current = 'send'


class Send(Screen):
    def sender(self, e, j):
        try:
            server = yagmail.SMTP(user="lukabartovich@gmail.com",
                                  password="yzwsawmzerqukyzp")

            server.send(to=e,
                        subject=f'qr code{str(" " * random.randint(0, 3))}'
                                f'{random.randint(1, 5)}',
                        attachments=j)
        except TypeError:
            print('net')

    def send(self):
        try:
            self.email = self.ids.email.text

            with open('name.txt', 'r+') as file:
                self.file = file.read()
                file.truncate(0)

            self.sender(self.email, self.file)

            self.manager.current = 'home'
        except yagmail.error.YagInvalidEmailAddress:
            print('not')


class Root(ScreenManager):
    pass


class MainApp(App):
    def build(self):
        return Root()


if __name__ == '__main__':
    MainApp().run()
