


class BackBroker():
    def __init__(self):
       self._value=0

    def set_cash(self, cash):
        '''Sets the cash parameter (alias: ``setcash``)'''
        self.startingcash = self.cash = cash
        self._value = cash

    setcash = set_cash