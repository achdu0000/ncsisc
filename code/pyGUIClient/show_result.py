import main
import threading
import matplotlib.pyplot as plt
import numpy as np

def draw_figure(file_name):
    # 读取文件
    data = []
    with open(file_name, 'r') as file:
        for line in file:
            line = line.strip()
            if line:
                x, y, cluster = line.split(';')
                data.append((float(x), float(y), int(cluster)))
    # 提取簇的标签
    clusters = set(item[2] for item in data)
    # 创建颜色映射
    colors = plt.cm.tab20(np.linspace(0,1,len(clusters)))
    # 绘制散点图
    for item in data:
        x, y, cluster = item
        plt.scatter(x, y, c=colors[cluster])
    # 添加图例
    legend_elements = [plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=color, markersize=8) for color in colors]
    legend_labels = ['Cluster {}'.format(cluster) for cluster in clusters]
    plt.legend(legend_elements, legend_labels)

    # 显示图形
    plt.show()
    exit()

def show_result(file_name):
    thread=threading.Thread(target=draw_figure,args=(file_name,))
    thread.start()
    main.set_log(main.Main.scrolled_text, "show result OK!")
