import re


class Course:
    def __init__(self, course, name, average, assignments, grade_types):
        self.course = course
        self.name = name
        self.average = average
        self.assignments = assignments
        self.grade_types = grade_types


class Assignment:
    def __init__(self, title_of_assignment, score, date_due, date_assigned, type_of_grade, max_points, can_be_dropped,
                 total_points, weight, weighted_score, weighted_total_points, percentage):
        self.title_of_assignment = title_of_assignment
        self.score = score
        self.date_due = date_due
        self.date_assigned = date_assigned
        self.type_of_grade = type_of_grade
        self.max_points = max_points
        self.can_be_dropped = can_be_dropped
        self.total_points = total_points
        self.weight = weight
        self.weighted_score = weighted_score
        self.weighted_total_points = weighted_total_points
        self.percentage = percentage


class GradeType:
    def __init__(self, category, grade, weight):
        self.category = category
        self.grade = grade
        self.weight = weight


def get_number(local_result):
    return re.findall("\d+\.\d+", local_result)[0]


def find_name(element):
    heading = element.findAll("a", {"class": "sg-header-heading"})  # sg-header-heading"

    name_with_whitespace = re.findall(r"(?s)(?<=\>)(.*?)(?=\<\/a\>)", str(heading))[
        0]  # extracting name with lots of whitespace

    name = str(re.sub(r'\s{2,}', ' ',
                      name_with_whitespace)).lstrip()  # a lot of bullshit to extract the name, should fix with regex

    return name


def find_total_avg(element):
    # grade[total_average] = re.findall('(\d+)', str(element.findAll("span", {"class": "sg-header-heading"})))
    return re.findall('\d+\.\d+', str(element.findAll("span", {"class": "sg-header-heading sg-right"})))  # extracts avg


def get_grid(classes):
    results = re.findall(r'(?s)(?<=\<td)(.*?)(?=\<\/td\>)', str(classes))

    date_due = results[0][1:]
    date_assigned = results[1][1:]

    various_things = results[2].splitlines()
    title_of_assignment = str(re.findall(r'(?<=Classwork\: ).*', str(various_things[2]))[0]).replace("&quot;",
                                                                                                     "\"").replace(
        "&amp;", "&")
    type_of_grade = re.findall(r'(?<=Category\: ).*', str(various_things[3]))[0]
    max_points = re.findall(r'(?<=Max Points\: ).*', str(various_things[5]))[0]
    can_be_dropped = re.findall(r'(?<=Can Be Dropped\: ).*', str(various_things[6]))[
        0]  # dunno what this does, but kept it for completions sake

    score = results[4].strip()[5:].strip()  # actual grade
    total_points = get_number(results[5])
    weight = get_number(results[6])
    weighted_score = get_number(results[7])
    weighted_total_points = get_number(results[8])
    percentage = get_number(results[9])

    return Assignment(title_of_assignment, score, date_due, date_assigned, type_of_grade,
                      max_points, can_be_dropped, total_points, weight, weighted_score, weighted_total_points,
                      percentage)


def main(classes):
    courses = []
    for class_ in classes:  # like, alg2, chem, etc etc
        grid = class_.findAll("table", {"class": "sg-asp-table"})  # grid
        assignments = grid[0].findAll("tr", {"class": "sg-asp-table-data-row"})  # every assignment
        categories = grid[1].findAll("tr", {"class": "sg-asp-table-data-row"})
        grade_data = []
        for res in categories:
            dt = res.findAll("td")
            grade_data.append(GradeType(str(dt[0].string), float(dt[3].string[:-1]), float(dt[4].string)))

        full_name = find_name(class_).strip()
        course = re.findall("\w+\s-\s\d+\s", full_name)[0].strip()
        name = re.sub("\w+\s-\s\d+\s", "", full_name).strip()
        average = find_total_avg(class_)[0]
        # grades[name] = {"course": course, "name": name, "average": find_total_avg(class_)[0]}

        assignment_list = []
        # TODO: add grade weights for grade predictions
        for assignment in assignments:
            try:
                a = get_grid(assignment)
                assignment_list.append(a)
            except IndexError:  # it tries to parse the major minor and other averages, that dont match the normal logic, so it errors out, i need to fix this
                pass
        courses.append(Course(course, name, average, assignment_list, grade_data))

    return courses
