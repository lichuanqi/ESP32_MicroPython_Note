import json
from ..utils.urequest import get


url = 'http://quan.suning.com/getSysTime.do'
res = get(url).text

j=json.loads(res)
t2_date = j['sysTime2'].split()[0] # 日期
t2_time = j['sysTime2'].split()[1] # 时间
print('internet time: %s %s'%(t2_date, t2_time))