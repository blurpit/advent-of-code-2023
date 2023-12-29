import math
from collections import deque

from util import Graph


class Module:
    def __init__(self, name):
        self.name = name
        self.watch = False

    def on_high(self, sender):
        pass

    def on_low(self, sender):
        pass

    def send_high(self):
        # Watch when this module sends a high pulse and add it to the pattern
        if self.watch:
            pattern[self.name].append(presses)

        for nbr, _ in graph.get_neighbors(self.name):
            pulses.append((self.name, 'high', nbr))

    def send_low(self):
        for nbr, _ in graph.get_neighbors(self.name):
            pulses.append((self.name, 'low', nbr))

class FlipFlop(Module):
    def __init__(self, name):
        super().__init__(name)
        self.on = False

    def on_high(self, sender):
        pass

    def on_low(self, sender):
        if self.on:
            self.on = False
            self.send_low()
        else:
            self.on = True
            self.send_high()

class Conjunction(Module):
    def __init__(self, name):
        super().__init__(name)
        self.memory = {}

    def on_high(self, sender):
        self.memory[sender] = 'high'
        if self.all_high():
            self.send_low()
        else:
            self.send_high()

    def on_low(self, sender):
        self.memory[sender] = 'low'
        self.send_high()

    def all_high(self):
        return all(pulse == 'high' for pulse in self.memory.values())

class Broadcast(Module):
    def on_high(self, sender):
        self.send_high()

    def on_low(self, sender):
        self.send_low()

def build_graph(text):
    g = Graph()
    rev = Graph() # reversed graph
    for line in text.splitlines():
        name, connections = line.split(' -> ', 1)
        connections = connections.split(', ')
        if name == 'broadcaster':
            module = Broadcast(name)
        elif name[0] == '%':
            module = FlipFlop(name[1:])
        elif name[0] == '&':
            module = Conjunction(name[1:])
        else:
            raise ValueError("Oh no")

        modules[module.name] = module
        for conn in connections:
            g.add_edge(module.name, conn, 1)
            rev.add_edge(conn, module.name, 1)

    # initialize conj memories using rev
    for v in modules:
        if isinstance(modules[v], Conjunction):
            modules[v].memory = {
                mod: 'low'
                for mod, _ in rev.get_neighbors(v)
            }

    return g

def press_button():
    pulses.append(('button', 'low', 'broadcaster'))

    while pulses:
        sender, pulse, recipient = pulses.popleft()
        # print(f'{sender} -{pulse}-> {recipient}')

        if recipient in modules:
            if pulse == 'low':
                modules[recipient].on_low(sender)
            else:
                modules[recipient].on_high(sender)


if __name__ == '__main__':
    with open('input.txt') as file:
        pulses = deque()
        modules = {}
        graph = build_graph(file.read())

        # These four conjunction modules are connected to the conjunction module
        # lg which is connected to rx. Rx will recieve a low pulse when all of
        # these four send a high pulse at the same time.
        # "Watch" these four modules, every time they receive a high pulse,
        # record the number of times the button has been pressed.
        pattern = {
            'ls': [],
            'vc': [],
            'nb': [],
            'vg': []
        }
        for mod in pattern:
            modules[mod].watch = True

        # Simulate a whole bunch of presses to figure out the pattern
        presses = 0
        for i in range(20000):
            presses += 1
            press_button()

        for k, v in pattern.items():
            print(k, v)
            diffs = [v[i] - v[i-1] for i in range(1, len(v))]
            print(k, diffs) # notice that they pulse high at regular intervals
            print()

        # Each of the four modules send a high pulse every couple thousand
        # presses. How many presses it takes is given by patten[mod][0]. When
        # those numbers line up for all 4 modules, rx will get a low pulse.
        answer = math.lcm(*(
            pattern[mod][0]
            for mod in pattern
        ))
        print(answer)
