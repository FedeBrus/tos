import re
from htmlw import Htmlw
from node import Node

def clear_input(input):
    return re.sub('[\s+]', '', input)

def tokenize(input):
    tokens = []
    symbols = ['(', ')', '[', ']', '{', '}', ',', ';']

    i = 0
    while(i < len(input)):
        if input[i] in symbols:
            tokens.append(input[i])
            i += 1
        else:
            result = ''
            while(input[i] not in symbols):
                result += input[i]
                i += 1

            tokens.append(result)

    return tokens

def create_trees(tokens):
    current1 = Node(None, 'root', 0)
    current2 = Node(None, 'root', 0)

    i = 0
    while(i < len(tokens) and tokens[i] != ';'):

        if(tokens[i] == '('):
            current1 = current1.children[-1]

        elif(tokens[i] == ')'):
            current1 = current1.parent

        elif(tokens[i] == ','):
            pass

        elif(tokens[i] == '[' and tokens[i + 2] == ']'):
            current1.children[-1].value = int(tokens[i + 1]) if tokens[i + 1].isnumeric() else 1
            i += 2

        elif(tokens[i].isalnum()):
            if(len(current1.content) > 0):
                return None, None
            else:
                current1.children.append(Node(current1, tokens[i], 1))

        else:
            return None, None

        i += 1

    i += 1

    while(i < len(tokens) and tokens[i] != ';'):
        
        if(tokens[i] == '('):
            current2 = current2.children[-1]
        
        elif(tokens[i] == ')'):
            current2 = current2.parent
        
        elif(tokens[i] == ','):
            pass

        elif(tokens[i] == '[' and tokens[i + 2] == ']'):
            current2.children[-1].value = int(tokens[i + 1]) if tokens[i + 1].isnumeric() else 1
            i += 2

        elif(tokens[i] == '{'):
            if(len(current2.children) > 0):
                return None, None
            else:
                entry = []
                while(tokens[i] != '}'):
                    if(tokens[i].isalnum()):
                        entry.append(tokens[i])
                    i += 1
                current2.content.append(entry)
        
        elif(tokens[i].isalnum()):
            if(len(current2.content) > 0):
                return None, None
            else:
                current2.children.append(Node(current2, tokens[i], 1))

        else:
            return None, None

        i += 1

    return current1, current2

filepath = './test/test.txt'
htmlpath = './result/index.html'

with open(filepath) as f:
    content = f.read()

input = clear_input(content)
tokens = tokenize(input)
a1, a2 = create_trees(tokens)

depth1 = a1.rec_depth() if a1 is not None else 0
depth2 = a2.rec_depth() if a2 is not None else 0

h = Htmlw(htmlpath)
h.clear()
h.open_tags('html', 'head')
h.write('<link rel="stylesheet" type="text/css" href="style.css">')
h.close_tags('head')
h.open_tags('body', 'div', 'table')

# Carico subito il primo strato nella coda
queue = []
if(depth1 > 0 and len(a1.children) > 0):
    for child in a1.children:
        queue.append((child, 1))

current_depth = 0
first = True
while(len(queue) > 0):
    # Normale BFS
    current = queue.pop(0)
    for child in current[0].children:
        queue.append((child, current[1] + 1))

    # Quando c'è un cambio di profondità vengono aperti/chiusi i <tr>
    if(current[1] > current_depth):
        current_depth = current[1]
        if(current_depth > 1):
            h.close_tags('tr')
        
        if(current_depth < depth1):
            h.open_tags('tr')

    # Nel primo <tr> va inserito il pivot
    if(first and depth2 > 1):
        first = False
        h.write(f'<td class="header" colspan="{depth2 - 1}" rowspan="{depth1 - 1}"></td>')


    h.write(f'<td class="header" colspan="{a1.node_subtree_value(current[0].name)}"')     
    # I <td> foglia che non si trovano in fondo devono avere un rowspan
    if(len(current[0].children) == 0 and current[1] != depth1 - 1):
        h.write(f' rowspan="{depth1 - current[1]}"')     
    h.write(f'>{current[0].name}</td>')

h.close_tags('tr')

stack = []
if(depth2 > 1 and len(a2.children) > 0):
    for child in reversed(a2.children):
        stack.append((child, 1))
else:
    for row in a2.content:
        h.open_tags('tr')
        for entry in row:
            h.tag_content('td', entry)
        h.close_tags('tr')
    
current_depth = 0
h.open_tags('tr')
while(len(stack) > 0):
    # Normale DFS
    current = stack.pop()
    for child in reversed(current[0].children):
        stack.append((child, current[1] + 1))

    # Quando salgo di un livello devo aprire un nuovo <tr>
    if(current[1] <= current_depth):
        h.close_tags('tr')
        h.open_tags('tr')
    
    current_depth = current[1]

    h.write(f'<td class="header" rowspan="{a2.node_subtree_value(current[0].name)}"')     
    # I <td> foglia che si trovano in fondo devono avere un rowspan
    if(len(current[0].children) == 0 and current[1] != depth2 - 1):
        h.write(f' colspan="{depth2 - current[1]}"')
    h.write(f'>{current[0].name}</td>')

    if(len(current[0].children) == 0):
        if(len(current[0].content) >= 1):
            for entry in current[0].content[0]:
                h.tag_content('td', entry)
            
    # Quando il valore del nodo è diverso da 1 devo aprire un nuovo <tr>
    if(current[0].value > 1):
        for i in range(0, current[0].value - 1):
            h.close_tags('tr')
            h.open_tags('tr')
            for entry in current[0].content[i + 1]:
                h.tag_content('td', entry)

h.close_tags('tr', 'table', 'div')
h.write_file_as_is(filepath)
h.close_tags('body', 'html')