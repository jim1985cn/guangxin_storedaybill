#2024-06-12新增3个字段数据，分别是cash_in, cashReturn, memo
from flask import Flask, request, render_template, session, flash, redirect, url_for
from datetime import datetime, date, timedelta
#import json
import csv
import pathlib
import requests
import os
# import pandas as pd


app = Flask(__name__)

app.config["SECRET_KEY"] = os.urandom(24)

def sendPushBear(msg):
    send_Key="SCT93184TmF1ig2kldkMHKEtnzuIqTIfx.send";#2024/5/28号于https://sct.ftqq.com/上申请，有数量限制5条/日
    title = "明珠城业绩情况"
    url_host = "https://sctapi.ftqq.com/"
    url = url_host + send_Key
    req_type = "POST"
    data = {"title": title,
            "desp": msg}
    response = requests.post(timeout=2,
                        url= url,
                        data= data)
    # print(response.url)
    print(response.status_code)
    if response.status_code == 200 or response.status_code == 302:
        print(response.content)
        return response.content
    pass

def IsExistsRecord(aRow, num):
    lstRow = aRow[0:num]
    print(lstRow)
    bExist = False
    with open('bill.csv') as f:
        csv_reader = csv.reader(f)
        for row in csv_reader:
#                 print(row)
            d = [False for c in lstRow if c not in row]
            if not d:
                bExist = True
                break
        return bExist

def WriteDataToCSV(aRow):
    #csv 写入之前判断纪录是否存在
    if not IsExistsRecord(aRow, 1):
        #打开之前先判断文件是否已经被打开
#             if self.is_open('trainlatetime.csv'):
#                 print("文件已被打开，请关闭")
#                 sleep(10)
        #打开文件，追加a
        out = open('bill.csv','a', newline='')  
        #设定写入模式
        csv_write = csv.writer(out,dialect='excel')
        #写入具体内容
        csv_write.writerow(aRow)
        print('写入文件成功')
        # sendPushBear(','.join(aRow))
        return None
def getbilldata(date_list):
    #初始化要显示的数据
    dict_return = {}
    # yes_date = today.strftime('%Y-%m-%d')
    goal = 0
    achievement = 0
    Sum_Achievement = 0
    precent = 0
    sum_referrals = 0
    cash = 0
    #判断bill.csv文件是否存在
    path = pathlib.Path('bill.csv')
    if path.is_file():
        # print("bill.csv文件存在")
        # print(data_format)
        if IsExistsRecord(date_list,1):
            print("record is exists")
            date_str = date_list[0]
            print('date_str:{}'.format(date_str))

            with open("bill.csv", mode="r", encoding="utf-8") as file:
                reader = csv.reader(file)

                for row in reader:
                    if date_str in row:
                        print(row)
                        #提取数据
                        dict_return['yes_date'] = row[0]
                        dict_return['goal'] = row[1]
                        dict_return['achievement'] = row[2]
                        dict_return['Sum_Achievement'] = row[3]
                        dict_return['precent'] = row[4]
                        dict_return['balance'] = row[5]
                        dict_return['dayNeed'] = row[6]
                        dict_return['douyin'] = row[7]
                        dict_return['douyin_count'] = row[8]
                        dict_return['meituan'] = row[9]
                        dict_return['meituan_count'] = row[10]
                        dict_return['cash'] = row[11]
                        dict_return['expend'] = row[12]
                        dict_return['payment'] = row[13]
                        dict_return['dayReferrals'] = row[14]
                        dict_return['sum_referrals'] = row[15]
                        dict_return['cash_in'] = row[16]
                        dict_return['cash_return'] = row[17]
                        dict_return['memo'] = row[18]
            return dict_return
        else:
            return None
    
    

def Is_Firstday_month(date_str):

    # 获取当前月的第一天
    first_day_of_month = date(date_str.year, date_str.month, 1)

    # 检查当前日期是否是月的第一天
    if date_str.date() == first_day_of_month:
        return True
    else:
        return False    
        pass
