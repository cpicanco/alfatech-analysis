from databases.students import students
from databases import ACOLE1, ACOLE2, ACOLE3, MODULE1, MODULE2, MODULE3

def update_students(dataset):
    for up_to_date_student in students:
        for block in dataset.blocks:
            for i, student in enumerate(block.data['students']):
                if student is not None:
                    if student.id == up_to_date_student.id:
                        block.data['students'][i] = up_to_date_student
    dataset.save_to_file()

data = [ACOLE1]

# students.summary()

# for dataset in data:
#     update_students(dataset)

# check if students are up to date
for dataset in data:
    schools = [s for s in dataset.schools(True).keys()]
    for school in schools:
        print(school)
        dataset.by_school(school).summary()
