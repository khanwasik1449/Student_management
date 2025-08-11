import json


## Assignement -1 
class Person:
    def __init__(self, name, age, address):
        self.name = name
        self.age = age
        self.address = address

    def display_person_info(self):
        print("Name:", self.name)
        print("Age:", self.age)
        print("Address:", self.address)


class Student(Person):
    def __init__(self, name, age, address, student_id):
        super().__init__(name, age, address)
        self.student_id = student_id
        self.grades = {}
        self.courses = []

    def add_grade(self, subject, grade):
        self.grades[subject] = grade

    def enroll_course(self, course_obj):
        if course_obj not in self.courses:
            self.courses.append(course_obj)

    def display_student_info(self):
        print("\n--- Student Information ---")
        super().display_person_info()
        print("ID:", self.student_id)
        if self.courses:
            print("Enrolled Courses:", ", ".join(c.course_name for c in self.courses))
        else:
            print("Enrolled Courses: None")
        if self.grades:
            print("Grades:", self.grades)
        else:
            print("Grades: None")


class Course:
    def __init__(self, name, code, instructor):
        self.course_name = name
        self.course_code = code
        self.instructor = instructor
        self.students = []

    def add_student(self, student_obj):
        if student_obj not in self.students:
            self.students.append(student_obj)

    def display_course_info(self):
        print("\n--- Course Information ---")
        print("Course Name:", self.course_name)
        print("Code:", self.course_code)
        print("Instructor:", self.instructor)
        print("Enrolled Students:")
        if self.students:
            for s in self.students:
                print(f"  - {s.name} (ID: {s.student_id})")
        else:
            print("  - None")


students_dict = {}
courses_dict = {}


def add_new_student():
    name = input("Enter student's name: ")
    try:
        age = int(input("Enter student's age: "))
    except ValueError:
        print("Invalid age! Please enter a number.")
        return
    address = input("Enter address: ")
    student_id = input("Enter student ID: ")
    if student_id in students_dict:
        print("Error: A student with that ID already exists.")
        return
    s = Student(name, age, address, student_id)
    students_dict[student_id] = s
    print(f"Student '{name}' (ID: {student_id}) added successfully!")


def add_new_course():
    name = input("Enter course name: ")
    code = input("Enter course code: ")
    instructor = input("Enter instructor's name: ")
    if code in courses_dict:
        print("Error: A course with that code already exists.")
        return
    c = Course(name, code, instructor)
    courses_dict[code] = c
    print(f"Course '{name}' (Code: {code}) added successfully.")


def enroll_student_in_course():
    sid = input("Enter student ID: ")
    ccode = input("Enter course code: ")
    student_obj = students_dict.get(sid)
    course_obj = courses_dict.get(ccode)
    if not student_obj:
        print("Error: Student not found.")
        return
    if not course_obj:
        print("Error: Course not found.")
        return
    student_obj.enroll_course(course_obj)
    course_obj.add_student(student_obj)
    print(f"Student '{student_obj.name}' enrolled in '{course_obj.course_name}'.")


def add_grade_for_student():
    sid = input("Enter student ID: ")
    ccode = input("Enter course code: ")
    grade = input("Enter grade: ")
    student_obj = students_dict.get(sid)
    course_obj = courses_dict.get(ccode)
    if not student_obj:
        print("Error: Student not found.")
        return
    if not course_obj:
        print("Error: Course not found.")
        return
    if course_obj not in student_obj.courses:
        print(f"Error: Student '{student_obj.name}' is not enrolled in {course_obj.course_name}.")
        return
    student_obj.add_grade(course_obj.course_name, grade)
    print(f"Grade '{grade}' recorded for {student_obj.name} in {course_obj.course_name}.")


def display_student_details():
    sid = input("Enter student ID: ")
    student_obj = students_dict.get(sid)
    if student_obj:
        student_obj.display_student_info()
    else:
        print("Error: Student not found.")


def display_course_details():
    ccode = input("Enter course code: ")
    course_obj = courses_dict.get(ccode)
    if course_obj:
        course_obj.display_course_info()
    else:
        print("Error: Course not found.")


def save_data():
    data = {
        "students": [
            {
                "name": s.name,
                "age": s.age,
                "address": s.address,
                "student_id": s.student_id,
                "grades": s.grades,
                "courses": [c.course_code for c in s.courses]
            }
            for s in students_dict.values()
        ],
        "courses": [
            {
                "course_name": c.course_name,
                "course_code": c.course_code,
                "instructor": c.instructor,
                "students": [s.student_id for s in c.students]
            }
            for c in courses_dict.values()
        ]
    }
    try:
        with open("sms_data.json", "w") as f:
            json.dump(data, f, indent=4)
        print("Data saved successfully.")
    except IOError:
        print("Error: Could not save data.")


def load_data():
    global students_dict, courses_dict
    try:
        with open("student_data.json", "r") as f:
            data = json.load(f)
        students_dict.clear()
        courses_dict.clear()
        for s in data.get("students", []):
            student_obj = Student(s['name'], s['age'], s['address'], s['student_id'])
            student_obj.grades = s['grades']
            students_dict[student_obj.student_id] = student_obj
        for c in data.get("courses", []):
            course_obj = Course(c['course_name'], c['course_code'], c['instructor'])
            courses_dict[course_obj.course_code] = course_obj
        for s in data.get("students", []):
            student_obj = students_dict[s['student_id']]
            for ccode in s.get("courses", []):
                course_obj = courses_dict.get(ccode)
                if course_obj:
                    student_obj.enroll_course(course_obj)
                    course_obj.add_student(student_obj)
        print("Data loaded successfully.")
    except FileNotFoundError:
        print("No saved data found. Starting fresh.")
    except Exception as e:
        print(f"Error loading data: {e}")


def show_menu():
    print("\n===== Student Management Menu =====")
    print("1. Add New Student")
    print("2. Add New Course")
    print("3. Enroll Student in Course")
    print("4. Add Grade for Student")
    print("5. Display Student Details")
    print("6. Display Course Details")
    print("7. Save Data")
    print("8. Load Data")
    print("0. Exit")


def main():
    while True:
        show_menu()
        choice = input("Choose option: ").strip()
        if choice == '1':
            add_new_student()
        elif choice == '2':
            add_new_course()
        elif choice == '3':
            enroll_student_in_course()
        elif choice == '4':
            add_grade_for_student()
        elif choice == '5':
            display_student_details()
        elif choice == '6':
            display_course_details()
        elif choice == '7':
            save_data()
        elif choice == '8':
            load_data()
        elif choice == '0':
            print("Goodbye!")
            break
        else:
            print("Invalid choice, try again.")


if __name__ == "__main__":
    main()
