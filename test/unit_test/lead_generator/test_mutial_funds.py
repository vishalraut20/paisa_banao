import unittest

from mock import patch

from lead_generator import mutual_funds


class TestMoneyControl(unittest.TestCase):

    def setUp(self):
        money_control = mutual_funds.MoneyControl()

    @patch.object(mutual_funds.MoneyControl, "_get_data_from_url")
    @patch.object(mutual_funds.MoneyControl, "_get_holding_list_from_html")
    @patch.object(mutual_funds.MoneyControl, "_update_holding_map")
    def test_create_holding_map(self,
                                mock_update_holding_map,
                                mock_get_holding_list_from_html,
                                mock_get_data_from_url):
        pass
