import os

import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt

class OutputFiles:
    def __init__(self, extention='.png',
                 base_dir=os.path.abspath(__file__).rsplit("figures", 1)[0],
                 output_dir='output'):
        self.extension = extention
        self.base_dir = base_dir
        self.__base_output_dir = os.path.join(base_dir, output_dir)
        self.directory = self.__base_output_dir

    def output_path(self, filename):
        return os.path.join(self.directory, filename+self.extension)

    def cd(self, folder):
        self.directory = os.path.join(self.directory, folder)

    def back(self):
        self.directory = self.__base_output_dir

opt = OutputFiles()

def statistics_from_block(block, key='percentages'):
    data_points = block.data[key]
    participants = block.data['students']
    for d, p in zip(data_points, participants):
        if d is not None:
            if d > 10:
                print(p.id, d)

    data_points = [p for p in data_points if p is not None]
    bar_length = len(data_points)
    if bar_length > 0:
        bar_value = np.mean(data_points)
        bar_std = np.std(data_points)
        bar_median = np.median(data_points)
        bar_min = np.min(data_points)
        bar_max = np.max(data_points)

    else:
        if key=='percentages':
            bar_length = 1
            bar_value = 0
            bar_std = 0
            bar_median = 0
            bar_min = 0
            bar_max = 0
        else:
            bar_value = np.nan
            bar_std = np.nan
            bar_median = np.nan
            bar_min = np.nan
            bar_max = np.nan

    return bar_value, bar_std, bar_length, bar_median, bar_min, bar_max

def statistics_from_blocks(blocks, key='percentages'):
    values, stds, lengths, medians, mins, maxs = [], [], [], [], [], []
    for block in blocks:
        value, std, length, median, min_, max_ = statistics_from_block(block, key)
        values.append(value)
        stds.append(std)
        lengths.append(length)
        medians.append(median)
        mins.append(min_)
        maxs.append(max_)
    return values, stds, lengths, medians, mins, maxs

# Q-Q plot
def qq_plot(block):
    sm.qqplot(np.array([p for p in block.data['percentages'] if p is not None]), line='s')
    plt.title(opt.filename+'_'+block.to_string())
    plt.tight_layout()
    plt.savefig(opt.output_path(), bbox_inches='tight')
    plt.close()

def output_path(filename):
    return opt.output_path(filename)