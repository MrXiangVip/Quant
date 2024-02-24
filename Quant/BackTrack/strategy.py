
class Strategy():
    def _start(self):
        self.start()

    def start(self):
        pass

    def _stop(self):
        self.stop()

    def stop(self):
        pass

    def _oncepost(self, dt):
        self.next()

    def next(self):
        pass
