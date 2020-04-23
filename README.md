# pool

 小小爬虫代理池

 - 该代理池中的IP是通过爬虫在网络收集的免费代理；
 - 代理池中的IP都是爬取当天最最最新鲜的IP，但是任然可能存在网络超时的情况，在使用时为避免这种情况，可以只用timeout来进行处理；
 - 注意
   - 该代理池中抓取的数据存放在MongoDB数据库中，请没有安装该数据库安装一下，同时安装一下pymongo
  
  ### 使用方法

  1. 数据库的安装
  
- 在Ubuntu中安装MongoDB可以使用如下命令导入秘钥   
    ```
    sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv EA312927
    ````
- 再使用sudo apt update更新后，使用如下命令安装数据库
  ```
  sudo apt-get install -y mongodb
  ```
- 并使用如下命令安装pymongo   
  ```
  python3 -m pip install pymongo
  ```
  
2. 具体使用方法

- 导入包
  ```
  import proxy_pool
  ```
- 实例化
  ```
  proxy = proxy_pool.main()
  ```
- 在自己代码中使用
  ```
  例如：
  r = requests.get('www.baidu.com',proxies=proxy)
  ```
- 建议在使用时加入超时检测，并使用try语句

3. 检测IP是否伪装成功方法
- 使用如下代码检测
  ```
    import requests
    proxy = {} # 括号中填写找到的IP，格式为 'http':'http://xxx.xxx.xxx.xxx:xxxx'
    r = requests.get('http://httpbin.org/get',proxies=proxy)
    print(r.text)
  ```
- 运行后可以在运行结果中查看，若运行结果为你填写的IP(非本机IP)，则为代理成功。
  ```
    {
    "args": {},
    "headers": {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate",
        "Host": "httpbin.org",
        "User-Agent": "python-requests/2.23.0",
        "X-Amzn-Trace-Id": "Root=1-5ea14f1e-ed4afb8308b01f6a988c2789"
    },
    "origin": "xxx.xxx.xx.xx",
    "url": "http://httpbin.org/get"
    }
  ```
  - 上述运行结果中，origin的值非本机IP，则表明代理成功
  
4. 开始愉快玩耍吧 哈哈哈哈哈