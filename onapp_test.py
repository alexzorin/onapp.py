import unittest
import os
import re

import onapp


class TestOnApp(unittest.TestCase):
    def setUp(self):
        self.client = onapp.OnAppConnection(os.getenv("ONAPP_HOST", "localhost"),
                                            os.getenv("ONAPP_USER", "admin@example.org"),
                                            os.getenv("ONAPP_API_KEY", "abc123"))

    def test_getversion(self):
        self.assertIsNotNone(re.match('[\d\.]+', self.client.getversion()))

    def test_virtualmachines_list(self):
        vms = onapp.OnAppVirtualMachines(self.client)
        l = vms.list(limit=1, page=1)

        self.assertTrue(len(l) == 1)
        self.assertIsNotNone(l[0]['virtual_machine'])

if __name__ == '__main__':
    unittest.main()
