import json, os, shutil, json, os, datetime, hashlib
from core import withdraw



@withdraw.login   # 可以直接调用从withdraw导入的login而无需重新再写一个login函数
def transfer():
    print("----------------------------------- ICBC Bank -----------------------------------")
    transfer_comp = input('请输入转账公司:')
    price = float(input('请输入转账金额：'))
    user_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'account/alex.json')
    com_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'account/'+transfer_comp+'.json')
    user_r = open(user_path, 'r')  #
    alex_acc = json.load(user_r)
    user_r.close()
    while True:
        confirm = input(f'请确认是否向{transfer_comp}支付现金{price}购买{transfer_comp[:-5]}(y)'
                        '或取消并退出(c)')
        if confirm == 'y':
            com_r = open(com_path, 'r')  # 读tesla company文件
            com_acc = json.load(com_r)  # 储存tesla company账户数据
            com_r.close()
            alex_acc['balance'] -= price  # 储存user存款数减少的数值
            com_acc['balance'] += price * (1 - 0.05)  # 储存交易接款到company的数值，5%的手续费扣除

            # # 方法一：直接开始写入文档
            # user_w = open(user_path, 'w')  # 准备写user文件
            # com_w = open(com_path, 'w')    # 准备写company文件
            #
            # json.dump(com_acc, com_w)   # 数据储存到company数据文件
            # json.dump(alex_acc, user_w) # 数据储存到user数据文件
            # user_w.close()
            # com_w.close()

            # 方法二：暂存文档，保证写入失败时，也会有暂存文件保存数据
            user_temp_path = os.path.join(os.path.dirname(user_path), 'alex_temp.json')  # 用户暂存文件目录
            com_temp_path = os.path.join(os.path.dirname(user_path), transfer_comp+'_temp.json')  # 公司暂存文件目录
            alex_temp = open(user_temp_path, 'w')  # 使用w模式生成用户暂存文件目录
            com_temp = open(com_temp_path, 'w')  # 使用w模式生成公司暂存文件目录
            json.dump(alex_acc, alex_temp)  # 交易数据写入到用户暂存文件
            json.dump(com_acc, com_temp)  # 交易数据写入到公司暂存文件
            alex_temp.close()
            com_temp.close()
            # 复制文件
            shutil.copy(user_temp_path, user_path)  # 交易数据写入到用户正式文件
            shutil.copy(com_temp_path, com_path)  # 交易数据写入到公司正式文件
            withdraw.logs.append(f"transfer to [{transfer_comp}] with amount RMB {price}")
            print('交易完成，感谢您的使用！')
            break
        else:
            print('已手动取消交易，感谢您的使用！')
            break
    logs_file = open(withdraw.log_path, 'a')
    logs_file.writelines(' '.join(withdraw.logs) + '\n')
    logs_file.close()


transfer()




