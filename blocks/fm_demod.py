"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
from gnuradio import gr


class blk(gr.sync_block):
    """FM-Demodulator: m[n] = gain * arg(x[n] * conj(x[n-1]))"""

    def __init__(self, gain=1.0):
        gr.sync_block.__init__(
            self,
            name='My FM Demod',
            in_sig=[np.complex64],
            out_sig=[np.float32],
        )
        self.gain = gain
        self.last = np.complex64(1.0)

    def work(self, input_items, output_items):
        x = input_items[0]
        prev = np.concatenate(([self.last], x[:-1]))
        output_items[0][:] = self.gain * np.angle(x * np.conj(prev))
        self.last = x[-1]
        return len(x)
