"""
测试数据主文件
created by ywp 2018-1-16
"""
import random
import string
import time
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
from .chinacitycode import CITYCODE_LIST
from .chinesename import SURNAME_LIST, FIRSTNAME_LIST
from .chinesecardbin import CARDBIN_LIST


class PersonalInfo:
    """
    个人信息
    """

    def create_phone(self):
        """
        创建手机号码
        """
        prelist = [
            "130", "131", "132", "133", "134", "135", "136", "137", "138",
            "139", "147", "150", "151", "152", "153", "155", "156", "157",
            "158", "159", "186", "187", "188", "189"
        ]
        return random.choice(prelist) + "".join(
            random.choice("0123456789") for i in range(8))

    def sur(self):
        """
        姓
        """
        return random.choice(SURNAME_LIST)

    def name(self):
        """
        名字
        """
        return random.choice(FIRSTNAME_LIST)

    def full_name(self):
        """
        姓名
        """
        sur = random.choice(SURNAME_LIST)
        name = random.choice(FIRSTNAME_LIST)
        return "{0}{1}".format(sur, name)

    def _generateCheckCode(self, idCard):
        """
        身份证最后1位，校验码
        """
        def haoma_validate(idCard):
            if type(idCard) in [str, list, tuple]:
                if len(idCard) == 17:
                    return True
            raise Exception('Wrong argument')

        if haoma_validate(idCard):
            if type(idCard) == str:
                seq = map(int, idCard)
            elif type(idCard) in [list, tuple]:
                seq = idCard

            t = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
            s = sum(map(lambda x: x[0] * x[1], zip(t, map(int, seq))))
            b = s % 11
            bd = {
                0: '1',
                1: '0',
                2: 'X',
                3: '9',
                4: '8',
                5: '7',
                6: '6',
                7: '5',
                8: '4',
                9: '3',
                10: '2'
            }
            return bd[b]

    def create_idcard(self):
        """
        身份证
        """
        cur = datetime.now()
        id = str(random.choice(CITYCODE_LIST))  #地区码
        id = id + str(random.randint(cur.year-100, cur.year-18))  #年份项
        da = date.today() + timedelta(days=random.randint(1, 366))  #月份和日期项
        id = id + da.strftime('%m%d')
        id = id + str(random.randint(100, 300))  #顺序号简单处理
        id = id + self._generateCheckCode(id)
        return id

    def create_bankcardno(self):
        """
        银行卡
        """
        return random.choice(CARDBIN_LIST) + "".join(
            random.choice("0123456789") for i in range(10))

    def fourelements(self):
        """
        四要素
        """
        return {
            "CardNo": self.create_idcard(),
            "Name": self.full_name(),
            "BankNo": self.create_bankcardno(),
            "Phone": self.create_phone()
        }


class DateTimeUtil:
    """
    封装一些常用的日期/时间
    """
    def get_sql_dt(self, days=0):
        '''
        获取当前日期时间，格式'2015-07-08 08:51:59'
        '''
        onedatetime = datetime.now() + timedelta(days=days)
        return onedatetime.strftime(r'%Y-%m-%d %H:%M:%S')

    def get_noseparators_dt(self, days=0):
        '''
        获取当前日期时间，格式'20150708085159'
        '''
        onedatetime = datetime.now() + timedelta(days=days)
        return onedatetime.strftime(r'%Y%m%d%H%M%S')

    def get_request_no(self):
        """
        获取时间流水号
        """
        requestno = self.get_noseparators_dt() + "".join(
            random.choice(string.ascii_letters) for i in range(4))
        return requestno

    def strtodate(self, datestr):
        '''
        仅限yy-mm-dd 格式
        '''
        tmp = [int(x) for x in datestr.split('-')]
        return datetime(tmp[0], tmp[1], tmp[2])

    def get_today(self):
        '''
        获取当前日期时间，格式'20170821'
        '''
        return time.strftime(r'%Y%m%d', time.localtime(time.time()))

    def get_tomorrow(self):
        '''
        获取当前日期时间，格式'20170821'
        '''
        tomorrow = datetime.now() + timedelta(days=+1)
        return tomorrow.strftime(r'%Y%m%d')

    def get_yesterday(self):
        '''
        获取当前日期时间，格式'20170821'
        '''
        yesterday = datetime.now() + timedelta(days=-1)
        return yesterday.strftime(r'%Y%m%d')

    def get_oneday(self, days):
        '''
        通过日期偏移量获取某一天，格式'2017-08-21'
        '''
        tmp = datetime.now() + timedelta(days)
        return tmp.strftime("%Y-%m-%d")

    def get_timexint(self):
        """
        获取时间戳
        """
        return str(time.time()).replace('.', '')

    def get_aftermonth(self, months):
        '''
        通过月数偏移量获取某一天，格式'2017-08-21'
        '''
        tmp = datetime.now() + relativedelta(months=months)
        return tmp.strftime("%Y-%m-%d")

    def get_day(self):
        '''
        获取今天是这个月的第几天
        '''
        return str(date.today().day)


if __name__ == '__main__':
    TMP = PersonalInfo()
    su = DateTimeUtil()
    print(su.get_sql_dt(6))
    print(TMP.fourelements())
    print(TMP.full_name())
