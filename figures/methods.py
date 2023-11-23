import numpy as np

def statistics_from_block(block):
    percentages = block.data['percentages']
    percentages = [p for p in percentages if p is not None]
    bar_length = len(percentages)
    if bar_length > 0:
        bar_value = np.mean(percentages)
        bar_std = np.std(percentages)
        bar_median = np.median(percentages)
        bar_min = np.min(percentages)
        bar_max = np.max(percentages)
    else:
        bar_value = np.nan
        bar_std = np.nan
        bar_median = np.nan
        bar_min = np.nan
        bar_max = np.nan

    return bar_value, bar_std, bar_length, bar_median, bar_min, bar_max

def statistics_from_blocks(blocks):
    values, stds, lengths, medians, mins, maxs = [], [], [], [], [], []
    for block in blocks:
        value, std, length, median, min_, max_ = statistics_from_block(block)
        values.append(value)
        stds.append(std)
        lengths.append(length)
        medians.append(median)
        mins.append(min_)
        maxs.append(max_)
    return values, stds, lengths, medians, mins, maxs