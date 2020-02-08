import json, os, shutil, json, os, datetime, hashlib, time

log_path = os.path.dirname(os.path.dirname(__file__)) + '/logs/bank.log'  # 日志路径
logs = []  # 储存日志

def login(func):
    def inner():
        goon = input('按确认键继续，退出请按其他键！')
        if goon == '':
            n = 0  # 输入密码次数
            login_time = time.strftime('%Y%m%d  %H:%M:%S', time.localtime())  # 登入日期和时间，strftime得到的时间可以直接与字符串比较
            logs.append(login_time)  # 先将登录时间存入列表
            print('登入时间:', login_time)
            while True:
                # 账户登录信息和账户余额信息都放在/account/alex.json里
                filepath = os.path.dirname(os.path.dirname(__file__)) + '/account/alex.json'
                r_file = open(filepath, 'r')
                r_load = json.load(r_file)  # 读取json文件
                status = r_load['status']  # 读取json文件status
                expire_date = r_load['expire_date']  # 过期时间
                if status == 0 and (expire_date > login_time):  # 判断是否status=0并且没有超过时间,strftime得到的时间可以直接与字符串比较
                    account = [file[:] for root, dirs, filenames in os.walk(os.path.dirname(filepath))
                               for file in filenames if file[:] == 'alex.json'][0][:-5]  # 用户账户名————json文件的文件名
                    # account = os.path.splitext(os.path.basename(__file__))[0]  # 用户账户————当前文件名
                    logs.append(account)  # 用户名先存入logs列表
                    print('账户名：', account)
                    password = input('请输入您的密码：')  # 输入密码
                    if str(hashlib.md5(password.encode('utf-8')).hexdigest()) == r_load[
                        'password']:  # 比对密码hashlib.md5加密后的值
                        print('登陆成功!')
                        r_file.close()
                        func()  # 登录成功开始转账(transfer)或查询业务(withdraw)
                        break
                    elif password == '':
                        print('已手动退出，谢谢您的使用！')
                        break
                    elif n >= 2:
                        r_load['status'] = 1
                        w_file = open('account.json', 'w')
                        json.dump(r_load, w_file)
                        w_file.close()
                        print('密码错误3次，账户被锁定！')
                        print('交易终止，谢谢您的使用！')
                        break
                    else:
                        n += 1
                        print(f'密码输入错误{n}次，密码错误三次后将锁定账户！')
                        continue
                elif status == 1 or (expire_date < login_time):
                    print('账户已被锁定或已到期，请联系工作人员！')
                    print('交易终止，谢谢您的使用！')
                    break

        else:
            print('交易终止，谢谢您的使用！')

    return inner


@login
def withdraw():
    print("----------------------------------- ICBC Bank -----------------------------------")
    # price = 960000
    user_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'account/alex.json')
    # com_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'account/tesla_company.json')
    user_r = open(user_path, 'r')  #
    alex_acc = json.load(user_r)
    user_r.close()
    while True:
        confirm = input('请确认是否办理账户查询业务(q)，或取消(c)并退出：')
        if confirm == 'q':
            """当执行start.py时，出现交互窗口：
           ----------- ICBC Bank -----------
           1.账户提现
           2.提现
           ·选择1账户信息：显示alex的当前余额和信用额度
           ·选择2提现：提现金额应小于等于信用额度，利息为5%，提现金额为用户自定义
           ·提现代码的实现要写在withdraw.py里"""
            query = input('请选择1.账户提现；2.信用额度提现')
            if query == '1':
                # print(alex_acc['balance'], alex_acc['credit'])
                print(f"账户余额：{alex_acc['balance']}RMB，信用余额：{alex_acc['credit']}RMB")
            elif query == '2':
                withdraw_sum = input('请输入提现金额：')
                if (1.05 * float(withdraw_sum)) <= alex_acc['credit']:
                    alex_acc['credit'] -= 1.05 * float(withdraw_sum)
                    logs.append(
                        f"withdraw cash RMB{withdraw_sum}, interest is {0.05 * float(withdraw_sum)}")  # 将取款数据存入logs列表
                    user_w = open(user_path, 'w')  # 准备写user文件
                    json.dump(alex_acc, user_w)  # 数据储存到user数据文件
                    user_w.close()
                    print('交易完成，感谢您的使用！')
                    break
                else:
                    print('输入金额超过信用余额，请重新选择业务办理！')
            else:
                print('已取消查询业务，感谢您的使用！')
                break
        else:
            print('已取消查询业务，感谢您的使用！')
            break
    logs_file = open(log_path, 'a')
    logs_file.writelines(' '.join(logs) + '\n')
    logs_file.close()



withdraw()
logs = []  # 初始化日志
# logs_file = open(log_path, 'a')
# logs_file.writelines(' '.join(logs) + '\n')
