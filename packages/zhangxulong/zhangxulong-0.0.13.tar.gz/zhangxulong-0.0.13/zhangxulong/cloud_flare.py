import json

import requests


class CloudFlare():
    def __init__(self, dns_name):
        self.header = {
            "X-Auth-Email": "zhangxulong1009@gmail.com",
            "X-Auth-Key": "f4363c63fbe2f189e37804cc6d4b9720c4c65",
            "Content-Type": "application/json"
        }
        self.dns_name = dns_name
        self.per_page = "100"

        self.url_get_account = "https://api.cloudflare.com/client/v4/accounts?page=1&per_page=20&direction=desc"
        self.get_account_id_name()
        self.get_zone_id()

    def get_account_id_name(self):
        r = requests.get(url=self.url_get_account, headers=self.header)
        res_dict = json.loads(r.text)
        self.account_id = res_dict['result'][0]['id']
        self.account_name = res_dict['result'][0]['name']

    def get_zone_id(self):
        url_get_zone = "https://api.cloudflare.com/client/v4/zones?name={0}&status=active&account.id={1}&account.name={2}&page=1&per_page=20&order=status&direction=desc&match=all".format(
            self.dns_name, self.account_id, self.account_name)
        r = requests.get(url=url_get_zone, headers=self.header)
        res_dict = json.loads(r.text)
        self.zone_id = res_dict['result'][0]['id']

    def add_dns_record(self, dns_item, dns_item_value):
        self.get_record_id(dns_item, dns_item_value)
        if not self.record_id:
            url_link_add_dns = 'https://api.cloudflare.com/client/v4/zones/{0}/dns_records'.format(self.zone_id)
            pay_load = {"type": "A",
                        "name": dns_item + '.' + self.dns_name,
                        "content": dns_item_value,
                        "ttl": 1,
                        "priority": 10,
                        "proxied": False}
            pay_load_json = json.dumps(pay_load, )
            requests.post(url=url_link_add_dns, headers=self.header, data=pay_load_json)
            print('add okay')
        else:
            print('exist not add')

    def del_record_id(self, dns_item, dns_item_value):
        self.get_record_id(dns_item, dns_item_value)
        url_link_del_dns = "https://api.cloudflare.com/client/v4/zones/{0}/dns_records/{1}".format(self.zone_id,
                                                                                                   self.record_id)
        r = requests.delete(url=url_link_del_dns, headers=self.header)
        print(r.text)

    def update_record_id(self, dns_item, dns_item_value, dns_item_update):
        self.get_record_id(dns_item, dns_item_value)
        url_link_update_dns = "https://api.cloudflare.com/client/v4/zones/{0}/dns_records/{1}".format(self.zone_id,
                                                                                                      self.record_id)
        pay_load = {"type": "A",
                    "name": dns_item + '.' + self.dns_name,
                    "content": dns_item_update,
                    "ttl": 1,
                    "proxied": False}
        pay_load_json = json.dumps(pay_load, )
        r = requests.put(url=url_link_update_dns, headers=self.header, data=pay_load_json)
        print(r.text)
        print('update')

    def get_record_id(self, dns_item, dns_item_value):
        url_link_lst_dns = "https://api.cloudflare.com/client/v4/zones/{0}/dns_records?type=A&name={1}&content={2}&page=1&per_page=20&order=type&direction=desc&match=all".format(
            self.zone_id, dns_item + '.' + self.dns_name, dns_item_value)
        r = requests.get(url=url_link_lst_dns, headers=self.header)
        res_dict = json.loads(r.text)
        try:
            self.record_id = res_dict['result'][0]['id']
        except:
            self.record_id = None


if __name__ == '__main__':
    dns_name = 'zhangxulong.xyz'
    item = 'zhang'
    value_list = ['1.1.1.1', '1.1.1.2']
    update = '1.1.1.1'
    cf = CloudFlare(dns_name)
    for value in value_list:
        cf.del_record_id(item, value)
    cf.add_dns_record(item, update)
