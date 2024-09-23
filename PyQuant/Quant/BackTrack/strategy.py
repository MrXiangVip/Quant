
class Strategy():
    def __init__(self, lines):
        self.lines=lines
        self.total=10000
        self.position=False
        self.orders=0
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
        print("buy start", dt.trade_date, "买入价格 ", dt.low)
        self.orders =int(self.total/(dt.low*100))
        self.total -= dt.low * self.orders*100
        print( " 现金:", self.total, " 股票：", dt.low*self.orders*100, " 总资产: ", self.total+dt.low*self.orders*100 )
        print("buy end")

    def sell(self, dt ):
        print("sell start", dt.trade_date, "卖出价格 ", dt.close)
        self.total += dt.close*self.orders*100
        print(" 总资产: ", self.total )
        print("sell end")