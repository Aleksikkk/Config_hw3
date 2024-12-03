import toml
import sys
from peco import *

mknum = to(lambda n: float(n))
mkstr = to(lambda s: s[1:-1])
mkarr = to(lambda a: list(a))
mkobj = to(lambda o: dict(o))

#Пробелы и комментарии
ws = many(eat(r'\s+|\'.+'))
token = lambda f: memo(seq(ws, f))
tok = lambda c: token(push(eat(c)))
skip = lambda c: token(eat(c))

#Определение токенов
num = seq(tok(r'[-+]?\d+'), mknum)
name = tok(r'[a-zA-Z]+')

#Обработка массивов, словарей и значений
val = lambda s: val(s)
array = seq(skip(r'#\('), group(many(seq(val, skip(r',')))), skip(r'\)'), mkarr)
item = group(seq(name, skip(r'='), val, skip(r',')))
obj = seq(skip(r'table\(\['), group(many(item)), skip(r'\]\)'), mkobj)

#Объявление констант
const_dec1 = group(seq(skip(r'var'), name, val, skip(r';')))
const_expr = lambda s: const_expr(s)
const_expr = group(seq(skip(r'@{'), 
                       alt(tok(r'\+'), tok(r'-'), tok(r'\*'), tok(r'min'), tok(r'max')),
                       alt(num, name, const_expr), 
                       alt(num, name, const_expr), 
                       skip(r'}')))

val = alt(num, array, obj, const_expr)

main = seq(alt(group(many(alt(item, const_dec1))),obj), ws, mkobj)

def interp(env, tree):
    if isinstance(tree, tuple):
        op, left, right = tree
        left = interp(env, left)
        right = interp(env,right)
        if op == "+":
            return left + right
        if op == "-":
            return left - right
        if op == "*":
            return left * right
        if op == "min":
            return min(left, right)
        if op == "max":
            return max(left, right)
    if isinstance(tree, str):
        return interp(env, env[tree])
    if isinstance(tree, int | float):
        return tree
    return tree
        
        
def to_toml(src):
    s = parse(src, main)
    code = s.stack[0]
    for k in code:
        code[k] = interp(code, code[k])
    return toml.dumps(code)

if __name__ == "__main__":
    input = sys.argv[1]
    output = sys.argv[2]
    print(input, output)
    with open(input, "r") as file:
        content = file.read()
        a = to_toml(content)
        print(a)
    with open(output, "w") as file:
        file.write(a)
