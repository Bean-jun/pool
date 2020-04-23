import re
import time
import requests
import pymongo
from lxml import etree


class GetProxiesPool(object):
    '''获取免费代理IP'''
    def __init__(self):
        self.base_url = ['http://www.data5u.com/','http://www.66ip.cn/index.html',
                        'https://www.kuaidaili.com/free/inha/','https://www.kuaidaili.com/free/intr/',
                        'http://www.ip3366.net/',
                        ]
        self.ip = []
        self.port = []
        self.net_type = []
        self.key = []
        self.value = []
        self.new_dic = {}
        self.use_head = ''
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36',
        }
    
    def get_data5u_ip_port(self):
        '''获取http://www.data5u.com/网站中的免费IP'''
        r = requests.get(self.base_url[0],headers=self.headers)
        html = etree.HTML(r.text)
        ip = html.xpath('//*[@class="l2"]/span[1]/li/text()')
        port = html.xpath('//*[@class="l2"]/span[2]/li/text()')
        net_type = html.xpath('//*[@class="l2"]/span[4]/li/text()')
        self.ip.append(ip)
        self.port.append(port)
        self.net_type.append(net_type)
    
    def get_66ip_ip_port(self):
        '''获取http://www.66ip.cn/index.html网站中的免费IP'''
        r = requests.get(self.base_url[1],headers=self.headers)
        html = etree.HTML(r.text)
        ip = html.xpath('//*[@id="main"]//tr/td[1]/text()')[1:]
        port = html.xpath('//*[@id="main"]//tr/td[2]/text()')[1:]
        temp = len(ip)
        net_type = ['http'] * temp
        self.ip.append(ip)
        self.port.append(port)
        self.net_type.append(net_type)

    def get_kuaidaili_ip_port(self):
        '''获取https://www.kuaidaili.com/free网站中的免费IP'''
        r = requests.get(self.base_url[2],headers=self.headers)
        html = etree.HTML(r.text)
        ip_01 = html.xpath('//*[@class="table table-bordered table-striped"]//td[1]/text()')
        port_01 = html.xpath('//*[@class="table table-bordered table-striped"]//td[2]/text()')
        net_type_01 = html.xpath('//*[@class="table table-bordered table-striped"]//td[4]/text()')
        self.ip.append(ip_01)
        self.port.append(port_01)
        self.net_type.append(net_type_01)

        time.sleep(3)
        r = requests.get(self.base_url[3],headers=self.headers)
        html = etree.HTML(r.text)
        ip_02 = html.xpath('//*[@class="table table-bordered table-striped"]//td[1]/text()')
        port_02 = html.xpath('//*[@class="table table-bordered table-striped"]//td[2]/text()')
        net_type_02 = html.xpath('//*[@class="table table-bordered table-striped"]//td[4]/text()')
        self.ip.append(ip_02)
        self.port.append(port_02)
        self.net_type.append(net_type_02)

    def get_ipnet_ip_port(self):
        '''获取http://www.ip3366.net/网站中的免费IP'''
        r = requests.get(self.base_url[4],headers=self.headers)
        html = etree.HTML(r.text)
        ip = html.xpath('//*[@class="table table-bordered table-striped"]//td[1]/text()')
        port = html.xpath('//*[@class="table table-bordered table-striped"]//td[2]/text()')
        net_type = html.xpath('//*[@class="table table-bordered table-striped"]//td[4]/text()')
        self.ip.append(ip)
        self.port.append(port)
        self.net_type.append(net_type)
    
    def save_mongodb(self):
        '''获取结果存入数据库中'''
        cliect = pymongo.MongoClient('localhost', 27017)
        db = cliect['ProxyPool']
        collection = db['pool']
        for i in range(len(self.ip)):
            for j in range(len(self.ip[i])):
                temp = self.net_type[i][j] + '://' + self.ip[i][j] + ':' + self.port[i][j]
                self.value.append(temp)
                self.key.append(self.net_type[i][j])
        for index,text in enumerate(self.key):
            self.new_dic.setdefault('http',[]).append(self.value[index])
        collection.delete_many({})
        collection.insert_one(self.new_dic)
    
    def get_mongo_pool(self):
        cliect = pymongo.MongoClient('localhost', 27017)
        db = cliect['ProxyPool']
        collection = db['pool']
        pipeline = [
            { '$unwind':'$http' },
            { '$project':{'_id':0}}
        ]
        for net_dict in collection.aggregate(pipeline):
                for key,val in net_dict.items():
                    yield val

    def use_pool(self):
        head = []
        temp=[]
        t = ''
        val  = [i for i in self.get_mongo_pool()]
        pattern = re.compile('http\w?', re.I)
        for i in val:
            head.append(re.findall(pattern,i))
        for index,i in enumerate(head):
            new_list = '\'' + str(i[0]) + '\'' + ':' + '\'' +val[index] + '\''
            temp.append(new_list)
        for i in temp:
            t += i + ','
        self.use_head = '{'+ t +'}'
        return self.use_head

    def run(self):
        '''运行'''
        print('开始获取...')
        self.get_data5u_ip_port()
        self.get_66ip_ip_port()
        self.get_kuaidaili_ip_port()
        self.get_ipnet_ip_port()
        self.save_mongodb()
        print("ok!")
        return self.use_pool()

def main():
    ip_pool = GetProxiesPool()
    proxy= ip_pool.run()
    return(proxy)

if __name__ == '__main__':
    main()
