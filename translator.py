import toml
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
const_dec1 = seq(tok(r'var'), name, val, skip(r';'))
const_expr = seq(tok(r'@{'), alt(tok(r'\+'), tok(r'-'), tok(r'\*'), tok(r'min'), tok(r'max')), name, many(num), skip(r'}'))

val = alt(num, array, obj, const_dec1, const_expr)

main = seq(alt(group(many(item)),obj), ws, mkobj)

def to_toml(src):
    s = parse(src, main)
    code = s.stack[0]
    return toml.dumps(code)
if __name__ == "__main__":
    print(42)

