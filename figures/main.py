import Fig17, Fig17b, Fig17c, Fig18_by_age, Fig18_by_school_year
import Fig19_by_sex_age
# import Fig27, Fig28, Fig29
import Fig24, Fig25, Fig26,  Fig27b,  Fig29b
import Fig30_m1_complete_acole_complete, Fig30_m1_complete_first_acole_incomplete, Fig30_m1_complete
import Fig31_m2_complete_acole_complete, Fig31_m2_complete_first_acole_incomplete, Fig31_m2_complete
import Fig32_m3_complete_acole_complete, Fig32_m3_complete_first_acole_incomplete, Fig32_m3_complete
import Fig33_has_first_acole_incomplete, Fig33_has_two_acoles, Fig33_has_two_complete_acoles
import Fig18_by_sex, Fig19_by_sex_school_year, Fig20_forwarding_age
import Fig20_forwarding_school_year, Fig20_forwarding_sex, Fig28b
from methods import opt

if __name__ == '__main__':
    # opt.extension = '.pdf'
    figures = [
        # Fig17,
        # Fig17b,
        # Fig17c,
        # Fig18_by_school_year,
        # Fig18_by_age,
        # Fig18_by_sex,
        # Fig19_by_sex_school_year,
        # Fig19_by_sex_age,
        # Fig20_forwarding_age,
        # Fig20_forwarding_school_year,
        # Fig20_forwarding_sex,
        # Fig24,
        # Fig25,
        # Fig26,
        # Fig27b,
        # Fig28b,
        # Fig29b,
        Fig30_m1_complete_acole_complete,
        Fig30_m1_complete_first_acole_incomplete,
        Fig30_m1_complete,
        Fig31_m2_complete_acole_complete,
        Fig31_m2_complete_first_acole_incomplete,
        Fig31_m2_complete,
        Fig32_m3_complete_acole_complete,
        Fig32_m3_complete_first_acole_incomplete,
        Fig32_m3_complete,
        Fig33_has_first_acole_incomplete,
        Fig33_has_two_acoles,
        Fig33_has_two_complete_acoles,
    ]
    for figure in figures:
        figure.plot()


