import random
from datetime import date, timedelta
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from courses.models import Instructor, Course, Enrollment

class Command(BaseCommand):
    help = 'Seeds the database with sample course data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding database...')
        
        # Create admin user if it doesn't exist
        if not User.objects.filter(username='admin').exists():
            admin_user = User.objects.create_superuser(
                username='admin',
                email='admin@example.com',
                password='adminpassword'
            )
            self.stdout.write(self.style.SUCCESS(f'Created admin user: {admin_user.username}'))
        
        # Create instructors
        instructors_data = [
            {
                'username': 'jsmith',
                'first_name': 'John',
                'last_name': 'Smith',
                'email': 'jsmith@example.com',
                'bio': 'Professor with 15 years of teaching experience in Computer Science.',
                'expertise': 'Computer Science'
            },
            {
                'username': 'mjohnson',
                'first_name': 'Maria',
                'last_name': 'Johnson',
                'email': 'mjohnson@example.com',
                'bio': 'Experienced instructor specializing in Mathematics and Statistics.',
                'expertise': 'Mathematics'
            },
            {
                'username': 'alee',
                'first_name': 'Alex',
                'last_name': 'Lee',
                'email': 'alee@example.com',
                'bio': 'Industry professional with background in software engineering.',
                'expertise': 'Software Engineering'
            },
        ]
        
        created_instructors = []
        for instructor_data in instructors_data:
            username = instructor_data.pop('username')
            first_name = instructor_data.pop('first_name')
            last_name = instructor_data.pop('last_name')
            email = instructor_data.pop('email')
            
            # Create user if it doesn't exist
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    'first_name': first_name,
                    'last_name': last_name,
                    'email': email,
                    'is_staff': True
                }
            )
            
            if created:
                user.set_password(f'{username}123')
                user.save()
                self.stdout.write(f'Created user: {user.username}')
            
            # Create instructor if it doesn't exist
            instructor, created = Instructor.objects.get_or_create(
                user=user,
                defaults=instructor_data
            )
            
            if created:
                self.stdout.write(f'Created instructor: {instructor}')
            
            created_instructors.append(instructor)
        
        # Create courses
        courses_data = [
            {
                'title': 'Introduction to Programming',
                'code': 'CS101',
                'description': 'A beginner-friendly introduction to programming concepts using Python.',
                'credits': 3,
                'level': 'BEG',
                'max_students': 40,
                'instructor_idx': 0,
            },
            {
                'title': 'Data Structures and Algorithms',
                'code': 'CS201',
                'description': 'Study of fundamental data structures and algorithms for solving computational problems.',
                'credits': 4,
                'level': 'INT',
                'max_students': 30,
                'instructor_idx': 0,
            },
            {
                'title': 'Database Systems',
                'code': 'CS301',
                'description': 'Introduction to database design, implementation, and management.',
                'credits': 3,
                'level': 'INT',
                'max_students': 25,
                'instructor_idx': 2,
            },
            {
                'title': 'Web Development',
                'code': 'CS350',
                'description': 'Fundamentals of web development including HTML, CSS, JavaScript, and frameworks.',
                'credits': 3,
                'level': 'INT',
                'max_students': 35,
                'instructor_idx': 2,
            },
            {
                'title': 'Calculus I',
                'code': 'MATH101',
                'description': 'Introduction to differential and integral calculus.',
                'credits': 4,
                'level': 'BEG',
                'max_students': 45,
                'instructor_idx': 1,
            },
            {
                'title': 'Statistics',
                'code': 'MATH201',
                'description': 'Introduction to statistical methods and data analysis.',
                'credits': 3,
                'level': 'INT',
                'max_students': 30,
                'instructor_idx': 1,
            },
        ]
        
        today = date.today()
        semester_start = today - timedelta(days=30)  # Assume semester started 30 days ago
        semester_end = semester_start + timedelta(days=120)  # 4-month semester
        
        created_courses = []
        for course_data in courses_data:
            instructor_idx = course_data.pop('instructor_idx')
            course_data['instructor'] = created_instructors[instructor_idx]
            course_data['start_date'] = semester_start
            course_data['end_date'] = semester_end
            
            course, created = Course.objects.get_or_create(
                code=course_data['code'],
                defaults=course_data
            )
            
            if created:
                self.stdout.write(f'Created course: {course}')
            
            created_courses.append(course)
        
        # Add prerequisites
        cs201 = Course.objects.get(code='CS201')
        cs101 = Course.objects.get(code='CS101')
        cs201.prerequisites.add(cs101)
        
        cs301 = Course.objects.get(code='CS301')
        cs301.prerequisites.add(cs201)
        
        math201 = Course.objects.get(code='MATH201')
        math101 = Course.objects.get(code='MATH101')
        math201.prerequisites.add(math101)
        
        # Create students
        students_data = [
            {'username': 'student1', 'first_name': 'Alice', 'last_name': 'Brown'},
            {'username': 'student2', 'first_name': 'Bob', 'last_name': 'Jones'},
            {'username': 'student3', 'first_name': 'Charlie', 'last_name': 'Davis'},
            {'username': 'student4', 'first_name': 'Diana', 'last_name': 'Wilson'},
            {'username': 'student5', 'first_name': 'Evan', 'last_name': 'Taylor'},
        ]
        
        created_students = []
        for student_data in students_data:
            username = student_data['username']
            
            student, created = User.objects.get_or_create(
                username=username,
                defaults={
                    'first_name': student_data['first_name'],
                    'last_name': student_data['last_name'],
                    'email': f'{username}@example.com'
                }
            )
            
            if created:
                student.set_password(f'{username}123')
                student.save()
                self.stdout.write(f'Created student: {student.username}')
            
            created_students.append(student)
        
        # Create enrollments
        for student in created_students:
            # Enroll each student in 2-4 random courses
            num_courses = random.randint(2, 4)
            courses_to_enroll = random.sample(created_courses, num_courses)
            
            for course in courses_to_enroll:
                # Randomly assign status and grades
                status = random.choice(['ENR', 'CMP'])
                grade = None
                if status == 'CMP':
                    grade = random.choice(['A', 'B', 'C', 'D', 'F'])
                
                enrollment, created = Enrollment.objects.get_or_create(
                    student=student,
                    course=course,
                    defaults={
                        'status': status,
                        'grade': grade
                    }
                )
                
                if created:
                    self.stdout.write(f'Enrolled {student.username} in {course.code}')
        
        self.stdout.write(self.style.SUCCESS('Database seeding completed successfully!'))