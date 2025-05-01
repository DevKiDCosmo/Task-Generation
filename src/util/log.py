import datetime


class Log:
    def __init__(self):
        self.filename = datetime.datetime.now().strftime("%Y-%m-%d") + ".log"

    def write(self, message: str):
        print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " - " + message)
        with open(self.filename, 'a', encoding="utf-8") as f:
            f.write(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " - " + message + '\n')

    def create_log(self):
        with open(self.filename, 'w', encoding="utf-8") as f:
            f.write("Log file created at " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '\n')
            f.write("Log file name: " + self.filename + '\n')
