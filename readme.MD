# Bank account
1.导入模块的方式有哪几种，官方不推荐哪种？
答：一个.py文件就可以作为一个模块
import xxx、
from xxx import xxx
from xxx import *（从某模块直接导入所有py文件，但不推荐，因为可能会出现py文件与变量或其他模块的py文件重名的现象）
以命名a导入b模块:import b as a

导入父目录同级兄弟目录的子py文件(如advancedFunction下的learning.py模块)：
1.使用sys.path.append("爷绝对目录")然后from 父目录的兄弟目录 import 其下的py文件：
例如 在practice_proj->buytesla->core下的withdraw要导入practice_proj->buytesla->bin下的test.py：
import sys
sys.path.append('E:/bilibili\practice_proj/buytesla')
from bin import test
**此方法不推荐，因为如果设备更换则代码需改变，所以代码需更改一下:**
import sys, os
base_name = os.path.dirname(os.path.dirname(__file__))
sys.path.append(base_name)
from bin import test
**然而，以上方法依然很繁琐，故官方不推荐这么做**，于是有如下方法**跨目录导入模块**
注意此方法要求运行路径从项目顶级目录开始运行（如下例子是在import_test/start.py运行）：
例：import_test文件夹下：import_module目录下imp.py要导入import_module的兄弟目录brother_dir下的mod.py
1.直接在imp.py写入 from brother_dir import mod
2.在import_test(imp.py的父目录的父目录)下建立一个start.py，在start.py写入 from import_module import imp

python项目需要的依赖都放在requirements.txt的文件中，
生成方法：pip freeze > requirement (freeze如何指定安装包？？)将安装包包含其版本都写入到requirement下

2.如何让你的模块可以被系统任何一个py文件导入
将py文件移动到python目录下第三方模块(site-package)的位置下，不推荐放到内置模块位置下

3.写一个用户登录验证程序，文件account.json，内容如下：
{'expire_date': "2021-01-01", "id":1234, "status":0, "pay_day": 22, "password": "abc"}
·根据用户输入的用户名&密码，找到对应的json文件，把数据加载出来验证
·用户名为json文件名，密码为password
·判断是否过期，与expire_date进行对比
·登录成功后，打印“登陆成功”，三次登录失败，status变为1，并锁定账号
(作业参照login.py)

4.把第3题用户密码进行hashlib加密处理。即：json文件里的密码保存为md5的值，然后用md5的值验进行验证账号信息是否正确
(作业参照login_hash.py)

5.最近alex买了Tesla Model S，通过转账的形式，并且支付了5%的手续费，tesla的价格为96万。账户文件为json，请用程序实现该转账行为
需求如下：
○目录结构为

├─account
│      alex.json
│      alex_temp.json
│      tesla_company.json
│      tesla_company_temp.json
│
└─bin
       start.py
        
6.对上题增加一个需求：提现。
目录结构如下：

├─account
│      alex.json
│      alex_temp.json
│      tesla_company.json
│      tesla_company_temp.json
│
├─bin
│      start.py
│
└─core
       withdraw.py
当执行start.py时，出现交互窗口：
----------- ICBC Bank -----------
1.账户提现
2.提现
·选择1账户信息：显示alex的当前余额和信用额度
·选择2提现：提现金额应小于等于信用额度，利息为5%，提现金额为用户自定义
·提现代码的实现要写在withdraw.py里
7.尝试把上一章的验证用户登录的装饰器添加到提现和转账功能上

8.对第6题的用户转账、登录和提现操作均记录日志，日志文件位置如下：

│  main.py
│  readme.MD
│
├─account
│      alex.json
│      alex_temp.json
│      tesla_company.json
│      tesla_company_temp.json
│
├─bin
│      start.py
│
├─core
│      withdraw.py
│
└─logs
        bank.log
日志格式如下：
20190502  18:34:23   alex   transfer to [tesla_company] with amount RMB95  
20190812  14:20:17   alex   withdraw cash RMB800, interest is RMB40  
20190805  22:27:43   alex   consume cash RMB600 in shop [神仙岛], interest is RMB30  

