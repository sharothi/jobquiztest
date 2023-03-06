



from django_q.tasks import schedule
from django_q.models import Schedule

'''
def do_somthing(*agrs,**kwargs):
    print(agrs)
    
    print('hello')
    return agrs
    

schedule('quiz_app.views.do_somthing',
9,
schedule_type=Schedule.CRON,
cron = '0/2 0 * * 0-6')
'''

'''
at 9:30am on the 15th day of every month:
'30 9 15 * ?' or '30 9 15 * 0-6'


at 6pm on the last day of every month:
'0 18 L * ?' or '0 18 L * 0-6'



<minute> <hour> <day-of-month> <month> <day-of-week> 


'''

from datetime import date, timedelta

last_day_of_prev_month = date.today().replace(day=1) - timedelta(days=1)

start_day_of_prev_month = date.today().replace(day=1) - timedelta(days=last_day_of_prev_month.day)

# For printing results
print("First day of prev month:", start_day_of_prev_month)
print("Last day of prev month:", last_day_of_prev_month)




schedule('quiz_app.views.create_payment_info',
schedule_type=Schedule.CRON,
cron = '0 16 3 * 0-6')



schedule('quiz_app.views.institution_deactivation',
schedule_type=Schedule.CRON,
cron = '10 16 3 * 0-6')