#2024-06-04经认真考虑还是放弃以下功能，主要居于以下考虑：
#可能会被客户滥用此功能，造成用户体验下降，但也有改善措施，最终还是决定开放此项功能，以下是改善措施
#1、用户只能修改当天的数据
#2、对于缺失的数据可以查询添加
@app.route("/query_data", methods=['GET'])
def query_data():
        date = request.args.get('query_date')
        date_format = '%Y-%m-%d'
        date_object = datetime.strptime(date, date_format)
        print(date_object)
        prior_day = date_object - timedelta(days=1)
        priorDay_str = prior_day.strftime(date_format)
        #查询是否有前一天的数据
        data_bill = getbilldata([priorDay_str])
        print(data_bill)
        if data_bill is None:
            # priorday_str = prior_day.strftime(date_format)
            # print("prior_day:{}".format(priorday_str))
            data_bill = {'yes_date':priorDay_str,
                        'goal': 0,
                        'achievement': 0,
                        'Sum_Achievement': 0,
                        'precent': '0%',
                        'cash': 0,
                        'sum_referrals': 0} 
        #查询date当天的数据，如果有则显示，无则显示默认值
        data_bill1 = getbilldata([date])
        if data_bill1 is None:
            # 增加当月自动显示goal,Sum_Achievement,cash,sum_referrals,自动填入上一结算日数据功能2024-06-11
            month_goal = 0;
            sum_Achievement = 0;
            cash = 0;
            sum_referrals = 0;
            if not Is_Firstday_month(date_object) and data_bill['goal']!= 0:
                month_goal = data_bill['goal']
                if data_bill['Sum_Achievement']!= 0:
                    sum_Achievement = data_bill['Sum_Achievement']
                if data_bill['cash']!= 0:
                    cash = data_bill['cash']
                if data_bill['sum_referrals']!=0: 
                    sum_referrals = data_bill['sum_referrals']


            data_bill1 = {'yes_date':date,
                        'goal': month_goal,
                        'achievement': 0,
                        'Sum_Achievement': sum_Achievement,
                        'precent': '0%',
                        'balance': 0,
                        'dayNeed': 0,
                        'cash': cash,
                        'sum_referrals': sum_referrals,
                        'douyin': 0,
                        'douyin_count': 0,
                        'meituan': 0,
                        'meituan_count': 0,
                        'expend': 0,
                        'payment': 0,
                        'dayReferrals':0,
                        'cash_in': 0,
                        'cash_return': 0,
                        'memo': '',
                        } 
        return render_template('index.html', 
                                date = date,
                                pre_date = data_bill['yes_date'],
                                pre_goal = data_bill['goal'],
                                pre_achievement = data_bill['achievement'],
                                pre_sumAchievement = data_bill['Sum_Achievement'],
                                pre_pace = data_bill['precent'],
                                pre_cash = data_bill['cash'],
                                pre_sumreferrals = data_bill['sum_referrals'],

                                Yes_date=data_bill1['yes_date'],
                                goal = data_bill1['goal'],
                                Yes_Achievement=data_bill1['achievement'],
                                Sum_Achievement=data_bill1['Sum_Achievement'],
                                pace=data_bill1['precent'],
                                balance= data_bill1['balance'],
                                dayNeed= data_bill1['dayNeed'],
                                cash=data_bill1['cash'],
                                douyin=data_bill1['douyin'],
                                douyin_count=data_bill1['douyin_count'],
                                meituan=data_bill1['meituan'], 
                                meituan_count=data_bill1['meituan_count'],
                                # cash=data_bill1['cash'] ,
                                expend=data_bill1['expend'],
                                payment=data_bill1['payment'], 
                                dayreferrals=data_bill1['dayReferrals'],
                                sum_referrals=data_bill1['sum_referrals'],
                                cash_in = data_bill1['cash_in'],
                                cash_return = data_bill1['cash_return'],
                                memo = data_bill1['memo'],
                                )


@app.route("/query-next", methods=['GET', 'POST'])
def query_next():
    pass

