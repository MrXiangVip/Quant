import itertools

from .broker import BackBroker

import pandas as pd
class Cerebro():
    def __init__(self):
        self.lines = list()
        self.strats = list()
        self._broker = BackBroker()
        self._broker.cerebro = self

    def addstrategy(self, strategy, *args, **kwargs):
        self.strats.append([(strategy, args, kwargs)])
        return len(self.strats) - 1

    def adddata(self, data, name=None):
        # data.setenvironment(self)
        self.lines.append(data)
        return  data

    def setbroker(self, broker):
        '''
        Sets a specific ``broker`` instance for this strategy, replacing the
        one inherited from cerebro.
        '''
        self._broker = broker
        broker.cerebro = self
        return broker

    def getbroker(self):
        '''
        Returns the broker instance.

        This is also available as a ``property`` by the name ``broker``
        '''
        return self._broker

    broker = property(getbroker, setbroker)


    def run(self, **kwargs):
        # if not self.lines:
        #     return []  # nothing can be run
        self.runstrats = list()
        iterstrats = itertools.product(*self.strats)
        for iterstrat in iterstrats:
            runstrat = self.runstrategies(iterstrat)
            self.runstrats.append( runstrat )
        return  self.runstrats

    def _runonce(self, runstrat):
        print("runonce")
        if not self.lines:
            return []
        lines = self.lines
        while True:
            # 取出 下一个元素
            dts = [line.advance_peek() for line in lines]
            if any( item  is None for item in dts):
                print("end of lines")
                break;
            # 将整个数据线推进到下一个
            # for i, dti in enumerate(self.lines):
            #     lines[i].advance()
            runstrat._oncepost(dts)



    def runstrategies(self, iterstrat, predata=False):
        runstrats = list()
        for stratcls, sargs , skwargs in iterstrat:
            try:
                strat = stratcls( self.lines )
            except Exception as e:
                print( e )
                continue
            runstrats.append(strat)

        if runstrats:
            for idx, strat in enumerate(runstrats):
                strat._start()

            self._runonce( strat )

            for strat in runstrats:
                strat._stop()

