

# ---------- Basic Queries ----------

GET_ALL_STUDENTS = """
MATCH (s:Student)
RETURN s.name AS name, s.email AS email, s.enrolled_since AS enrolled_since
ORDER BY s.name
"""

GET_STUDENT_BY_NAME = """
MATCH (s:Student {name: $name})
RETURN s.name AS name, s.email AS email, s.enrolled_since AS enrolled_since
"""

GET_STUDENT_COURSES = """
MATCH (s:Student {name: $name})-[r:ENROLLED_IN]->(c:Course)
RETURN c.title AS title, c.description AS description, c.level AS level,
       c.credits AS credits, r.enrollment_date AS enrollment_date
ORDER BY r.enrollment_date DESC
"""

GET_STUDENT_SKILLS = """
MATCH (s:Student {name: $name})-[r:HAS_SKILL]->(sk:Skill)
RETURN sk.name AS name, sk.category AS category, r.proficiency AS proficiency
ORDER BY sk.name
"""

GET_COURSE_BY_TITLE = """
MATCH (c:Course {title: $title})
RETURN c.title AS title, c.description AS description,
       c.level AS level, c.credits AS credits
"""

GET_COURSE_SKILLS = """
MATCH (c:Course {title: $title})-[r:REQUIRES]->(sk:Skill)
RETURN sk.name AS name, sk.category AS category, r.minimum_proficiency AS min_proficiency
ORDER BY sk.name
"""

GET_COURSE_PREREQUISITES = """
MATCH (c:Course {title: $title})<-[:PREREQUISITE_FOR]-(prereq:Course)
RETURN prereq.title AS title
ORDER BY prereq.title
"""

GET_COURSE_INSTRUCTORS = """
MATCH (i:Instructor)-[:TEACHES]->(c:Course {title: $title})
RETURN i.name AS name, i.email AS email
ORDER BY i.name
"""

SEARCH_COURSES_BY_SKILL = """
MATCH (c:Course)-[:REQUIRES]->(sk:Skill {name: $skill_name})
RETURN DISTINCT c.title AS title, c.description AS description,
       c.level AS level, c.credits AS credits
ORDER BY c.title
"""

LIST_COURSES_BY_INSTRUCTOR = """
MATCH (i:Instructor {name: $instructor_name})-[r:TEACHES]->(c:Course)
RETURN c.title AS title, c.description AS description,
       c.level AS level, c.credits AS credits
ORDER BY c.title
"""

# ---------- Advanced Queries ----------

# Multi-hop traversal: courses a student is eligible to take (based on skills and prerequisites)
ELIGIBLE_COURSES = """
MATCH (s:Student {name: $student_name})
MATCH (c:Course)
WHERE NOT (s)-[:ENROLLED_IN]->(c)
  AND ALL(req IN [(c)-[:REQUIRES]->(sk:Skill) | {skill: sk.name, min: req.minimum_proficiency}]
         WHERE EXISTS {
           MATCH (s)-[r:HAS_SKILL]->(sk2:Skill {name: req.skill})
           WHERE r.proficiency >= req.min
         })
  AND ALL(prereq_title IN [(c)<-[:PREREQUISITE_FOR]-(p:Course) | p.title]
          WHERE EXISTS {
            MATCH (s)-[:ENROLLED_IN]->(pc:Course {title: prereq_title})
          })
RETURN c.title AS title, c.description AS description,
       c.level AS level, c.credits AS credits
ORDER BY c.title
"""

# "Awkward for relational": trending courses among similar skill profiles
TRENDING_COURSES = """
MATCH (s:Student {name: $student_name})
MATCH (s)-[r1:HAS_SKILL]->(skill:Skill)
WHERE r1.proficiency >= 1
WITH s, collect(skill) AS student_skills
MATCH (peer:Student)-[r2:HAS_SKILL]->(shared_skill:Skill)
WHERE peer <> s
  AND shared_skill IN student_skills
  AND r2.proficiency >= 3
WITH peer, count(DISTINCT shared_skill) AS overlap_count
WHERE overlap_count >= 2
MATCH (peer)-[:ENROLLED_IN]->(course:Course)
WHERE NOT (s)-[:ENROLLED_IN]->(course)
RETURN course.title AS title, course.description AS description,
       course.level AS level, course.credits AS credits,
       count(DISTINCT peer) AS peer_count
ORDER BY peer_count DESC, course.title
LIMIT 10
"""

# Health check
HEALTH_CHECK = """
RETURN 1 AS alive
"""
