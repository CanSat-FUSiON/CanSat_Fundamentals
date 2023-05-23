class Reset:
    def __init__(self, file_name, encoding):
        self.file_name = file_name
        self.encoding = encoding

    def set(self):
        self.sleeptime = self.read()

    def read(self):
        f = open(self.file_name+'.txt', 'r', encoding=self.encoding)
        sleeptime = f.read()
        f.close()
        return int(sleeptime)

    def rewrite(self, resettime):
        f = open(self.file_name+'.txt', 'w')
        f.write(str(resettime))
        f.close()
