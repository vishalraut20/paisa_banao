import requests
import json
import operator
from bs4 import BeautifulSoup
from datetime import datetime
import statistics


class TopMutualFunds:

    def __init__(self):
        pass


class MoneyControl:

    def __init__(self):
        json_data = open("config.json").read()
        self.config_json = json.loads(json_data)
        self.holding_map = {}

    def get_list_of_funds(self):
        print(datetime.now())

        for url in self.config_json.get("funds_url"):
            html_data = self._get_data_from_url(url)
            funds_list = self._get_fund_list_from_html(html_data)
            self.create_holding_map(funds_list)
        # final_map = sorted(self.holding_map.items(),
        #                    key=operator.itemgetter(1),
        #                    reverse=True)
        final_map = self.holding_map
        print(final_map)
        map_file = open("../output.json", "a")
        map_file.write("\n\n")
        map_file.write(str(datetime.now()))
        # map_file.write(str(final_map))
        stocks_above_sd = self.stock_above_SD(final_map)
        # stocks_above_sd_sorted = sorted(stocks_above_sd.items(),
        #                                 key=operator.itemgetter(1),
        #                                 reverse=True)
        map_file.write(str(stocks_above_sd))
        print(datetime.now())
        # map_file.close()

    def stock_above_SD(self, stock_info_map):
        stocks_above_sd = {}
        for key in stock_info_map:
            stock_percents = stock_info_map.get(key).get("percent")
            print(stock_percents)
            sd = 1
            median = 0
            if len(stock_percents) > 1:
                sd = statistics.stdev(stock_percents)
                median = statistics.median(stock_percents)
            stocks_above_sd[key] = {"sd": sd, "count": 0, "median": median}
            stocks_above_sd.get(key)["count"] = len(stock_percents)
        stocks_above_sd = sorted(
            stocks_above_sd.items(), key=lambda x: x[1]["count"], reverse=True)
        print(stocks_above_sd)
        return stocks_above_sd

    def create_holding_map(self, funds_list):
        count = 0
        for fund in funds_list:
            fund_holding_url = self.config_json.get("holding_base_url") \
                               + "/" \
                               + fund
            holding_html = self._get_data_from_url(fund_holding_url)
            holding_list = self._get_holding_list_from_html(holding_html)
            # print(holding_list)
            self._update_holding_map(self.holding_map, holding_list)
            count += 1
            # break
        print(count)
        return self.holding_map

    def _update_holding_map(self, holding_map, holding_list):
        for holding in holding_list:
            # holding_map[holding] = holding_map[holding] + 1 if \
            #     holding_map.get(holding) else holding_map[holding] = 1
            if holding_map.get(holding.get("title")):
                share_info = holding_map.get(holding.get("title"))
                share_info["count"] = share_info.get("count") + 1
                share_info.get("percent").append(holding.get("%"))
                holding_map[holding.get("title")] = share_info
            else:
                share_info = {"count": 1, "percent": [holding.get("%")]}
                holding_map[holding.get("title")] = share_info
        return holding_map


    def _get_data_from_url(self, url_to_call):
        return requests.get(url_to_call).text

    def _get_fund_list_from_html(self, html_data):
        soup = BeautifulSoup(html_data)
        funds_table = soup.find("table", attrs={"class":"gry_t thdata"})
        funds_list = []
        for row in funds_table.find_all("tr")[1:]:
            fund_full_name = row.find(attrs={"class": "bl_12"})
            if fund_full_name and str(fund_full_name).__contains__("href"):
                fund_url = fund_full_name.get("href")
                fund_id = str(fund_url).split("/")[-1]
                funds_list.append(fund_id)
        return funds_list

    def _get_holding_list_from_html(self, holding_html):
        holding_list = []
        soup = BeautifulSoup(holding_html)
        holding_table = soup.find("table", attrs={"class": "tblporhd"})
        if not holding_table:
            return holding_list
        for row in holding_table.find_all("tr")[1:]:
            share_obj={}
            for column in row.find_all("td"):
                for a in column.find_all("a"):
                    if a and str(a).__contains__("title"):
                        share_title = a.get("title")
                        share_obj["title"] = share_title
            for column in row.find_all("td")[-1:]:
                try:
                    share_obj["%"] = float(column.get_text())
                except:
                    share_obj["%"] = float("0")
            holding_list.append(share_obj)
        return holding_list

if __name__ == "__main__":
    money_control = MoneyControl()
    money_control.get_list_of_funds()