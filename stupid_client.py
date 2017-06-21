import client
import itertools
from messages import GO_UP, GO_DOWN, GO_RIGHT, GO_LEFT
import time

c = client.SnakeClient(stupid=True)
c.create()

while True:
    for d in itertools.cycle([GO_UP, GO_RIGHT, GO_DOWN, GO_LEFT]):
        c._send(d)
        time.sleep(0.5)
