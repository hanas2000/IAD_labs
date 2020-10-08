import matplotlib.pyplot as plt


def show_line(name, table):
    plt.plot(table.index, table[name])
    plt.title(name)
    plt.ylabel(name)
    plt.xlabel('Data')


def show_bar(name, table):
    data = table[name]
    plt.bar(data.index, data)
    plt.title(name)
    plt.xlabel("Data")
    plt.ylabel(name)


def show_pie(name, table):
    unique = set(table[name])
    dictionary = dict.fromkeys(unique, 0)
    for i in table[name]:
        dictionary[i] += 1
    fig1, ax1 = plt.subplots()
    ax1.pie(dictionary.values(), labels=dictionary.keys(), autopct='%1.1f%%',
            shadow=True, startangle=90)
    ax1.axis('equal')
    plt.title(name)


def show_box_plot(name, data_frame):
    data = data_frame[name]
    plt.title(name)
    plt.ylabel(name)
    plt.xlabel('Data')
    plt.boxplot(data)


def show_scatter(name, data_frame):
    x = data_frame.index
    y = data_frame[name]
    plt.title(name)
    plt.ylabel(name)
    plt.xlabel("Date")
    plt.scatter(x, y)


def show_hist(name, data_frame):
    x = data_frame[name]
    plt.title(name)
    plt.ylabel('Count')
    plt.xlabel(name)
    plt.hist(x, density=False, bins=30)


def show_graphics_by_name_and_type(name, type_graph, data_frame):
    if type_graph == "Line":
        show_line(name, data_frame)
    if type_graph == "Bar":
        show_bar(name, data_frame)
    if type_graph == "Pie":
        show_pie(name, data_frame)
    if type_graph == "BoxPlot":
        show_box_plot(name, data_frame)
    if type_graph == "Scatter":
        show_scatter(name, data_frame)
    if type_graph == "Hist":
        show_hist(name, data_frame)


def show_graphics_by_name(name, data_frame):
    if str(data_frame[name].dtype) == "int64" or str(data_frame[name].dtype) == "float64":
        show_bar(name, data_frame)
        show_pie(name, data_frame)
    if str(data_frame[name].dtype) == "object":
        show_pie(name, data_frame)

