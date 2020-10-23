import schedule
import time
import datetime
import csdnblog as cb

def job1():
    print('Job1:每隔5-7分钟执行一次的任务')
    print('Job1-startTime:%s' %(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    cb.start()
    print('Job1-endTime:%s' % (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    print('------------------------------------------------------------------------')

def job2():
    print('Job2:每隔30秒执行一次，每次执行5秒')
    print('Job2-startTime:%s' % (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    time.sleep(5)
    print('Job2-endTime:%s' % (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    print('------------------------------------------------------------------------')


def job3():
    print('Job3:每隔1分钟执行一次，每次执行10秒')
    print('Job3-startTime:%s' % (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    time.sleep(10)
    print('Job3-endTime:%s' % (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    print('------------------------------------------------------------------------')


def job4():
    print('Job4:每天下午17:49执行一次，每次执行20秒')
    print('Job4-startTime:%s' % (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    time.sleep(20)
    print('Job4-endTime:%s' % (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    print('------------------------------------------------------------------------')


def job5():
    print('Job5:每隔5秒到10秒执行一次，每次执行3秒')
    print('Job5-startTime:%s' % (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    time.sleep(3)
    print('Job5-endTime:%s' % (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    print('------------------------------------------------------------------------')


if __name__ == '__main__':
#     schedule.every(10).seconds.do(job1)
#     schedule.every(30).seconds.do(job2)
#     schedule.every(1).minutes.do(job3)
#     schedule.every().day.at('17:49').do(job4)
    schedule.every(5).to(7).minutes.do(job1)
    while True:
        schedule.run_pending()