"""
Django management command to seed the Neo4j database.
Run: python manage.py seed
"""
import random
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from neo4j import GraphDatabase
from django.conf import settings

class Command(BaseCommand):
    help = 'Seed the Neo4j database with realistic data'

    def handle(self, *args, **options):
        self.stdout.write("Starting seed...")
        uri = settings.NEO4J_URI
        user = settings.NEO4J_USER
        password = settings.NEO4J_PASSWORD
        database = settings.NEO4J_DATABASE

        if not uri or not password:
            self.stderr.write("Neo4j credentials not set. Please set NEO4J_URI and NEO4J_PASSWORD in .env.")
            return

        driver = GraphDatabase.driver(uri, auth=(user, password))

        # ---------- Data Sets (same as before) ----------
        STUDENTS = [
            {'name': 'Alice Johnson', 'email': 'alice@example.com', 'enrolled_since': '2024-01-15'},
            {'name': 'Bob Smith', 'email': 'bob@example.com', 'enrolled_since': '2024-02-01'},
            {'name': 'Carol White', 'email': 'carol@example.com', 'enrolled_since': '2024-03-10'},
            {'name': 'David Brown', 'email': 'david@example.com', 'enrolled_since': '2024-04-20'},
            {'name': 'Eva Green', 'email': 'eva@example.com', 'enrolled_since': '2024-05-05'},
            {'name': 'Frank Taylor', 'email': 'frank@example.com', 'enrolled_since': '2024-06-12'},
            {'name': 'Grace Lee', 'email': 'grace@example.com', 'enrolled_since': '2024-07-01'},
            {'name': 'Henry Kim', 'email': 'henry@example.com', 'enrolled_since': '2024-08-15'},
            {'name': 'Isabel Martinez', 'email': 'isabel@example.com', 'enrolled_since': '2024-09-10'},
            {'name': 'Jack Wilson', 'email': 'jack@example.com', 'enrolled_since': '2024-10-01'},
        ]

        INSTRUCTORS = [
            {'name': 'Dr. Emily Davis', 'email': 'emily@university.edu'},
            {'name': 'Prof. John Doe', 'email': 'john@university.edu'},
            {'name': 'Prof. Sarah Connor', 'email': 'sarah@university.edu'},
            {'name': 'Dr. Michael Chen', 'email': 'michael@university.edu'},
            {'name': 'Prof. Lisa Park', 'email': 'lisa@university.edu'},
        ]

        SKILLS = [
            {'name': 'Python', 'category': 'Programming'},
            {'name': 'JavaScript', 'category': 'Programming'},
            {'name': 'Java', 'category': 'Programming'},
            {'name': 'SQL', 'category': 'Data'},
            {'name': 'Machine Learning', 'category': 'Data Science'},
            {'name': 'Deep Learning', 'category': 'Data Science'},
            {'name': 'Statistics', 'category': 'Math'},
            {'name': 'Calculus', 'category': 'Math'},
            {'name': 'Linear Algebra', 'category': 'Math'},
            {'name': 'UI/UX Design', 'category': 'Design'},
            {'name': 'Graphic Design', 'category': 'Design'},
            {'name': 'React', 'category': 'Programming'},
            {'name': 'Django', 'category': 'Programming'},
            {'name': 'Flask', 'category': 'Programming'},
            {'name': 'Docker', 'category': 'DevOps'},
            {'name': 'Git', 'category': 'DevOps'},
            {'name': 'Linux', 'category': 'DevOps'},
            {'name': 'R', 'category': 'Data Science'},
            {'name': 'Tableau', 'category': 'Data Visualization'},
            {'name': 'NLP', 'category': 'Data Science'},
        ]
        SKILLS.append({'name': 'HTML/CSS', 'category': 'Programming'})

        COURSES = [
            {'title': 'Intro to Python', 'description': 'Learn Python basics', 'level': 'Beginner', 'credits': 3},
            {'title': 'Web Development with JavaScript', 'description': 'Front-end and back-end with JS', 'level': 'Intermediate', 'credits': 4},
            {'title': 'Data Science Fundamentals', 'description': 'Intro to data science and analytics', 'level': 'Intermediate', 'credits': 4},
            {'title': 'Machine Learning A-Z', 'description': 'Comprehensive ML course', 'level': 'Advanced', 'credits': 5},
            {'title': 'Advanced Deep Learning', 'description': 'Deep learning architectures', 'level': 'Advanced', 'credits': 5},
            {'title': 'Linear Algebra for Data Science', 'description': 'Math foundations', 'level': 'Intermediate', 'credits': 3},
            {'title': 'UI/UX Design Principles', 'description': 'Design thinking and prototyping', 'level': 'Beginner', 'credits': 3},
            {'title': 'React for Beginners', 'description': 'Modern front-end with React', 'level': 'Intermediate', 'credits': 4},
            {'title': 'Django Web Framework', 'description': 'Full-stack with Django', 'level': 'Intermediate', 'credits': 4},
            {'title': 'DevOps with Docker and Kubernetes', 'description': 'Containerization and orchestration', 'level': 'Advanced', 'credits': 5},
            {'title': 'Data Visualization with Tableau', 'description': 'Visual analytics', 'level': 'Beginner', 'credits': 3},
            {'title': 'Natural Language Processing', 'description': 'NLP techniques and applications', 'level': 'Advanced', 'credits': 5},
            {'title': 'Java Programming', 'description': 'Object-oriented programming in Java', 'level': 'Beginner', 'credits': 3},
            {'title': 'Statistical Methods', 'description': 'Statistical inference and analysis', 'level': 'Intermediate', 'credits': 4},
            {'title': 'Git and Version Control', 'description': 'Collaborative development with Git', 'level': 'Beginner', 'credits': 2},
        ]

        PREREQUISITES = [
            ('Intro to Python', 'Web Development with JavaScript'),
            ('Intro to Python', 'Data Science Fundamentals'),
            ('Data Science Fundamentals', 'Machine Learning A-Z'),
            ('Machine Learning A-Z', 'Advanced Deep Learning'),
            ('Linear Algebra for Data Science', 'Machine Learning A-Z'),
            ('Statistical Methods', 'Data Science Fundamentals'),
            ('Intro to Python', 'Django Web Framework'),
            ('Web Development with JavaScript', 'React for Beginners'),
            ('Intro to Python', 'Java Programming'),
        ]

        COURSE_SKILL_REQUIREMENTS = {
            'Intro to Python': [('Python', 1), ('Git', 1)],
            'Web Development with JavaScript': [('JavaScript', 2), ('HTML/CSS', 1)],
            'Data Science Fundamentals': [('Python', 2), ('Statistics', 2), ('SQL', 1)],
            'Machine Learning A-Z': [('Python', 3), ('Statistics', 3), ('Linear Algebra', 2), ('Machine Learning', 1)],
            'Advanced Deep Learning': [('Python', 4), ('Machine Learning', 3), ('Deep Learning', 2), ('Calculus', 3)],
            'Linear Algebra for Data Science': [('Calculus', 2), ('Linear Algebra', 1)],
            'UI/UX Design Principles': [('UI/UX Design', 1)],
            'React for Beginners': [('JavaScript', 3), ('React', 1)],
            'Django Web Framework': [('Python', 3), ('Django', 1), ('SQL', 2)],
            'DevOps with Docker and Kubernetes': [('Docker', 1), ('Linux', 2), ('Git', 2)],
            'Data Visualization with Tableau': [('Tableau', 1), ('SQL', 1)],
            'Natural Language Processing': [('Python', 4), ('Machine Learning', 3), ('NLP', 1)],
            'Java Programming': [('Java', 1)],
            'Statistical Methods': [('Statistics', 2), ('Calculus', 1)],
            'Git and Version Control': [('Git', 1)],
        }

        INSTRUCTOR_COURSES = {
            'Dr. Emily Davis': ['Intro to Python', 'Data Science Fundamentals', 'Machine Learning A-Z'],
            'Prof. John Doe': ['Web Development with JavaScript', 'React for Beginners', 'Java Programming'],
            'Prof. Sarah Connor': ['Advanced Deep Learning', 'Natural Language Processing'],
            'Dr. Michael Chen': ['Linear Algebra for Data Science', 'Statistical Methods'],
            'Prof. Lisa Park': ['UI/UX Design Principles', 'Data Visualization with Tableau', 'DevOps with Docker and Kubernetes', 'Git and Version Control', 'Django Web Framework'],
        }

        STUDENT_ENROLLMENTS = {
            'Alice Johnson': ['Intro to Python', 'Data Science Fundamentals', 'Statistical Methods'],
            'Bob Smith': ['Web Development with JavaScript', 'React for Beginners', 'Django Web Framework'],
            'Carol White': ['Machine Learning A-Z', 'Linear Algebra for Data Science', 'Advanced Deep Learning'],
            'David Brown': ['UI/UX Design Principles', 'Data Visualization with Tableau'],
            'Eva Green': ['Intro to Python', 'Java Programming', 'Git and Version Control'],
            'Frank Taylor': ['DevOps with Docker and Kubernetes', 'Git and Version Control'],
            'Grace Lee': ['Data Science Fundamentals', 'Statistical Methods', 'Natural Language Processing'],
            'Henry Kim': ['Web Development with JavaScript', 'Django Web Framework', 'React for Beginners'],
            'Isabel Martinez': ['Intro to Python', 'Data Science Fundamentals', 'Machine Learning A-Z'],
            'Jack Wilson': ['Linear Algebra for Data Science', 'Statistical Methods', 'UI/UX Design Principles'],
        }

        STUDENT_SKILLS = {
            'Alice Johnson': [('Python', 4), ('Statistics', 3), ('SQL', 2), ('Git', 2)],
            'Bob Smith': [('JavaScript', 4), ('React', 3), ('Django', 2), ('Git', 3)],
            'Carol White': [('Python', 5), ('Machine Learning', 4), ('Linear Algebra', 3), ('Deep Learning', 3)],
            'David Brown': [('UI/UX Design', 4), ('Tableau', 3), ('SQL', 2)],
            'Eva Green': [('Python', 3), ('Java', 4), ('Git', 3)],
            'Frank Taylor': [('Docker', 4), ('Linux', 4), ('Git', 4)],
            'Grace Lee': [('Python', 4), ('Statistics', 4), ('Machine Learning', 3), ('NLP', 2)],
            'Henry Kim': [('JavaScript', 5), ('React', 4), ('SQL', 3), ('Git', 3)],
            'Isabel Martinez': [('Python', 4), ('Statistics', 3), ('Linear Algebra', 2), ('Machine Learning', 2)],
            'Jack Wilson': [('Calculus', 3), ('Linear Algebra', 4), ('Statistics', 3), ('UI/UX Design', 2)],
        }

        # ---------- Helper functions (same as before) ----------
        def clear_all(tx):
            tx.run("MATCH (n) DETACH DELETE n")

        def create_student(tx, student):
            tx.run(
                "MERGE (s:Student {name: $name, email: $email, enrolled_since: $enrolled_since})",
                name=student['name'], email=student['email'], enrolled_since=student['enrolled_since']
            )

        def create_instructor(tx, instructor):
            tx.run(
                "MERGE (i:Instructor {name: $name, email: $email})",
                name=instructor['name'], email=instructor['email']
            )

        def create_skill(tx, skill):
            tx.run(
                "MERGE (sk:Skill {name: $name, category: $category})",
                name=skill['name'], category=skill['category']
            )

        def create_course(tx, course):
            tx.run(
                "MERGE (c:Course {title: $title, description: $description, level: $level, credits: $credits})",
                title=course['title'], description=course['description'],
                level=course['level'], credits=course['credits']
            )

        def create_prerequisite(tx, prereq_title, course_title):
            tx.run(
                """
                MATCH (prereq:Course {title: $prereq_title})
                MATCH (course:Course {title: $course_title})
                MERGE (prereq)-[:PREREQUISITE_FOR]->(course)
                """,
                prereq_title=prereq_title, course_title=course_title
            )

        def create_course_skill_requirement(tx, course_title, skill_name, min_proficiency):
            tx.run(
                """
                MATCH (c:Course {title: $course_title})
                MATCH (sk:Skill {name: $skill_name})
                MERGE (c)-[:REQUIRES {minimum_proficiency: $min_proficiency}]->(sk)
                """,
                course_title=course_title, skill_name=skill_name, min_proficiency=min_proficiency
            )

        def create_instructor_teaches(tx, instructor_name, course_title):
            tx.run(
                """
                MATCH (i:Instructor {name: $instructor_name})
                MATCH (c:Course {title: $course_title})
                MERGE (i)-[:TEACHES]->(c)
                """,
                instructor_name=instructor_name, course_title=course_title
            )

        def create_student_enrollment(tx, student_name, course_title, enrollment_date):
            tx.run(
                """
                MATCH (s:Student {name: $student_name})
                MATCH (c:Course {title: $course_title})
                MERGE (s)-[:ENROLLED_IN {enrollment_date: $enrollment_date}]->(c)
                """,
                student_name=student_name, course_title=course_title, enrollment_date=enrollment_date
            )

        def create_student_skill(tx, student_name, skill_name, proficiency):
            tx.run(
                """
                MATCH (s:Student {name: $student_name})
                MATCH (sk:Skill {name: $skill_name})
                MERGE (s)-[:HAS_SKILL {proficiency: $proficiency}]->(sk)
                """,
                student_name=student_name, skill_name=skill_name, proficiency=proficiency
            )

        # ---------- Execute ----------
        with driver.session(database=database) as session:
            session.execute_write(clear_all)
            self.stdout.write("Cleared existing data.")

            for student in STUDENTS:
                session.execute_write(create_student, student)
            self.stdout.write(f"Created {len(STUDENTS)} students.")

            for instructor in INSTRUCTORS:
                session.execute_write(create_instructor, instructor)
            self.stdout.write(f"Created {len(INSTRUCTORS)} instructors.")

            for skill in SKILLS:
                session.execute_write(create_skill, skill)
            self.stdout.write(f"Created {len(SKILLS)} skills.")

            for course in COURSES:
                session.execute_write(create_course, course)
            self.stdout.write(f"Created {len(COURSES)} courses.")

            for prereq_title, course_title in PREREQUISITES:
                session.execute_write(create_prerequisite, prereq_title, course_title)
            self.stdout.write(f"Created {len(PREREQUISITES)} prerequisite relationships.")

            for course_title, requirements in COURSE_SKILL_REQUIREMENTS.items():
                for skill_name, min_prof in requirements:
                    session.execute_write(create_course_skill_requirement, course_title, skill_name, min_prof)
            self.stdout.write("Created course-skill requirement relationships.")

            for instructor_name, course_titles in INSTRUCTOR_COURSES.items():
                for course_title in course_titles:
                    session.execute_write(create_instructor_teaches, instructor_name, course_title)
            self.stdout.write("Created instructor-teaches relationships.")

            for student_name, course_titles in STUDENT_ENROLLMENTS.items():
                for course_title in course_titles:
                    days_ago = random.randint(1, 365)
                    date = (datetime.now() - timedelta(days=days_ago)).strftime('%Y-%m-%d')
                    session.execute_write(create_student_enrollment, student_name, course_title, date)
            self.stdout.write("Created student enrollments.")

            for student_name, skill_list in STUDENT_SKILLS.items():
                for skill_name, prof in skill_list:
                    session.execute_write(create_student_skill, student_name, skill_name, prof)
            self.stdout.write("Created student-skill relationships.")

        driver.close()
        self.stdout.write(self.style.SUCCESS("Database seeding completed successfully."))