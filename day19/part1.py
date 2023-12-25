def get_next(part, workflow):
    rules, fallback = workflow
    for rating, comp, num, send in rules:
        value = part[rating]
        if comp == '>' and value > num or comp == '<' and value < num:
            return send
    return fallback

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

def parse_part(part):
    part = part[1:-1] # remove { and }
    ratings = {}
    for rating in part.split(','):
        name, num = rating.split('=')
        ratings[name] = int(num)
    return ratings

def parse_input(text):
    workflows, parts = text.split('\n\n')
    workflows = workflows.splitlines()
    parts = parts.splitlines()

    for i in range(len(workflows)):
        workflows[i] = parse_workflow(workflows[i])
    workflows = dict(workflows)

    for i in range(len(parts)):
        parts[i] = parse_part(parts[i])
    return workflows, parts

if __name__ == '__main__':
    with open('input.txt') as file:
        workflows, parts = parse_input(file.read())

        answer = 0
        for part in parts:
            wf = 'in'
            while wf not in ('A', 'R'):
                wf = get_next(part, workflows[wf])
            if wf == 'A':
                answer += sum(part.values())
        print(answer)
