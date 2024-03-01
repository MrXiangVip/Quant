
class Strategy():
    def __init__(self, lines):
        self.lines=lines
        # print(id(self.lines), id(lines))

    def _start(self):
        self.start()

    def start(self):
        pass

    def _stop(self):
        self.stop()

    def stop(self):
        pass

    def _oncepost(self, dt0):
        self.forward(dt0)
        self.next()
        self.advance()

    def next(self):
        pass


    def forward(self, dt0):
        for i, line in enumerate(self.lines):
            line.forward(dt0[i])

    def advance(self):
        for i , line in enumerate(self.lines):
            line.advance()


    def buy(self, dt):
        print("buy start")
        print(dt)
        print("buy end")

    def sell(self, dt ):
        print("sell", dt)