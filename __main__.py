import os
from gevent import pywsgi
from flask import Flask
from flask import jsonify
from flask import request
import time
import pymysql

text1='----------------------------------------------正在启动服务器WSGIServer----------------------------------------------------'
print("SEJsonServer - version 2.1.0")
print(text1)
app = Flask(__name__)
# 打开数据库连接
db = pymysql.connect(host='mysql.sqlpub.com',
                     port=3306,
                     user='sestudio',
                     password='96312c734e441b40',
                     database='csse_all')
# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()
@app.route('/')
def test():
    return 
@app.route('/registarclient')
def changecl():
    return '<p>SE账号注册注册成功后请记住Account的内容</p><form method="get" action="/reg"><label>用户名：<input type="text" name="n" value=""></label><br><label>密码：<input type="password" name="p" value=""><br><input type="submit" value="注册"></form>'
@app.route('/version')
def hellow():
    return '2.1.0'

@app.route("/login", methods=['POST','GET'])#  "登录服务器 传入用户名和密码"
def login():
    data = request.args.to_dict()
    #data = json.loads(data)
    account = data.get('u')
    password = data.get('p')
    print(account, password)
    # SQL 查询语句
    sql = "SELECT * FROM player WHERE account = %s" % (account)
    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 获取所有记录列表
        results = cursor.fetchall()
        for row in results:
            name = row[1]
            lname = row[2]
            userbp = row[3]
            fenghao = row[4]
            # 打印结果 401=success;402=封号;403=password errow;404=not found
        if lname == password:
            if fenghao == '0':
                return {"success": "Pass", "username": name, "id": account, "userbp": userbp}  # 判断
            else:
                return {"success": "由于违规的游戏行为，您的账号已被封停！", "username": name, "id": account, "userbp": userbp} # 判断
        else:
            return {"success": "密码错误！"}
    except:
        return {"success": "用户不存在！"}


@app.route("/reg", methods=['POST', 'GET'])
def reg():
    a = int(time.time()-1658834628)
    c = request.args.get('n')
    b = request.args.get('p')
    email=request.args.get('email')
    if c!='' and b!='':
        # SQL 插入语句
        sql = "INSERT INTO `player` (`account`, `username`, `password`, `bp`, `fenghao`, `email`) VALUES (%s, '%s', '%s', 0, 0, '%s')" %(a,c,b,email)
        try:
           cursor.execute(sql)
           db.commit()
           return {"success": "Pass", "account": a}
        except:
           # 如果发生错误则回滚
           db.rollback()
           print("插入失败")
           return {"success": "服务器错误！"}
    else:
        return {"success": "账号密码不能为空"}

@app.route('/changepassword')
def changepw():
    a = request.args.get('account')
    k = request.args.get('name')
    v = request.args.get('password')
    sql = "SELECT * FROM player WHERE account = %s" % (a)
    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 获取所有记录列表
        results = cursor.fetchall()
        for row in results:
            name = row[1]
        if name==k:
            sql = "UPDATE `player` SET password='%s' WHERE account=%s" % (v,a)
            try:
                cursor.execute(sql)
                db.commit()
                return {"success": "Pass"}
            except:
                db.rollback()
                return {"success": "用户名不存在！"}
        else:
            return {"success": "用户名错误！"}
    except:
        return {"success": "服务器错误"}
@app.route('/change')
def change():
    a = request.args.get('account')
    k = request.args.get('key')
    v = request.args.get('value')
    sql = "UPDATE `player` SET %s='%s' WHERE account=%s" % (k, v, a)
    try:
        cursor.execute(sql)
        db.commit()
        return {"success": "Pass"}
    except:
        db.rollback()
        return {"success": "Internal Server Errow"}

@app.route('/managerlogin')
def managerlogin():
    return '<p>SE后台管理</p><form method="post" action="/manager"><label>用户名：<input type="text" name="user" value=""></label><br><label>密码：<input type="password" name="password" value=""><br><input type="submit" value="登录"></form>'

@app.route('/manager', methods=['POST'])
def manager():
    u = request.form.get("user")
    p = request.form.get("password")
    if u == 'sebackpartmanager' and p == '1029831232':
        return '<p>SE后台管理</p><p>修改数据</p><form method="get" action="/change"><label>account：<input type="text" name="account" value=""></label><br><label>key：<input type="text" name="key" value=""></label><br><label>value：<input type="text" name="value" value=""><br><input type="submit" value="修改"></form><p>查询</p><form method="post" action="/find"><label>account：<input type="text" name="a" value=""></label><br><input type="submit" value="查询"></form>'
    else:
        return "<p>登陆失败，密码错误</p><a href='./managerlogin'  target='_self'>重新登陆</a>"

@app.route('/find', methods=['POST'])
def find():
    value = request.form.get('a')
    sql = "SELECT * FROM player WHERE account = '%s'" % (value)
    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 获取所有记录列表
        results = cursor.fetchall()
        for row in results:
            account = row[0]
            name = row[1]
            userbp = row[3]
            fenghao = row[4]
            return '<p>账号:%s</p><p>用户名:%s</p><p>bp:%s</p><p>封号(0:正常/1:封号):%s</p>' % (account, name, userbp, fenghao)  # 判断
    except:
        return '<p>服务器错误</p>'
server = pywsgi.WSGIServer(('192.168.1.43',8888),app)
server.serve_forever()
