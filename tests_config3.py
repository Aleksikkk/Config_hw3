import unittest
from config3 import *

class TestConfigParser(unittest.TestCase):
    def test_parse_file(self):
        data = parse_file('HW3/example1_config.txt')
        self.assertEqual(data['port'], 8080)
        self.assertEqual(data['timeout'], 30)
        self.assertEqual(data['max_connections'], 100)
        self.assertEqual(data['server_name'], "example.com")
        self.assertEqual(data['array'], ["192.168.1.1", "192.168.1.2", "192.168.1.3"])
        self.assertEqual(data['table']['ip'], '"192.168.1.1",')
        self.assertEqual(data['table']['mask'], '"255.255.255.0",')
        self.assertEqual(data['table']['gateway'], "192.168.1.254")
        self.assertEqual(data['new_port'], 8081)
        self.assertEqual(data['new_timeout'], 25)
        self.assertEqual(data['new_max_connections'], 200)
        self.assertEqual(data['min_value'], 30)
        self.assertEqual(data['max_value'], 8080)

    def test_monitoring_config(self):
        data = parse_file('HW3/example2_config.txt')  

        self.assertEqual(data['monitoring_service'], "HealthCheckService")
        self.assertEqual(data['check_interval'], 5)

        self.assertEqual(data['endpoints'], ["http://localhost:8080/health", "http://localhost:8080/status"])

        self.assertEqual(data['notifications']['email'], "admin@example.com")
        self.assertEqual(data['notifications']['sms'], "1234567890")
        self.assertEqual(data['notifications']['alert_threshold'], 15)  

        self.assertEqual(data['status']['last_check'], "2023-10-01T12:00:00Z")
        self.assertEqual(data['status']['is_up'], True)
        self.assertEqual(data['status']['response_time'], 150)  

if __name__ == '__main__':
    unittest.main(exit=False)



