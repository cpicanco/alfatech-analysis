from databases import ACOLE1, ACOLE2, ACOLE3
from databases.students import students
from Fig17c import bar_plot

def plot():
    schools = sorted([k for k in students.schools(True).keys()])
    for school in schools:
        ACOLE1_by_school = ACOLE1.by_school(school)
        ACOLE2_by_school = ACOLE2.by_school(school)
        ACOLE3_by_school = ACOLE3.by_school(school)
        bar_plot(ACOLE1_by_school, f'Fig17c_acole1_{school}')
        bar_plot(ACOLE2_by_school, f'Fig17c_acole2_{school}')
        bar_plot(ACOLE3_by_school, f'Fig17c_acole3_{school}')
        bar_plot(ACOLE1_by_school, f'Fig17c_acole1_boxplot_{school}', use_boxplot=True)
        bar_plot(ACOLE2_by_school, f'Fig17c_acole2_boxplot_{school}', use_boxplot=True)
        bar_plot(ACOLE3_by_school, f'Fig17c_acole3_boxplot_{school}', use_boxplot=True)

if __name__ == "__main__":
    plot()