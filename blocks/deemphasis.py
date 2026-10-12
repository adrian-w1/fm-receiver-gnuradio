"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
from scipy.signal import lfilter
from gnuradio import gr


class blk(gr.sync_block):
    """De-Emphasis: y[n] = alpha*x[n] + (1-alpha)*y[n-1]"""

    def __init__(self, fs=48000.0, tau=50e-6):
        gr.sync_block.__init__(self, name='My Deemphasis',
                               in_sig=[np.float32], out_sig=[np.float32])
        alpha = 1.0 - np.exp(-1.0 / (fs * tau))
        self.b = [alpha]
        self.a = [1.0, -(1.0 - alpha)]
        self.zi = np.zeros(1)

    def work(self, input_items, output_items):
        y, self.zi = lfilter(self.b, self.a, input_items[0], zi=self.zi)
        output_items[0][:] = y
        return len(y)

