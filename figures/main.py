import Fig17, Fig17b, Fig17c, Fig18_by_age, Fig18_by_school_year
import Fig19_by_sex_age
import Fig17c_per_school,Fig18_by_age_per_school,Fig18_by_school_year_per_school
import Fig18_by_sex_per_school, Fig19_by_sex_age_per_school, Fig19_by_sex_school_year_per_school
import Fig20_forwarding_age_per_school
import Fig20_forwarding_school_year_per_school
import Fig20_forwarding_sex_per_school
import Fig24_m1_steps_per_school
import Fig25_m2_steps_by_school
import Fig26_m3_steps_per_school
import Fig27_m1_tests_per_school
import Fig28_m2_tests_per_school
import Fig29_m3_tests_per_school
import Fig30_frequency_deltas
import Fig18_by_sex, Fig19_by_sex_school_year, Fig20_forwarding_age
import Fig20_forwarding_school_year, Fig20_forwarding_sex
import Fig18_by_school, Fig20_forwarding_school, Fig28_m2_tests, Fig29_m3_tests
import Fig24_m1_steps,Fig25_m2_steps,Fig26_m3_steps,Fig27_m1_tests

from methods import opt

if __name__ == '__main__':
    opt.extension = '.pdf'
    figures = [
        Fig17,
        Fig17b,
        Fig17c,
        Fig18_by_age,
        Fig18_by_school_year,
        Fig18_by_school,
        Fig18_by_sex,
        Fig19_by_sex_age,
        Fig19_by_sex_school_year,
        Fig20_forwarding_age,
        Fig20_forwarding_school_year,
        Fig20_forwarding_school,
        Fig20_forwarding_sex,
        Fig24_m1_steps,
        Fig25_m2_steps,
        Fig26_m3_steps,
        Fig27_m1_tests,
        Fig28_m2_tests,
        Fig29_m3_tests,
        Fig17c_per_school,
        Fig18_by_age_per_school,
        Fig18_by_school_year_per_school,
        Fig18_by_sex_per_school,
        Fig19_by_sex_age_per_school,
        Fig19_by_sex_school_year_per_school,
        Fig20_forwarding_age_per_school,
        Fig20_forwarding_school_year_per_school,
        Fig20_forwarding_sex_per_school,
        Fig24_m1_steps_per_school,
        Fig25_m2_steps_by_school,
        Fig26_m3_steps_per_school,
        Fig27_m1_tests_per_school,
        Fig28_m2_tests_per_school,
        Fig29_m3_tests_per_school,
        # Fig30_frequency_deltas
    ]
    for figure in figures:
        figure.plot()


