from .models import Teacher, Student, UserQuizInfo,ExaminationInfo
from django.contrib.auth.models import User 
import django_filters
from django import forms



# def exam_name_by_teacher(request):
#     import pdb;pdb.set_trace()
#     # company = request.user.company
#     exam = ExaminationInfo.objects.filter(published=True, institution_name=request.user.teacher.institution_name )
#     # return company.department_set.all()
#     return exam

    # ExaminationInfo.objects.filter(published=True)


class UserQuizInfoFilter(django_filters.FilterSet):
    username = django_filters.CharFilter(field_name= 'user_info__user_info__username', lookup_expr='icontains', label='Username')
    email = django_filters.CharFilter(field_name = 'user_info__user_info__email', lookup_expr='icontains', label='Email')
    num_of_correct_ans__gt = django_filters.NumberFilter(field_name='num_of_correct_ans', lookup_expr='gt',)
    num_of_correct_ans__lt = django_filters.NumberFilter(field_name='num_of_correct_ans', lookup_expr='lt')
    roll_num = django_filters.NumberFilter(field_name='user_info__roll_num', label='Roll No.')
    exam_name = django_filters.ModelChoiceFilter(field_name = 'examination_info', queryset=ExaminationInfo.objects.filter(published=True) , label='Exam' )


    class Meta:
        model = UserQuizInfo
        fields = ['num_of_correct_ans']

        

    # @property
    # def qs(self):
    #     parent = super(UserQuizInfoFilter, self ).qs
    #     # user = get_current_user() 
    #     return parent.filter(examination_info__published=True) \
    #         | parent.filter(institution_name=self.request.user.teacher.institution_name)


    # @property
    # def qs(self):
    #     parent = super(UserQuizInfoFilter, self).qs
    #     if self.request:
    #         user = self.request.user
    #     else:
    #         user = None
    #     if user and user.is_authenticated():
    #         return parent.filter(examination_info__published=True, examination_info__institution_name=self.user.teacher.institution_name ) 
    #         # return parent.filter(examination_info__published=True, institution_name=self.request.user.teacher.institution_name ,master=True, deleted__isnull=True, user_fkey=user.id) 

    #     else:
    #         # do something if no request, or no logged in user
    #         # for example
    #         print(self)
    #         # import pdb; pdb.set_trace()
    #         return parent.filter(examination_info__published=True)



# class StudentInfoFilter(django_filters.FilterSet):
#     username = django_filters.CharFilter(field_name= 'user_info__username', lookup_expr='icontains', label='Username')
#     email = django_filters.CharFilter(field_name = 'user_info__email', lookup_expr='icontains', label='Email')
#     roll_num = django_filters.NumberFilter(field_name='roll_num', label='Roll No.')
#     # institution_name = django_filters.ChoiceFilter(field_name='institution_name__institution_name', label='Institution Name')

#     class Meta:
#         model = Student
#         fields = ['username']



class StudentInfoFilter(django_filters.FilterSet):

    username = django_filters.CharFilter(field_name= 'user_info__username', lookup_expr='icontains', label='Username')
    email = django_filters.CharFilter(field_name = 'user_info__email', lookup_expr='icontains', label='Email')
    roll_num = django_filters.NumberFilter(field_name='roll_num', label='Roll No.')
    # institution_name = django_filters.ChoiceFilter(field_name='institution_name__institution_name', label='Institution Name')

    class Meta:
        model = Student
        fields = ['is_student']




class TeacherInfoFilter(django_filters.FilterSet):

    username = django_filters.CharFilter(field_name= 'user_info__username', lookup_expr='icontains', label='Username')
    email = django_filters.CharFilter(field_name = 'user_info__email', lookup_expr='icontains', label='Email')

    class Meta:
        model = Teacher
        fields = ['phone_number']

