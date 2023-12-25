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
        # Invalid bounds or we ended at R
        return 0
    elif wf == 'A':
        # Combinations is the number of possible combinations of numbers within
        # the bounds (ie multiply the bounds together). Add 1 because bounds
        # are inclusive.
        return ((x_max - x_min + 1)
                * (m_max - m_min + 1)
                * (a_max - a_min + 1)
                * (s_max - s_min + 1))

    comb = 0
    rules, fallback = workflows[wf]

    for rating, comp, num, send in rules:
        r_min, r_max = bounds[rating] # bounds for this rule's rating
        new_bounds = bounds.copy() # bounds where this rule passes

        if comp == '<':
            # Restrict passing bounds (new_bounds) to numbers less than num
            # Restrict failing bounds (bounds) to numbers not less than num
            new_bounds[rating] = (r_min, num-1)
            bounds[rating] = (num, r_max)

        elif comp == '>':
            # Restrict passing bounds (new_bounds) to numbers greater than num
            # Restrict failing bounds (bounds) to numbers not greater than num
            new_bounds[rating] = (num+1, r_max)
            bounds[rating] = (r_min, num)

        # Add combinations where this rule passes
        comb += combinations(send, new_bounds)

    # Add fallback combinations, where all rules fail
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
