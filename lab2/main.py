import pandas as pd
import io
import requests
import matplotlib.pyplot as plt
import openpyxl

url1 = "https://raw.githubusercontent.com/VasiaPiven/covid19_ua/master/covid19_by_settlement_dynamics.csv"
url2 = "https://raw.githubusercontent.com/VasiaPiven/covid19_ua/master/covid19_by_settlement_actual.csv"
dynamics = requests.get(url1).content
active = requests.get(url2).content
data_frame = pd.read_csv(io.StringIO(dynamics.decode('utf-8')))
data_frame_2 = pd.read_csv(io.StringIO(dynamics.decode('utf-8')))
data_frame_map = pd.read_csv(io.StringIO(active.decode('utf-8')))
data_frame.set_index('zvit_date', inplace=True)
print(data_frame)
print(data_frame_map)


def get_column_by_name(name, table):
    if name == "zvit_date":
        return table.index
    return table[name]


def show_line(first_name, second_name, table):
    col1 = get_column_by_name(first_name, table)
    col2 = get_column_by_name(second_name, table)
    plt.plot(col1, col2)
    plt.title(first_name + " - " + second_name)
    plt.ylabel(second_name)
    plt.xlabel(first_name)
    plt.xticks(rotation=90)


#
#
#
# data_frame_group_by_registration_area = data_frame.groupby(data_frame["registration_area"])[
#     ["new_susp", "new_death", "new_confirm", "new_recover"]].sum()
# print(data_frame_group_by_registration_area)


# def men_woman(city):
#     unique = set(data_frame["person_gender"])
#     dictionary = dict.fromkeys(unique, 0)
#     gender_df = data_frame
#     if city:
#         gender_df = data_frame[data_frame.registration_area == city]
#     for i in gender_df["person_gender"]:
#         dictionary[i] += 1
#     print(city + " " + dictionary)


def sick_by_city(city):
    sick = data_frame
    if city:
        sick = data_frame[data_frame.registration_area == city]
    confirm = sick["new_confirm"].sum()
    recover = sick["new_recover"].sum()
    death = sick["new_death"].sum()
    print("Кількість людей, які ше хворіють " + city + ": " + str(confirm - recover - death))


def recover_by_city(city):
    recover_df = data_frame
    if city:
        recover_df = data_frame[data_frame.registration_area == city]
    recover = recover_df["new_recover"].sum()
    print("Загальна кількість людей, які виздоровіли " + city + ": " + str(recover))


def confirm_by_city(city):
    confirm_df = data_frame
    if city:
        confirm_df = data_frame[data_frame.registration_area == city]
    confirm = confirm_df["new_confirm"].sum()
    print("Загальна кількість підтверджених на захворювання людей " + city + ": " + str(confirm))


def death_by_city(city):
    death_df = data_frame
    if city:
        death_df = data_frame[data_frame.registration_area == city]
    death = death_df["new_death"].sum()
    print("Загальна кількість людей, які померли " + city + ": " + str(death))


def show_some_graphs_on_one_picture(names):
    dd = []
    for col in names:
        dd.append(
            data_frame_2[data_frame_2.registration_area == col].groupby(data_frame_2['zvit_date']).mean().new_susp)
    plt.xlabel('Timeline')
    i = 0
    for col in dd:
        plt.plot(col.tail(20).index, col.tail(20), label=names[i])
        i += 1

    plt.xticks(rotation=90)
    plt.legend()
    plt.show()


def show_map():
    map = plt.imread('ukraine.gif')
    fig, ax = plt.subplots()
    plt.figsize = (50, 50)
    ax.scatter(data_frame_map.registration_settlement_lng, data_frame_map.registration_settlement_lat,
               s=data_frame_map.total_confirm // 50)
    ax.imshow(map, extent=[22, 40, 43, 53])
    ax.set_xlim(22, 42.5)
    ax.set_ylim(43, 53)
    plt.show()


Menu = "1.Показати карту\n2.Показати аналіз по регіону\n3.Показати порівняльний аналіз по областях\n4.Записати в excel\n5.Вихід\n"
command = 0
while command != 5:
    print(Menu)
    command = int(input("Enter value: "))
    if command == 1:
        show_map()
    elif command == 2:
        region = input("Enter region")
        # men_woman(region)
        sick_by_city(region)
        recover_by_city(region)
        confirm_by_city(region)
        death_by_city(region)
        newdf = data_frame[data_frame.registration_area == region]
        data_frame_group = newdf.groupby(newdf.index).sum()
        print(data_frame_group)
        data_frame_group = data_frame_group.head(20)
        plt.figure(figsize=(15, 10))
        plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=1, hspace=1)
        plt.subplot(3, 2, 1)
        show_line("zvit_date", "new_susp", data_frame_group)
        plt.subplot(3, 2, 2)
        show_line("zvit_date", "new_confirm", data_frame_group)
        plt.subplot(3, 2, 3)
        show_line("zvit_date", "active_confirm", data_frame_group)
        plt.subplot(3, 2, 4)
        show_line("zvit_date", "new_death", data_frame_group)
        plt.subplot(3, 2, 5)
        show_line("zvit_date", "new_recover", data_frame_group)
        plt.show()
    elif command == 3:
        regions = input("Введіть області").split()
        show_some_graphs_on_one_picture(regions)
    elif command == 4:
        data_frame_group_by_registration_area = data_frame.groupby(data_frame["registration_area"])[
            ["new_susp", "new_death", "new_confirm", "new_recover"]].sum()
        data_frame_group_by_registration_area.to_excel('lab2.xlsx', 'Sheet1')
