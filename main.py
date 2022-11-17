import datetime
from time import sleep
import plotly.express as px
from matplotlib import pyplot, animation
import pandas

dicts = [
    dict(Task="A", Start=0, End=4, Time=4, Overload=False),
    dict(Task="B", Start=4, End=8, Time=4, Overload=False),
    dict(Task="B", Start=8, End=9, Time=1, Overload=True),
    dict(Task="C", Start=9, End=11, Time=2, Overload=False),
    dict(Task="B", Start=11, End=14, Time=3, Overload=False),
]
time = 0


def get_range_list(start, end, last):
    for i in range(last):
        if i <= start:
            yield start
        elif i <= end:
            yield i
        else:
            yield end

    # lst = [i if i < end else end for i in range(start, end)]
    # return lst


def get_index(i, start, end):
    if i <= start:
        return i
    elif i <= end:
        return i
    else:
        return end


def animate(i):
    global time
    default_color = 'blue'
    colors = []
    params = []
    left = list(map(lambda x: x.get('Start'), dicts))

    for dic in dicts:
        colors.append('red') if dic.get('Overload') is True else colors.append(default_color)

        if time <= dic.get('Start'):
            params.append(0)
        elif time <= dic.get('End'):
            params.append(time-dic.get('Start'))
        else:
            params.append(dic.get('Time'))

    time += 1

    pyplot.barh([dic.get('Task') for dic in dicts], params, left=left, color=colors)


def main():
    df = pandas.DataFrame(dicts)

    # project start date
    proj_start = df.Start.min()
    proj_end = df.End.max()
    # number of days from project start to task start
    df['start_num'] = df.Start - proj_start
    # number of days from project start to end of tasks
    df['end_num'] = df.End - proj_start
    # days between start and end of each task
    df['start_to_end'] = df.end_num - df.start_num

    # fig, ax = pyplot.subplots()
    # res = ax.barh(df.Task, df.start_to_end, left=df.start_num)

    # range_list = [get_range_list(0, 4, max), get_range_list(4, 8, max), get_range_list(8, 10, max)]

    fig = pyplot.figure()
    axes = fig.add_subplot()
    axes.set_xlim(0, proj_end+1)

    anim = animation.FuncAnimation(fig, animate, interval=1000)

    plot = pyplot.show()

    # fig = px.timeline(df, x_start="Start", x_end="End", y="Task")
    #
    # fig.update_traces(dict(Finish=get_date(4)), selector=dict(Task="A"))
    # sleep(1)
    #
    # fig.show()


if __name__ == '__main__':
    main()
