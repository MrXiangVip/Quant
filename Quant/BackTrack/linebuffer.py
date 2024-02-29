from collections import deque

from numpy import NAN


class LineBuffer():
    def __init__(self,data):
        # 原始数据
        self.data =data
        self.reset()

    def __getitem__(self, ago):
        return  self.array[self.idx+ago]

    def __setitem__(self, ago, value):
        self.array[self.idx+ago]=value

    def reset(self):
        #
        self.array = deque()
        # 当前在多少行
        self.idx =0
        #
        self.lencount=0


    def __len__(self):
        return self.lencount

    def forward(self, value=NAN):
        # self.idx += size
        # self.lencount += size
        self.array.append( value )

    def backwards(self, size=1, force=False):
        self.set_idx(self._idx -size, force=force)
        self.lencount -= size
        for i in range(size):
            self.array.pop()

    def advance(self, size=1):
        self.idx += size
        self.lencount += size

    def advance_peek(self):
        if self.idx < len(self.data):
            print("advance_peek", self.data.loc[self.idx])
            return  self.data.loc[self.idx]
        return  None