@app.route('/process', methods=['GET', 'POST'])
def process():
    if request.method == 'POST':
        # 获取表单数据
        # print(request.form["monthtarget"])
        # date = request.args.get('param', default=None, type=str)
        # date = session.get("currentDay")
        date = request.form['day']
        goal = request.form['monthtarget']
        Achievement = request.form['dayAchievement']
        Sum_Achievement = request.form['sumAchievement']
        precent = request.form['pace']
        balance = request.form['balance']
        average = request.form['dayNeed']
        douyin = request.form['douyin']
        douyin_count = request.form["douyin_count"]
        meituan = request.form['meituan']
        meituan_count = request.form["meituan_count"]
        cash = request.form['cash']
        expend = request.form['expend']
        payment = request.form['payment']
        referrals = request.form['dayReferrals']
        sum_referrals = request.form['sumReferrals']
        cash_in = request.form['cash_in']
        cash_return = request.form['cashReturn']
        memo = request.form['memo']

        #服务器验证表单数据合法性，主要验证goal,dayachievement
        print("goal:{0};achievement:{1}".format(goal, Achievement))
        if goal=='' or goal=='0':
            flash("月目标不能为空，请输入")
            print("月目标不能为空，请输入")
            return redirect(url_for('index'))
        if Achievement=='' or Achievement=='0':
            flash("业绩不能为空，请输入")
            print("业绩不能为空，请输入")
            return redirect(url_for('index'))

    
        # 处理表单数据（例如，存储到数据库）
        # print(f"姓名: {name}, 邮箱: {email}")
        # 重定向到另一个页面或返回成功消息
        # 要写入的数据
        data_to_write = {
            "date": date,
            "goal": goal,
            "Achievement": Achievement,
            "Sum_Achievement": Sum_Achievement,
            "precent": precent,
            "balance": balance,
            "average": average,
            "douyin": douyin,
            "meituan": meituan,
            "cash": cash,
            "expend": expend,
            "payment": payment,
            "referrals": referrals,
            "sum_referrals": sum_referrals
        }
        #将数据写入到表格文件bill.csv
        try:
            #组织数据格式
            #date+goal+achievement+sum_achievement+precent+balance+average+douyin+meituan+cash+expend+payment+referrals+sum_referrals
             #bill.csv是否存在
            path = pathlib.Path('bill.csv')
            #如果文件不存在，则创建
            if not path.is_file():
                csvfile = open('bill.csv','w')
                csvfile.close()
            bExists = False
            for line in csv.reader(open('bill.csv','r')):
                if '日期' in line:
                    print('标题已存在')
                    bExists = True
                    break
            bExists = False
            if not bExists:
                sheetHeader = [
                                '日期','月目标','日完成','总共完成','完成百分比','差','每日需完成','抖音金额',
                                '抖音笔数',"美团金额",'美团笔数',"备用金","今日现金支出","今日应上缴数","今日转介绍",
                                "月累计转介绍","今日现金收入","今日找回现金数","备注",
                                ]
                WriteDataToCSV(sheetHeader)       
            #设置日期格式：2024-05-20
            data_list = [date, goal, Achievement, Sum_Achievement, precent, balance, average, douyin, douyin_count,
                            meituan, meituan_count, cash, expend, payment, referrals, sum_referrals,
                            cash_in, cash_return, memo,
                            ]
            data_format = [ 
                            # ''.join(['日期:', date]),
                            ''.join(['月目标:', goal]),
                            ''.join(['{0}号业绩:{1}'.format(date, Achievement)]),
                            ''.join(['共完成:{0},进度:{1}'.format(Sum_Achievement, precent)]),
                            # ''.join(['完成百分比:', precent]),
                            ''.join(['差:{0},每日需完成:{1}'.format(balance, average)]),
                            # ''.join(['每日需完成:', average]),
                            ''.join(['抖音:{0}/{1}副'.format(douyin, douyin_count)]),
                            # ''.join(['抖音笔数:', douyin_count]),
                            ''.join(['美团:{0}/{1}副'.format(meituan, meituan_count)]),
                            # ''.join(['美团笔数:', meituan_count]),
                            ''.join(['备用金:', cash]),
                            ''.join(['今日现金支出:{0},今日找回现金数:{1}'.format(expend, cash_return)]),
                            ''.join(['今日应上缴数:', payment]),
                            ''.join(['今日转介绍:{0},月累计转介绍:{1}'.format(referrals, sum_referrals)]),
                            # ''.join(['月累计转介绍:', sum_referrals])
                            ]
            data_str = "\n\n".join(data_format)
            print(data_str)
            # data_format = "测试微信发送"
            WriteDataToCSV(data_list)
            # 推送信息到server酱服务器转发到微信
            if sendPushBear(data_str):
                print("发送到微信成功")
        except Exception as e:
            raise e

        # 将数据写入JSON文件
        # try:
        #     with open('data_{date}.json'.format(date=date), 'w', encoding='utf-8') as f:
        #         json.dump(data_to_write, f, ensure_ascii=False, indent=4)

        # except Exception as e:
        #     raise 
    flash("收到表单数据")
    return redirect(url_for('index'))



@app.route('/', methods=['GET','POST'])
def index():

    # 显示上一日的结算单数据，无则显示0，
    #如果是本月第一日，显示，除了月目标（），其它数据显示0
    # 获取当前日期
    current_date = datetime.now()
    today = date.today()
    today_formatted = today.strftime('%Y-%m-%d')
    yesterday = today - timedelta(days=1)
    # yesterday_formatted = f"{yesterday.year}-{yesterday.month}-{yesterday.day}"
    # print('yesterday_formatted{}'.format(yesterday_formatted))
    yesterday_formatted = yesterday.strftime('%Y-%m-%d')
    print('yesterday_formatted{}'.format(yesterday_formatted))
    #从csv文件查询是否有昨天的数据
   # if Is_Firstday_month(current_date):
    yes_date = today.strftime('%Y-%m-%d')

    date_format = [yesterday_formatted]  
    data_bill = getbilldata(date_format)
    if data_bill is None:
        data_bill = {'yes_date':yesterday_formatted,
                'goal': 0,
                'achievement': 0,
                'Sum_Achievement': 0,
                'precent': '0%',
                'cash': 0,
                'sum_referrals': 0,
                'expend': 0,
                'cash_in': 0,
                'cash_return': 0,
                'memo':'',
                }    
    return render_template('index.html', 
                            date = today_formatted,
                            pre_date=data_bill['yes_date'],
                            pre_goal = data_bill['goal'],
                            pre_achievement=data_bill['achievement'],
                            pre_sumAchievement=data_bill['Sum_Achievement'],
                            pre_pace=data_bill['precent'],
                            pre_cash=data_bill['cash'],
                            # douyin = 'None',
                            pre_sumreferrals=data_bill['sum_referrals'],
                            pre_expend= data_bill['expend'],
                            pre_cashin= data_bill['cash_in'],
                            pre_cashReturn = data_bill['cash_return'],
                            pre_memo = data_bill['memo'],

                            )

if __name__ == '__main__':
    app.run(debug=True)
