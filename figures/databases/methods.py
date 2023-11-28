from datetime import datetime

def age(birthdate):
    today = datetime.now()
    if isinstance(birthdate, str):
        birthdate = datetime.strptime(birthdate, "%d-%m-%Y")
    age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
    return age

if __name__ == '__main__':
    print(age('10-12-2000'))
    print(age('10-12-2001'))
    print(age('10-12-2002'))
    print(age('10-12-2003'))
    print(age('10-12-2004'))
    print(age('11-04-1987'))