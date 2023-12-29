from collections import deque

from util import Graph


class Module:
    def __init__(self, name):
        self.name = name

    def on_high(self, sender):
        pass

    def on_low(self, sender):
        pass

    def send_high(self):
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
    lows = 0
    highs = 0
    pulses.append(('button', 'low', 'broadcaster'))

    while pulses:
        sender, pulse, recipient = pulses.popleft()
        # print(f'{sender} -{pulse}-> {recipient}')

        if pulse == 'low':
            lows += 1
        else:
            highs += 1

        if recipient in modules:
            if pulse == 'low':
                modules[recipient].on_low(sender)
            else:
                modules[recipient].on_high(sender)

    return lows, highs


if __name__ == '__main__':
    with open('input.txt') as file:
        pulses = deque()
        modules = {}
        graph = build_graph(file.read())
        print(graph)
        print()

        lows = highs = 0
        for i in range(1000):
            l, h = press_button()
            # print()
            lows += l
            highs += h

        print(lows * highs)