#!/usr/bin/env python

import scrollphat
import sys
import time

class scroll_text(scrollphat):
	def __init__(self):
		scrollphat.__init__(self)

	def show_offset(self):
		return self.offset


if len(sys.argv) != 2:
    print("\nusage: python simple-text-scroll.py \"message\" \npress CTRL-C to exit\n")
    sys.exit(0)

scroll_text.write_string(sys.argv[1] + "   ")

while True:
    try:
        scroll_text.scroll()
	print (scroll_text.buffer_len(), scroll_text.show_offset())
        time.sleep(0.1)
    except KeyboardInterrupt:
        scrollphat.clear()
        sys.exit(-1)
