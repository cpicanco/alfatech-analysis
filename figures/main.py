import Fig17, Fig18_by_age, Fig19_by_sex_age, Fig20_M1_by_age
import Fig24, Fig25, Fig26, Fig27, Fig27b, Fig28, Fig29
import Fig30, Fig31, Fig32, Fig33, Fig34

from methods import opt

if __name__ == '__main__':
    opt.extension = '.pdf'
    figures = [
        # Fig17,
        # Fig18_by_age,
        # Fig19_by_sex_age,
        # Fig20_M1_by_age,
        # Fig24,
        # Fig25,
        # Fig26,
        # Fig27,
        # Fig27b,
        # Fig28,
        # Fig29,
        Fig30,
        Fig31,
        Fig32,
        Fig33,
        Fig34
    ]
    for figure in figures:
        figure.plot()
