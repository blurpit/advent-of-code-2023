def combinations(wf, bounds: dict):
    x_min, x_max = bounds['x']
    m_min, m_max = bounds['m']
    a_min, a_max = bounds['a']
    s_min, s_max = bounds['s']

    # base cases
    if (wf == 'R'
            or x_min >= x_max
            or m_min >= m_max
            or a_min >= a_max
            or s_min >= s_max):
        return 0
    elif wf == 'A':
        return ((x_max - x_min + 1)
                * (m_max - m_min + 1)
                * (a_max - a_min + 1)
                * (s_max - s_min + 1))

    comb = 0
    rules, fallback = workflows[wf]

    for rating, comp, num, send in rules:
        r_min, r_max = bounds[rating]
        new_bounds = bounds.copy()

        if comp == '<':
            # Restrict
            new_bounds[rating] = (r_min, num-1)
            bounds[rating] = (num, r_max)

        elif comp == '>':
            new_bounds[rating] = (num+1, r_max)
            bounds[rating] = (r_min, num)

        comb += combinations(send, new_bounds)

    # Add fallback with remaining bounds
    comb += combinations(fallback, bounds.copy())

    return comb

def parse_workflow(workflow):
    name, rules = workflow.split('{')
    rules = rules[:-1] # remove }
    rules = rules.split(',')
    fallback = rules.pop()
    for i in range(len(rules)): # ignore last rule (fallback)
        rule, send = rules[i].split(':')
        rating = rule[0]
        comp = rule[1]
        num = int(rule[2:])
        rules[i] = (rating, comp, num, send)
    return name, (rules, fallback)

def parse_workflows(text):
    workflows, _ = text.split('\n\n')
    workflows = workflows.splitlines()

    for i in range(len(workflows)):
        workflows[i] = parse_workflow(workflows[i])
    workflows = dict(workflows)

    return workflows

if __name__ == '__main__':
    with open('input.txt') as file:
        workflows = parse_workflows(file.read())
        bounds = {
            'x': (1, 4000),
            'm': (1, 4000),
            'a': (1, 4000),
            's': (1, 4000),
        }
        c = combinations('in', bounds)
        print(c)
