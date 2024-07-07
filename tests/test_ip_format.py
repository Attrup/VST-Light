import unittest

# Import functions to test
from VSTLight.network_controller import validate_ip_format


class TestIPFormat(unittest.TestCase):
    def test_default_ip(self):
        """
        Test that the valid default IP is accepted
        """
        ip = "192.168.11.20"
        self.assertTrue(validate_ip_format(ip))

    def test_valid_ip(self):
        """
        Test that a valid IP is accepted
        """
        ip = "114.0.11.20"
        self.assertTrue(validate_ip_format(ip))

    def test_valid_ip2(self):
        """
        Test that a valid IP is accepted
        """
        ip = "10.0.0.11"
        self.assertTrue(validate_ip_format(ip))
    
    def test_valid_ip3(self):
        """
        Test that a valid IP is accepted
        """
        ip = "0.255.0.1"
        self.assertTrue(validate_ip_format(ip))

    def test_ip_with_too_high_value(self):
        """
        Test that an IP with too high subnet values is rejected
        """
        ip = "192.168.11.256"
        self.assertFalse(validate_ip_format(ip))

    def test_ip_with_invalid_subnet_value(self):
        """
        Test that an IP with incorrect subnet value is rejected
        """
        ip = "114..11.20"
        self.assertFalse(validate_ip_format(ip))

    def test_ip_with_few__subnets(self):
        """
        Test that an IP with too few subnets is rejected
        """
        ip = "10.0.11"
        self.assertFalse(validate_ip_format(ip))

    def test_ip_with_many_subnets(self):
        """
        Test that an IP with too many subnets is rejected
        """
        ip = "0.255.0.0.1"
        self.assertFalse(validate_ip_format(ip))
