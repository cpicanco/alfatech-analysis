import os

import numpy as np
from numpy import percentile
import statsmodels.api as sm
import matplotlib.pyplot as plt

class OutputFiles:
    def __init__(self, extention='.png',
                 base_dir=os.path.abspath(__file__).rsplit("figures", 1)[0],
                 output_dir='output'):
        self.extension = extention
        self.filename = ''
        self.__base_filename = ''
        self.base_dir = base_dir
        self.__base_output_dir = os.path.join(base_dir, output_dir)
        self.directory = self.__base_output_dir

    def set_filename(self, filename):
        self.filename = filename
        self.__base_filename = filename

    def append_filename(self, appendix):
        self.filename += appendix

    def reset_filename(self):
        self.filename = self.__base_filename

    def output_path(self, filename=None):
        if filename is None:
            filename = self.filename
        return os.path.join(self.directory, filename+self.extension)

    def cd(self, folder):
        self.directory = os.path.join(self.directory, folder)

    def back(self):
        self.directory = self.__base_output_dir

opt = OutputFiles()

def statistics_from_block(block, key='percentages', exclude_outliers=False):
    data_points = block.data[key]
    if exclude_outliers:
        data_points = [d for d in data_points if d is not None and d != 54]
        students = [p.id for p, d in zip(block.data['students'], block.data[key]) if p is not None and d != 54]
    else:
        data_points = [d for d in data_points if d is not None]
        students = [p.id for p in block.data['students'] if p is not None]

    num_students = len(set(students))
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

    return bar_value, bar_std, num_students, bar_median, bar_min, bar_max

def statistics_from_blocks(blocks, key='percentages', exclude_outliers=False):
    values, stds, lengths, medians, mins, maxs = [], [], [], [], [], []
    for block in blocks:
        value, std, length, median, min_, max_ = statistics_from_block(block, key, exclude_outliers)
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

def histogram(data, data_name, xlabel='Porcentagem de acertos', ylabel='Frequência', bins=10, binwidth=10,range=None):
    fig1 = plt.figure()
    if bins is None:
        # Calculate the IQR
        iqr = np.subtract(*percentile(data, [75, 25]))
        # Calculate the bin width using Freedman-Diaconis rule
        bin_width = 2 * iqr / (len(data) ** (1/3))

        min_bin_width = 2 * np.std(data) / (len(data) ** (1/3))
        bin_width = max(bin_width, min_bin_width)
        # Calculate the number of bins
        min_ = min(data)
        max_ = max(data)
        num_bins = int((min_ - max_) / bin_width)
    else:
        num_bins = bins
        bin_width = binwidth
        if range is None:
            min_ = 0
            max_ = 100
        else:
            min_ = range[0]
            max_ = range[1]

    # Plotting the histogram
    plt.hist(data, bins=num_bins, range=(min_, max_), color='blue', alpha=0.7, width=bin_width)

    # Adding labels and title
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)

    # Display the plot
    opt.cd('histograms')
    opt.append_filename('_histogram_'+data_name)
    plt.savefig(opt.output_path().replace('\n', ' ').replace('*', '_Dif'), bbox_inches='tight')
    opt.reset_filename()
    opt.back()
    plt.close()

def histograms(data, data_names, xlabel='Porcentagem de acertos', ylabel='Frequência', bins=10, binwidth=10,range=None):
    fig, axs = plt.subplots(3, 3)
    fig.set_size_inches(12, 12)
    num_bins = bins
    bin_width = binwidth
    min_ = range[0]
    max_ = range[1]

    for i, (d, title) in enumerate(zip(data, data_names)):
        ax = axs[i//3, i%3]
        if i < 8:
            ax.set_ylim(0, 30)
        ax.set_title(title, ha='center', y=1.025)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.tick_params(axis='x', which='both', bottom=False, top=False)

        ax.hist(d, bins=num_bins, range=(min_, max_), color='blue', alpha=0.7, width=bin_width)
        # draw a vertical line for the mean
        ax.axvline(np.mean(d), color='k', linestyle='dashed', linewidth=1)

    # Adding labels and title
    axs[1, 0].set_ylabel(ylabel)
    axs[2, 1].set_xlabel(xlabel)

    # Display the plot
    opt.cd('histograms')
    opt.append_filename('_histogram_')
    plt.tight_layout()
    plt.savefig(opt.output_path().replace('\n', ' ').replace('*', '_Dif'), bbox_inches='tight')
    opt.reset_filename()
    opt.back()
    plt.close()



def output_path(filename):
    return opt.output_path(filename)