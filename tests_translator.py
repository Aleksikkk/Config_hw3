import unittest
from translator import *

class TestConfigParser(unittest.TestCase):
    def test_parse_toml(self):
        src = '''
' Это конфигурация для сетевых настроек
' Это однострочный комментарий
var = table([
    endpoints = #(6447, 145,),
    notifications = table([
        email = 123,
        sms = 1234567890,
        alertthreshold = 15,
    ]),
    status = table([
        lastcheck = 2024,
        isup = 1,
        responsetime = 150,
    ]),
]),
'''
        toml = to_toml(src)
        assert toml.strip() == """
[var]
endpoints = [ 6447.0, 145.0,]

[var.notifications]
email = 123.0
sms = 1234567890.0
alertthreshold = 15.0

[var.status]
lastcheck = 2024.0
isup = 1.0
responsetime = 150.0
""".strip()


    def test_parse(self):
        src = '''
' Это конфигурация для сетевых настроек
' Это однострочный комментарий

var x 10;
var y 20;

values = #(1, 2, 3, 4, 5,),

settings = table([
    version = 10,
]),

var = table([
    endpoints = #(6447, 145,),
    notifications = table([
        email = 123,
        sms = 1234567890,
        alertthreshold = 15,
    ]),
    status = table([
        lastcheck = 2024,
        isup = 1,
        responsetime = 150,
    ]),
]),
result = @{+ x y},

'''

        s = parse(src, main)
        data = s.stack[0]
        
        self.assertEqual(data['x'], 10)
        self.assertEqual(data['y'], 20)
        self.assertEqual(data['values'], [1, 2, 3, 4, 5])

        settings = data['settings']
        self.assertEqual(settings['version'], 10)
    
        var_data = data['var']
        self.assertEqual(var_data['endpoints'], [6447, 145])
        self.assertEqual(var_data['notifications']['email'], 123)
        self.assertEqual(var_data['notifications']['sms'], 1234567890)
        self.assertEqual(var_data['notifications']['alertthreshold'], 15)  
        self.assertEqual(var_data['status']['lastcheck'], 2024)
        self.assertEqual(var_data['status']['isup'], 1)
        self.assertEqual(var_data['status']['responsetime'], 150)

        self.assertEqual(interp(data, data["result"]), 30)

if __name__ == '__main__':
    unittest.main(exit=False)