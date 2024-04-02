import statistics

import pandas as pd
import math

# # Чтение CSV файла
# df = pd.read_csv('order.csv', header=None)
#
# df1 = pd.read_csv('order.csv', header=None)
# #
# # # Фильтрация строк по промежутку дат
# # start_date = '2022-11-01'
# # end_date = '2022-12-01'
# # filtered_df = df[(df[0] >= start_date) & (df[0] <= end_date)]
# #
# # # Вывод отфильтрованных строк
# #
# # filtered_df.to_csv('november_data.csv', index=False, date_format='%Y-%m-%d %H:%M:%S')
# #
# #
# # Фильтрация строк по промежутку дат
# start_date = '2023-01-01'
# end_date = '2023-02-01'
# filtered_df = df1[(df1[0] >= start_date) & (df1[0] <= end_date)]
#
# # Вывод отфильтрованных строк
#
# filtered_df.to_csv('january_data.csv', index=False, date_format='%Y-%m-%d %H:%M:%S')


# Постройте статистические ряды количества заявок в течение часа за каждые три дня Вашего набора данных.

# Считывание данных из файла с форматом datetime и преобразование формата

december_data = pd.DataFrame()
december_data['date'] = pd.read_csv('december_data.csv')
december_data['date'] = pd.to_datetime(december_data['date'], format='%Y-%m-%d %H:%M:%S')

november_data = pd.DataFrame()
november_data['date'] = pd.read_csv('november_data.csv')
november_data['date'] = pd.to_datetime(november_data['date'], format='%Y-%m-%d %H:%M:%S')

january_data = pd.DataFrame()
january_data['date'] = pd.read_csv('january_data.csv')
january_data['date'] = pd.to_datetime(january_data['date'], format='%Y-%m-%d %H:%M:%S')

months_data = pd.concat([
    november_data, december_data, january_data
], ignore_index=True)

# Выделение дня из даты
for index, row in december_data.iterrows():
    december_data.at[index, 'day'] = december_data.at[index, 'date'].day

# Выделение часа из даты
for index, row in december_data.iterrows():
    december_data.at[index, 'hour'] = december_data.at[index, 'date'].hour

# # Разделение данных на трехдневные интервалы
# three_day_intervals = [data[(data['day'] >= start_date) & (data['day'] <= end_date)] for start_date, end_date in
#                        zip(pd.date_range(data['day'].min(), data['day'].max(), freq='3D'),
#                            pd.date_range(data['day'].min() + pd.Timedelta(days=2), data['day'].max(), freq='3D'))]
#
#
#
#
#
#
# # Построение статистических рядов для каждого тридневного интервала
# for interval_data in three_day_intervals:
#     hourly_counts = interval_data.groupby(['day', 'hour']).size().unstack(fill_value=0)
#     print(hourly_counts)

# Постройте статистический ряд количества заявок в течение дня за месяц
days = {}
for index, row in december_data.iterrows():
    if december_data.at[index, 'day'] not in days:
        days[december_data.at[index, 'day']] = 0
    days[december_data.at[index, 'day']] += 1

print('Статистический ряд количества заявок в течение дня за месяц')
print(days)

lst = list(days.values())

mean = round(sum(lst) / len(lst) / 24, 2)

variance = round(statistics.variance(lst) ** (0.5) / 24, 2)

print('mean и var для декабря', mean, variance)


def calc_days(day_num, dataframe, dict):
    for index, row in dataframe.iterrows():

        if dataframe.at[index, 'date'].weekday() == day_num:
            key = dataframe.at[index, 'date'].date().strftime('%y-%m-%d')
            if key not in dict:
                dict[key] = 0

            dict[key] += 1


def calc_weeks(dataframe, dict):
    week_ct = 0
    day = 1
    cur_day = 0
    for index, row in dataframe.iterrows():
        if dataframe.at[index, 'date'].day != cur_day:
            day += 1
        if day > 7:
            day = 1
            week_ct += 1

        if week_ct not in dict:
            dict[week_ct] = 0

        dict[week_ct] += 1

        cur_day = dataframe.at[index, 'date'].day


# Воспользуйтесь данными двух месяцев, соседних Вашему варианту. Постройте статистический ряд количества заявок в течение понедельника за три месяца
# количество в завяках/час
mondays = {}

calc_days(0, months_data, mondays)

print('Постройте статистический ряд количества заявок в течение понедельника за три месяца')
print(mondays)
lst2 = list(mondays.values())
monday_mean = round(sum(lst2) / len(lst2) / 24, 2)

monday_variance = round(statistics.variance(lst2) ** (0.5) / 24, 2)

print('mean и var для понедельников', monday_mean, monday_variance)

# Воспользуйтесь данными двух месяцев, соседних Вашему варианту. Постройте статистический ряд количества заявок в течение понедельника за три месяца
# количество в заявках/час
sundays = {}

calc_days(6, months_data, sundays)

print('Статистический ряд количества заявок в течение воскресенья за три месяца')
print(sundays)
lst3 = list(sundays.values())
sunday_mean = round(sum(lst3) / len(lst3) / 24, 2)

sunday_variance = round(statistics.variance(lst3) ** (0.5) / 24, 2)

print('mean и var для воскресений', sunday_mean, sunday_variance)

weeks = {}

calc_weeks(months_data, weeks)
print('Статистический ряд количества заявок в течение недели за три месяца')
print(weeks)
lst4 = list(weeks.values())
months_mean = round(sum(lst4) / len(lst4) / 24, 2)
months_variance = round(statistics.variance(lst4) ** (0.5) / 24, 2)
print('mean и var для каждой недели', months_mean, months_variance)

min_var = min(months_variance, sunday_variance, months_variance, variance)

print(min_var, ' заявок в час')

lamb = min_var  # заявок в час приходит
t = 0.2 # среднее время обслуживания, часов
n = 10  # кол-во каналов

u = 1 / t  # заявок в час можно обработать

p = lamb / u # интенсивность нагрузки
a = n / p
alpha = p / n
b = lamb * t
c = math.pow(math.e, b * (1 - a))
if p != n:
    B = (c - 1) / (1 - alpha)
else:
    B = 1 + b

p0 = (sum((((p ** k) / math.factorial(k)) for k in range(n))) + B * ((p ** n) / math.factorial(n))) ** -1
p_otk = ((p ** n) / (math.factorial(n))) * c * p0
print(p_otk)
Q = 1 - p_otk
lamb_eff = lamb * Q
lamb_var = p_otk * lamb
if p != n:
    D = (a - c * (a + b * (a - 1))) / (b * (a - 1) ** 2)
else:
    D = 1 + b / 2



W0 = t * (p ** n) / (math.factorial(n)) * D * p0

print("Количество необработанных заявок:", p_otk)
print("Количетсво обработанных заявок:", Q)
print("В среднем в час обрабатывается заявок:", lamb_eff)
print("Среднее время в очереди:", W0 )
