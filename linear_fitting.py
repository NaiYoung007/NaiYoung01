import PySimpleGUI as sg 
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import threading

sg.theme('DarkGrey4')
layout1 = [[sg.Text('这是对双变量数据进行线性拟合的程序')],
          [sg.Text('请输入自变量x的名称：'),sg.InputText(key='-XNAME-')],
          [sg.Text('请输入自变量x的单位：'),sg.InputText(key='-XUNIT-')],
          [sg.Text('请输入因变量y的名称：'),sg.InputText(key='-YNAME-')],
          [sg.Text('请输入因变量y的单位：'),sg.InputText(key='-YUNIT-')],
          [sg.Text('请输入数据(x,y)的组数：'),sg.InputText(key='-NUMBER-')],
          [sg.Button('取消'), sg.Button('提交')]
          ]

window1 = sg.Window('线性拟合程序', layout1)

while True:
    event, values = window1.read()
    if event in (None,'取消'):
        break
    elif event == '提交':
        if not values['-NUMBER-'].isdigit():
            sg.popup('请输入一个有效的整数作为数据组数！')
            continue
        x_name = values['-XNAME-']
        x_unit = values['-XUNIT-']
        y_name = values['-YNAME-']
        y_unit = values['-YUNIT-']
        number = int(values['-NUMBER-'])
        print(
        f'自变量名称是：{x_name}，单位是：{x_unit}\n'
        f'因变量名称是：{y_name}，单位是：{y_unit}\n'
        f'数据组数是：{number}'
        )
        break
        
window1.close()

layout2 = [
    [sg.Text('请输入对应数据')],
    [[[sg.Text(f'第{i}组数据：')],
     [sg.Text(f'    x{i}='),sg.InputText(key=f'-DATAX{i}-')],
     [sg.Text(f'    y{i}='),sg.InputText(key=f'-DATAY{i}-')]] for i in range(1, number + 1)],
    [sg.Button('取消'), sg.Button('提交')]]

window2 = sg.Window('线性拟合程序', layout2)

while True:
    event, values = window2.read()
    if event in (None,'取消'):
        break
    elif event == '提交':
        data_x = []
        data_y = []
        for i in range(1, number + 1):
            try:
                x_val = float(values[f'-DATAX{i}-'])
                y_val = float(values[f'-DATAY{i}-'])
                data_x.append(x_val)
                data_y.append(y_val)
            except ValueError:
                sg.popup(f'第{i}组数据输入无效，请输入数字！')
                break
        else:
            print('输入的数据如下：')
            for i in range(number):
                print(f'第{i+1}组数据：x={data_x[i]}, y={data_y[i]}')
            break

window2.close()

layout3 = [[sg.Text('线性拟合：')],
           [sg.Table(
               headings = [f'组数',f'{x_name} ({x_unit})', f'{y_name} ({y_unit})'],
               values = [[i+1,data_x[i],data_y[i]] for i in range(number)],
               key = '-TABLE-',
               auto_size_columns = True,
               display_row_numbers =False,
               justification = 'right',
               num_rows = number,
            #    alternating_row_color="#171515"
               )],
            [sg.Text(f'拟合斜率: 待计算',key='-SLOPE-')],
            [sg.Text(f'拟合函数: 待计算',key='-FUNCTION-')],
           [sg.Button('关闭'),sg.Button('开始拟合',key='-FIT-')]
           ]

def perform_fitting():
    DATA_x =np.array(data_x)
    DATA_y =np.array(data_y)

    def linear_fit(x, k, b):
        return k * x + b
        
    popt, pcov = curve_fit(linear_fit, DATA_x, DATA_y)
    slope = popt[0]

    window3.write_event_value('-FIT_DONE-', (slope, popt))

    plt.figure(figsize=(8, 6))
    plt.scatter(DATA_x, DATA_y, label='Experiment Data', color='red')
    plt.plot(DATA_x, linear_fit(DATA_x, *popt), label=f'Fit: y={slope:.4f}x+{popt[1]:.2f}', color='blue')
    plt.xlabel(f'{x_name} ({x_unit})')
    plt.ylabel(f'{y_name} ({y_unit})')
    plt.title('linear fitting', fontsize=20)
    plt.legend()
    plt.grid(True)
    plt.show()


window3 = sg.Window('线性拟合程序', layout3)

while True:
    event, values = window3.read()
    if event in (None,'关闭'):
        break
    if event == '-FIT-':
        window3['-FIT-'].update(disabled=True)  # 禁用开始拟合按钮，防止重复点击
        threading.Thread(target=perform_fitting, daemon=True).start()  # 在后台线程中执行拟合计算
    if event == '-FIT_DONE-':
        slope, popt = values['-FIT_DONE-']
        window3['-SLOPE-'].update(f'拟合斜率: {slope:.4f}')
        window3['-FUNCTION-'].update(f'拟合函数: y={slope:.4f}x+{popt[1]:.2f}')     

window3.close()

