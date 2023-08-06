# coding=utf-8
import smtplib
from datetime import datetime
from email.mime.text import MIMEText


class Mail_Sender:
    def send_mail_by126(self, to_list, content):
        '''
        to_list:收件人列表
        content:内容
        send_mail("content")
        '''
        sub = '===系统时间到期自动提醒==='
        mail_server = "smtp.126.com"
        mail_user = "daleloogn@126.com"
        mail_pass = "iFudan88@"
        me = mail_user + "<" + mail_user + ">"
        msg = MIMEText(content, _charset='utf-8')
        msg['Subject'] = sub
        msg['From'] = me
        msg['To'] = ";".join(to_list)
        s = smtplib.SMTP()
        s.connect(mail_server)
        s.login(mail_user, mail_pass)
        s.sendmail(me, to_list, msg.as_string())
        s.close()


class Date_Counter:

    def str_date(self, str_cont='2018-10-21'):
        if str_cont[-2].isdigit():
            split_str = str_cont[-3]
        else:
            split_str = str_cont[-2]
        [year, month, day] = str_cont.split(split_str)
        date_res = datetime(int(year), int(month), int(day))
        return date_res

    def get_days_between(self, first_datestr, second_datestr):
        first_datetime, second_datetime = self.str_date(first_datestr), self.str_date(second_datestr)
        between_days = abs((second_datetime - first_datetime).days)
        return between_days


if __name__ == '__main__':
    user_end_time = '2020-10-09'
    user_name = 'Sir'
    dc = Date_Counter()
    ms = Mail_Sender()
    # calc_days_to_send_email_for_system_alert
    now_str = datetime.now().strftime('%Y-%m-%d')
    email_contend_str = ''
    days_left = dc.get_days_between(user_end_time, now_str)
    email_contend_str += 'user %s just have a quota of %d days left' % (user_name, days_left)
    ms.send_mail_by126(['zhangxulong1009@gmail.com'], email_contend_str)
