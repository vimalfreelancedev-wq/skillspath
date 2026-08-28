import logging
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from .db import run_query
from . import queries

logger = logging.getLogger(__name__)

def index(request):
    return render(request, 'index.html')

def student_dashboard(request, name):
    return render(request, 'student.html', {'student_name': name})

def course_detail(request, title):
    return render(request, 'course.html', {'course_title': title})

def search_courses(request):
    skill = request.GET.get('skill')
    if not skill:
        return render(request, 'search_results.html', {'courses': [], 'skill': None})
    try:
        records = run_query(queries.SEARCH_COURSES_BY_SKILL, {'skill_name': skill})
        courses = [dict(r) for r in records]
        return render(request, 'search_results.html', {'courses': courses, 'skill': skill})
    except Exception as e:
        logger.error(f"Error searching courses: {e}")
        return render(request, 'search_results.html', {'error': True})

def instructor_courses(request, name):
    try:
        records = run_query(queries.LIST_COURSES_BY_INSTRUCTOR, {'instructor_name': name})
        courses = [dict(r) for r in records]
        return render(request, 'instructor.html', {'instructor_name': name, 'courses': courses})
    except Exception as e:
        logger.error(f"Error fetching instructor courses: {e}")
        return render(request, 'instructor.html', {'error': True})

@csrf_exempt
def admin_seed(request):
    if request.method == 'POST':
        from django.core.management import call_command
        try:
            call_command('seed')
            return render(request, 'admin.html', {'success': True})
        except Exception as e:
            logger.error(f"Seeding failed: {e}")
            return render(request, 'admin.html', {'error': str(e)})
    return render(request, 'admin.html')

# ---------- API Views ----------
def api_students(request):
    try:
        records = run_query(queries.GET_ALL_STUDENTS)
        students = [{'name': r['name'], 'email': r['email'], 'enrolled_since': r['enrolled_since']} for r in records]
        return JsonResponse(students, safe=False)
    except Exception as e:
        logger.error(f"Error fetching students: {e}")
        return JsonResponse({'error': 'Unable to fetch students'}, status=500)

def api_student_profile(request, name):
    try:
        records = run_query(queries.GET_STUDENT_BY_NAME, {'name': name})
        if not records:
            return JsonResponse({'error': 'Student not found'}, status=404)
        print("records",records[0])
        return JsonResponse(records[0],safe=False)
    except Exception as e:
        logger.error(f"Error fetching student profile: {e}")
        return JsonResponse({'error': 'Unable to fetch profile'}, status=500)

def api_student_courses(request, name):
    try:
        records = run_query(queries.GET_STUDENT_COURSES, {'name': name})
        courses = [dict(r) for r in records]
        return JsonResponse(courses, safe=False)
    except Exception as e:
        logger.error(f"Error fetching student courses: {e}")
        return JsonResponse({'error': 'Unable to fetch courses'}, status=500)

def api_student_skills(request, name):
    try:
        records = run_query(queries.GET_STUDENT_SKILLS, {'name': name})
        skills = [dict(r) for r in records]
        return JsonResponse(skills, safe=False)
    except Exception as e:
        logger.error(f"Error fetching student skills: {e}")
        return JsonResponse({'error': 'Unable to fetch skills'}, status=500)

def api_student_recommendations(request, name):
    try:
        eligible_records = run_query(queries.ELIGIBLE_COURSES, {'student_name': name})
        eligible = [dict(r) for r in eligible_records]
        trending_records = run_query(queries.TRENDING_COURSES, {'student_name': name})
        trending = [dict(r) for r in trending_records]
        return JsonResponse({'eligible': eligible, 'trending': trending})
    except Exception as e:
        logger.error(f"Error fetching recommendations: {e}")
        return JsonResponse({'error': 'Unable to fetch recommendations'}, status=500)

def api_course_info(request, title):
    try:
        records = run_query(queries.GET_COURSE_BY_TITLE, {'title': title})
        print("records",records)
        if not records:
            return JsonResponse({'error': 'Course not found'}, status=404)
        return JsonResponse(records[0],safe=False)
    except Exception as e:
        logger.error(f"Error fetching course info: {e}")
        return JsonResponse({'error': 'Unable to fetch course info'}, status=500)

def api_course_skills(request, title):
    try:
        records = run_query(queries.GET_COURSE_SKILLS, {'title': title})
        skills = [dict(r) for r in records]
        return JsonResponse(skills, safe=False)
    except Exception as e:
        logger.error(f"Error fetching course skills: {e}")
        return JsonResponse({'error': 'Unable to fetch course skills'}, status=500)

def api_course_prerequisites(request, title):
    try:
        records = run_query(queries.GET_COURSE_PREREQUISITES, {'title': title})
        prereqs = [r['title'] for r in records]
        return JsonResponse(prereqs, safe=False)
    except Exception as e:
        logger.error(f"Error fetching prerequisites: {e}")
        return JsonResponse({'error': 'Unable to fetch prerequisites'}, status=500)

def api_course_instructors(request, title):
    try:
        records = run_query(queries.GET_COURSE_INSTRUCTORS, {'title': title})
        instructors = [dict(r) for r in records]
        return JsonResponse(instructors, safe=False)
    except Exception as e:
        logger.error(f"Error fetching instructors: {e}")
        return JsonResponse({'error': 'Unable to fetch instructors'}, status=500)

def health(request):
    try:
        run_query(queries.HEALTH_CHECK)
        return JsonResponse({'status': 'ok'}, status=200)
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return JsonResponse({'status': 'unhealthy', 'error': str(e)}, status=503)
