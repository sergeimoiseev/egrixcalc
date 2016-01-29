# -*- coding: utf-8 -*-
# from datetime import datetime, date, time
import datetime 
def calc_staj_in_days(date_of_start, date_of_finish):
    # print("input data:")
    # print(date_of_start)
    # print(date_of_finish)
    
    s = datetime.datetime.strptime(date_of_start, "%d/%m/%y")
    e = datetime.datetime.strptime(date_of_finish, "%d/%m/%y")
    res_minus_one_day = e - s
    res = res_minus_one_day.days + 1
    # print(res)
    return res

if __name__ == '__main__':
    input_start = raw_input("Vvedite datu nachala raboti v formate dd/mm/yy\n")
    input_finish = raw_input("Vvedite datu zaversheniya raboti v formate dd/mm/yy\n")
    print("Vi otrabotali:")
    res_ = calc_staj_in_days(input_start,input_finish)    
    print(res_)
    print("dney")
# calc_staj_in_days("21/01/16","22/01/16")    

# Задание: сделать выдачу ошибки, если время начала работы больше времени конца работы
# не меняя функцию calc_staj_in_days()







# t_start = 200
# t_finish = 400

# T = t_finish - t_start + 1
# print(T)
# dt = datetime.datetime.strptime("21/11/06 16:30", "%d/%m/%y %H:%M")
# print(dt)
# print(type(dt))

# import datetime
# # a = datetime.datetime.now()
# a = datetime.datetime(2016, 1, 1, 0,0,0)
# print(a)
# # datetime.datetime(2012, 8, 7, 14, 34, 14, 63000)
# b = datetime.datetime(2012, 8, 7, 0,0,0)
# # datetime.datetime(2012, 8, 7, 14, 50)
# print(b)

# c = b - a
# # datetime.timedelta(0, 945, 937000)
# print(c)
# print(c.days)
# # print(c.seconds)
# # print(c.seconds / 60)
