import Fig17, Fig18_by_age, Fig19_by_sex_age, Fig20_M1_by_age
import Fig24, Fig25, Fig26, Fig27, Fig28, Fig29, Fig30
import Fig27b
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
        Fig30
    ]
    for figure in figures:
        figure.plot()
