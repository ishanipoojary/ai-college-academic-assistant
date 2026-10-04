from datetime import datetime


# ============================================================
# SGPA CALCULATOR
# ============================================================

def calculate_sgpa(grades_and_credits):
    if not grades_and_credits:
        return 0.0

    total_credit_points = 0
    total_credits = 0

    for course in grades_and_credits:
        grade_point = course["grade_point"]
        credits = course["credits"]

        if grade_point < 0 or grade_point > 10:
            raise ValueError("Grade point must be between 0 and 10.")

        if credits <= 0:
            raise ValueError("Credits must be greater than 0.")

        total_credit_points += grade_point * credits
        total_credits += credits

    if total_credits == 0:
        return 0.0

    return round(total_credit_points / total_credits, 2)


# ============================================================
# GRADE → GRADE POINT
# ============================================================

def grade_to_point(grade):
    grade_points = {
        "O": 10,
        "A+": 9,
        "A": 8,
        "B+": 7,
        "B": 6,
        "C": 5,
        "P": 4,
        "F": 0,
        "AB": 0,
    }

    grade = grade.strip().upper()

    if grade not in grade_points:
        raise ValueError(f"Unknown grade: {grade}")

    return grade_points[grade]


# ============================================================
# SGPA FROM LETTER GRADES
# ============================================================

def calculate_sgpa_from_grades(courses):
    grades_and_credits = []

    for course in courses:
        grade_point = grade_to_point(course["grade"])

        grades_and_credits.append({
            "grade_point": grade_point,
            "credits": course["credits"]
        })

    return calculate_sgpa(grades_and_credits)


# ============================================================
# CGPA CALCULATOR
# ============================================================

def calculate_cgpa(sgpa_and_credits):
    if not sgpa_and_credits:
        return 0.0

    total_weighted_sgpa = 0
    total_credits = 0

    for semester in sgpa_and_credits:
        sgpa = semester["sgpa"]
        credits = semester["credits"]

        if sgpa < 0 or sgpa > 10:
            raise ValueError("SGPA must be between 0 and 10.")

        if credits <= 0:
            raise ValueError("Credits must be greater than 0.")

        total_weighted_sgpa += sgpa * credits
        total_credits += credits

    if total_credits == 0:
        return 0.0

    return round(
        total_weighted_sgpa / total_credits,
        2
    )


# ============================================================
# EXAM COUNTDOWN
# ============================================================

def calculate_days_until_exam(exam_date):
    today = datetime.now().date()

    exam = datetime.strptime(
        exam_date,
        "%Y-%m-%d"
    ).date()

    return (exam - today).days


# ============================================================
# CREATE STUDY PLAN
# ============================================================

def create_study_plan(
    subjects,
    hours_per_day,
    exam_date
):
    if not subjects:
        raise ValueError(
            "At least one subject is required."
        )

    if hours_per_day <= 0:
        raise ValueError(
            "Study hours must be greater than 0."
        )

    days_remaining = calculate_days_until_exam(
        exam_date
    )

    if days_remaining <= 0:
        raise ValueError(
            "Exam date must be in the future."
        )

    subject_count = len(subjects)

    hours_per_subject = (
        hours_per_day / subject_count
    )

    total_study_hours = (
        days_remaining * hours_per_day
    )

    plan = []

    for subject in subjects:

        plan.append({
            "subject": subject,
            "hours_per_day": round(
                hours_per_subject,
                2
            ),
            "days": days_remaining,
            "total_hours": round(
                hours_per_subject * days_remaining,
                2
            )
        })

    return {
        "exam_date": exam_date,
        "days_remaining": days_remaining,
        "hours_per_day": hours_per_day,
        "total_study_hours": round(
            total_study_hours,
            2
        ),
        "subjects": plan
    }


# ============================================================
# MODIFY STUDY PLAN
# ============================================================

def modify_study_plan(
    existing_plan,
    new_hours_per_day=None,
    new_exam_date=None,
    new_subjects=None
):
    """
    Modify an existing study plan.

    Any parameter that is not provided keeps its
    previous value.
    """

    if not existing_plan:
        raise ValueError(
            "An existing study plan is required."
        )

    subjects = (
        new_subjects
        if new_subjects is not None
        else [
            item["subject"]
            for item in existing_plan["subjects"]
        ]
    )

    hours_per_day = (
        new_hours_per_day
        if new_hours_per_day is not None
        else existing_plan["hours_per_day"]
    )

    exam_date = (
        new_exam_date
        if new_exam_date is not None
        else existing_plan["exam_date"]
    )

    return create_study_plan(
        subjects=subjects,
        hours_per_day=hours_per_day,
        exam_date=exam_date
    )


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    # SGPA
    courses = [
        {"grade": "O", "credits": 4},
        {"grade": "A", "credits": 3},
        {"grade": "B+", "credits": 3},
    ]

    print(
        "SGPA:",
        calculate_sgpa_from_grades(courses)
    )

    # CGPA
    semesters = [
        {"sgpa": 8.5, "credits": 20},
        {"sgpa": 9.0, "credits": 22},
        {"sgpa": 8.7, "credits": 21},
    ]

    print(
        "CGPA:",
        calculate_cgpa(semesters)
    )

    # Exam countdown
    print(
        "Days until exam:",
        calculate_days_until_exam(
            "2026-12-15"
        )
    )

    # Original study plan
    original_plan = create_study_plan(
        subjects=[
            "Data Communication",
            "Operating Systems",
            "Graphics",
            "ESD"
        ],
        hours_per_day=4,
        exam_date="2026-12-15"
    )

    print("\n===== ORIGINAL PLAN =====")

    for item in original_plan["subjects"]:
        print(
            f"{item['subject']}: "
            f"{item['hours_per_day']} hours/day"
        )

    # Modified study plan
    updated_plan = modify_study_plan(
        existing_plan=original_plan,
        new_hours_per_day=2
    )

    print("\n===== UPDATED PLAN =====")

    for item in updated_plan["subjects"]:
        print(
            f"{item['subject']}: "
            f"{item['hours_per_day']} hours/day"
        )