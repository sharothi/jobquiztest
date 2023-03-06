from django.shortcuts import render, redirect, get_object_or_404
from quiz_app.models import Quiz, Option, UserQuizInfo, Student
from django.shortcuts import get_object_or_404
from quiz_app.forms import QuizForm, CreateUserForm, UserLoginForm, CreateStudentForm, CreateTeacherForm, ExaminationInfoForm, PaymentForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout 
from .filters import UserQuizInfoFilter,TeacherInfoFilter, StudentInfoFilter


from django.http import HttpResponse, JsonResponse
from quiz_app.models import Quiz, Option, ExaminationInfo , Teacher, Student,Subject ,InstitutionInfo
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User

import datetime
from django.utils import timezone

import calendar
import time

# def job():
#     print("I'm workent....")





# Create your views here.


def home(request):
    d = datetime.timedelta( seconds = 30)
    # print(d)
    # payment_create_function()
    # institution_deactiv()

    # import pdb; pdb.set_trace()
    message = ''
    if request.headers.get('Referer'):
        if (request.headers['Referer'].find('student/regis/') != -1)or (request.headers['Referer'].find('teacher/regis/')!= -1) or (request.headers['Referer'].find('register/')!= -1) :
            message = 'Registration successful'
    
    homepage_message=''
    top_header=''
    if InstitutionInfo.objects.last():
        homepage_message = InstitutionInfo.objects.last().homepage_message
        top_header = InstitutionInfo.objects.last().top_header
    return render(request, 'home.html' ,{'message':message, 'homepage_message':homepage_message, 'top_header':top_header })

###---------------start registration, login, logout, change password ,update profile ---------###


##----- teacher registration-----##

def teacher_regis(request):
    user_form = CreateUserForm()
    teac_form = CreateTeacherForm()
    if request.method == 'POST':
        user_form = CreateUserForm(request.POST)
        teac_form = CreateTeacherForm(request.POST)
        if user_form.is_valid() and teac_form.is_valid() :
            user = user_form.save()
            teacher = teac_form.save(commit=False)
            teacher.user_info = user
            teacher.save()

            return redirect('quiz_app:home')

    context = {'user_form':user_form, 'teac_form': teac_form}
    return render(request, 'teach_regis.html', context)





##----- student registration-----##


def student_regis(request):
    user_form = CreateUserForm()
    stu_form = CreateStudentForm()
    if request.method == 'POST':

        user_form = CreateUserForm(request.POST)
        stu_form = CreateStudentForm(request.POST)
        if user_form.is_valid() and stu_form.is_valid() :
            user = user_form.save()
            user.username = user.username + str(user.id)
            student = stu_form.save(commit=False)
            student.user_info = user
            student.roll_num = user.id
            student.save()

            return redirect('quiz_app:home')

    context = {'user_form':user_form, 'stu_form': stu_form}
    return render(request, 'stu_regis.html', context)






def login_page(request):
    # all_insti = Institution.objects.all()
    # for inst in all_insti:
    #     payment = Payment.objects.create(institution_info=inst)
    #     payment.save()

    form = UserLoginForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password') 
            user = authenticate(username=username, password=password)
            login(request, user)
            
            try:
                if request.user.teacher.is_teacher:
                    return redirect('quiz_app:teacher_dashboard')

            except:
            
                try:
                    if request.user.student.is_student:
                        return redirect('quiz_app:exam_list')
                except:
                    try:
                        if request.user:
                            return redirect('quiz_app:super_admin_dashboard')
                    except:
                        print("Something went wrong")

            
            


    return render(request, 'login.html', {'form': form})



def logout_view(request):
    logout(request)
    return redirect('quiz_app:home')



###---------------end registration, login, logout, change password ,update profile ---------###






### -----------start only for teacher ----------- ###


@login_required
def exam_info_list(request ):
    exam_info_ls = ExaminationInfo.objects.filter(teacher=request.user.teacher)
    return render(request,'dashboard.html',{'exam_info_ls':exam_info_ls})



            ### ---- for exam info ----##

@login_required
def exam_info_input(request):
    exam_info_form = ExaminationInfoForm()
    if request.method == 'POST':
        exam_info_form = ExaminationInfoForm(request.POST)
        if exam_info_form.is_valid():
            exam_info = exam_info_form.save(commit=False)
            exam_info.teacher = request.user.teacher
            exam_info.save()
            return redirect('quiz_app:teacher_dashboard')

        
    context = {'exam_info_form':exam_info_form}
    return render(request, 'exam_info_form.html', context)


@login_required
def exam_info_details_view(request, pk):
    exam_info = get_object_or_404(ExaminationInfo, pk=pk)
    return render(request, 'exam_info_details.html', {'exam_info':exam_info})


@login_required
def exam_info_update(request, pk):
    exam_info = get_object_or_404(ExaminationInfo, pk=pk)
    exam_info_form = ExaminationInfoForm(instance=exam_info)
    if request.method == "POST":
        exam_info_form = ExaminationInfoForm(request.POST, instance=exam_info)
        if exam_info_form.is_valid():
            exam_info = exam_info_form.save(commit=False)
            # exam_info.institution_name = request.user.teacher.institution_name
            exam_info.teacher = request.user.teacher
            exam_info.save()
            return redirect('quiz_app:exam_info_details', pk=pk)

    context = {'exam_info_form':exam_info_form}
    return render(request, 'exam_info_form.html', context)



@login_required
def exam_info_publish(request, pk):
    exam_info = get_object_or_404(ExaminationInfo, pk=pk)
    exam_info.publish()
    return redirect('quiz_app:exam_info_details', pk=pk)
    

@login_required
def exam_info_status_change(request, pk):
    exam_info = get_object_or_404(ExaminationInfo, pk=pk)
    exam_info.change_status()
    return redirect('quiz_app:teacher_dashboard')

@login_required
def exam_info_delete(request, pk):
    exam_info= get_object_or_404(ExaminationInfo, pk=pk)
    if request.method == "POST":
        exam_info.delete()
        return redirect('quiz_app:teacher_dashboard')
    context = {'pk':pk}
    return render(request, 'exam_info_delete_view.html', context)




    ### -------question_input, edit ,delete --------###
    

@login_required
def question_input_form(request,pk=0):
    exam_info = ExaminationInfo.objects.get(teacher=request.user.teacher, pk=pk)
    number_of_questions = Quiz.objects.filter(exam_info=exam_info)
    quiz_form = QuizForm()

    if request.method == 'POST' :
        quiz_form = QuizForm(request.POST)
        
        if quiz_form.is_valid():

            quiz_title = quiz_form.cleaned_data['title']
            quiz_hints = quiz_form.cleaned_data['hints']
            quiz = Quiz.objects.create( exam_info=exam_info , title = quiz_title, hints = quiz_hints)
            try:
                options_titels = dict(request.POST)['option_title']
                i = 0 
                for opt_title in options_titels:
                    is_corre = 'is_correct_' + str(i)
                    is_corr = True if dict(request.POST).get(is_corre)[0] == 'True' else False 
                    Option.objects.create(quiz=quiz, title=opt_title, is_correct=is_corr)
                    i= i+1
            except:
                quiz.delete()
                return render(request, 'forms.html' , { 'quiz_form':quiz_form, 'message': 'Please input your data correctly' })

            else:
                quiz_form = QuizForm()
                return render(request, 'forms.html' , { 'quiz_form':quiz_form, 'message': 'Submited' ,'number_of_questions':number_of_questions })

                

    return render(request, 'forms.html' , { 'quiz_form':quiz_form , 'number_of_questions':number_of_questions })




@login_required
def question_check_view(request, pk):
    exam_info = ExaminationInfo.objects.get(teacher=request.user.teacher, pk=pk)
    questions = Quiz.objects.filter(exam_info=exam_info)
    return render(request, 'check_questions.html', {'questions':questions})





@login_required
def question_edit(request, pk):
    quiz_data = get_object_or_404(Quiz, pk=pk)
    quiz_form = QuizForm(instance=quiz_data)
    options = Option.objects.filter(quiz=quiz_data)

    if request.method == "POST":
        quiz_form = QuizForm(request.POST, instance=quiz_data)

        if quiz_form.is_valid():
            quiz = quiz_form.save()
            try:
                options_titels = dict(request.POST)['option_title']

                i=0
                for option in options_titels:
                    opt = get_object_or_404(Option, title=option)

                    is_corre = 'is_correct_' + str(i)
                    is_corr = True if dict(request.POST).get(is_corre)[0] == 'True' else False 
                    opt.update(title=opt_title, is_correct=is_corr)

                    i= i+1
            except:
                return render(request, 'questions_edit_form.html' , { 'quiz_form':quiz_form, 'message': 'Please input your data correctly' })

            else:
                quiz_form = QuizForm()
                return render(request, 'questions_edit_form.html' , { 'quiz_form':quiz_form, 'message': 'Submited' ,'number_of_questions':number_of_questions })
        
    context = {'quiz_form':quiz_form, 'options':options}
    return render(request, 'questions_edit_form.html', context)



@login_required
def question_delete(request, pk):
    quiz_data = get_object_or_404(Quiz, pk=pk)
    exam_info_pk = quiz_data.exam_info.pk
    if request.method == "POST":
        quiz_data.delete()
        return redirect('quiz_app:question_check', pk=exam_info_pk)
    context = {'pk':pk}
    return render(request, 'question_delete_view.html', context)
    

@login_required
def std_info_institu(request):
    students = Student.objects.all()
    # print(students)
    return render(request, 'stdinfo_institu.html', {'students':students})
    # f = StudentInfoFilter(request.GET, queryset=students)
    # return render(request, 'stdinfo_institu.html', {'filter':f})


@login_required
def stu_activation(request, pk):
    student=Student.objects.get(pk=pk)
    student.activate_student()
    
    student.approved_by = request.user.teacher
    return redirect('quiz_app:students_of_institution')
###----------------end only for teacher----------###





###----------- start only for students -----------###


# def subject_list_view(request):
#     sub_list = Subject.objects.all()
#     questions=[]
#     for subj in sub_list:
#         question = ExaminationInfo.objects.filter(class_name=request.user.student.class_name, published=True, subject_name=subj).count()
#         questions.append(question)

#     # import pdb; pdb.set_trace()
#     subject_list = zip(sub_list, questions)
#     context ={
#         'subject_list': subject_list
#     }
#     return render(request, 'subject_list_view.html', context)


def exam_list_view(request):
    payment_form = PaymentForm()
    if request.method == 'POST':
        payment_form = PaymentForm(request.POST)
        if payment_form.is_valid():
            payment = payment_form.save(commit=False)
            payment.user_info = request.user.student
            payment.save()
            return redirect('quiz_app:exam_list')
        
    
    exam_list = ExaminationInfo.objects.filter(published=True)

    activation_message = 'There are no activation message from admin'
    if InstitutionInfo.objects.last():
        activation_message = InstitutionInfo.objects.last().activation_message
        after_payment_message = InstitutionInfo.objects.last().after_payment_message

    if exam_list:
        if request.user.student.approved:
            return render(request, 'exam_view1.html', {'std_exam_info':exam_list })
        else:
            # import pdb;pdb.set_trace()
            if not request.user.student.stu_pay_info.last():
                return render(request, 'exam_view.html', { 'activation_message':activation_message, 'form':payment_form})
            else:
                return render(request, 'exam_view1.html', {'after_payment_message':after_payment_message})

    return render(request, 'exam_view1.html', {'message':'There are no Qusetions available','activation_message':activation_message})



@login_required
def quiz_view(request,id , pk=0):
    if not request.user.student : 
        std_exam_info = ExaminationInfo.objects.get(pk=id)
        all_questions = Quiz.objects.filter(exam_info = std_exam_info)
        timeduration = int(std_exam_info.total_time*60)
        time = datetime.timedelta(seconds=timeduration)
    else:
        std_exam_info = ExaminationInfo.objects.get(pk=id)
        all_questions = Quiz.objects.filter(exam_info = std_exam_info)
        timeduration = int(std_exam_info.total_time*60)
        time = datetime.timedelta(seconds=timeduration)
    # print(time)
    if UserQuizInfo.objects.filter(examination_info=std_exam_info,user_info=request.user.student).exists():
        info = UserQuizInfo.objects.filter(examination_info=std_exam_info,user_info=request.user.student)
        last_user_user_quiz_start_time = info[0].start_time
        # import pdb; pdb.set_trace()
        if (time < (timezone.now()-last_user_user_quiz_start_time)):
            if not info[len(info)-1].exam_done:
                info.last().exam_done_ok()
                info.last().exam_end_time()
                # print('time over')
        if UserQuizInfo.objects.get(examination_info=std_exam_info,user_info=request.user.student).exam_done:
            result_info = UserQuizInfo.objects.get(examination_info=std_exam_info, user_info=request.user.student)
            return render(request, 'index.html',{'quiz': 0,'result_info':result_info})

    def get_next_data(quiz_list_id):
        # quiz = Quiz.objects.filter(pk=pk, exam_info = std_exam_info).count()
        # if (quiz == 1):
        #     quiz = Quiz.objects.get(pk=pk, exam_info = std_exam_info)
        #     # quiz = all_questions[]
        #     options = Option.objects.filter(quiz=quiz)
        #     next_pk = pk+1
            
        #     return {'quiz':quiz, 'options':options, 'pk':pk , 'next_pk':next_pk }
    
        # pk = pk + 1
        # return get_next_data(pk)
        quiz = all_questions[quiz_list_id]
        options = Option.objects.filter(quiz=quiz)
        next_pk = quiz_list_id + 1
        pk = quiz_list_id

        return {'quiz':quiz, 'options':options, 'pk':pk , 'next_pk':next_pk }

    if request.method == 'POST' :
        data = get_next_data(pk)
        quiz = data['quiz']
        options = data['options']
        pk = data['pk']
        next_pk = data['next_pk']
        corr_options = Option.objects.filter(quiz=quiz, is_correct = True)
        client_given = list(dict(request.POST).keys())

        if len(client_given)-1 >= 1:
            if (len(corr_options)) == (len(client_given)-1):
                for option in corr_options:
                    if str(option) not in client_given:
                        obj,created = UserQuizInfo.objects.get_or_create(user_info=request.user.student, examination_info=std_exam_info )
                        obj.last_answered_quiz_pk = quiz.pk
                        obj.save()

                        return redirect('quiz_app:quiz_view',id=id, pk=next_pk)

                else:

                    obj,created = UserQuizInfo.objects.get_or_create(user_info=request.user.student , examination_info=std_exam_info )
                    obj.last_answered_quiz_pk = quiz.pk
                    obj.num_of_correct_ans = obj.num_of_correct_ans + 1
                    obj.save()
                    return redirect('quiz_app:quiz_view', id=id, pk=next_pk)

            else:
                obj,created = UserQuizInfo.objects.get_or_create(user_info=request.user.student , examination_info=std_exam_info )
                obj.last_answered_quiz_pk = quiz.pk
                obj.save()
                return redirect('quiz_app:quiz_view', id=id, pk=next_pk)

        else:
            # import pdb; pdb.set_trace()
            return render(request, 'index.html', {'last_user_user_quiz_start_time':last_user_user_quiz_start_time,'quiz':quiz, 'options': options, 'next_pk':next_pk, 'error':'You have not provided any answer'})

            

    if pk == all_questions.count():
        result_info = UserQuizInfo.objects.get(examination_info=std_exam_info,user_info=request.user.student)
        if (pk == all_questions.count()):
            result_info.exam_done_ok()
            result_info.exam_end_time()
        return render(request, 'index.html',{'quiz': 0,'result_info':result_info})
 
    else:

        outputs = get_next_data(pk)
        quiz = outputs['quiz']
        options = outputs['options']
        pk = outputs['pk']
        next_pk = outputs['next_pk']
        last_user_user_quiz_start_time = UserQuizInfo.objects.get_or_create(user_info=request.user.student, examination_info=std_exam_info )[0].start_time
        
        # import pdb; pdb.set_trace()
        return render(request, 'index.html', {'last_user_user_quiz_start_time':last_user_user_quiz_start_time,'quiz':quiz, 'options': options, 'next_pk':next_pk })




###--------------- for super admin ---------------###


def super_admin_dashboard(request):
    
    # print(agents)
    # import pdb; pdb.set_trace()
    return render(request, 'dashboard.html')




def result_view(request):
    students_result = UserQuizInfo.objects.filter(exam_done=True)
    if students_result:
        students_result.order_by('-num_of_correct_ans')[:30]
        top_result = UserQuizInfo.objects.filter(exam_done=True, num_of_correct_ans=students_result[0].num_of_correct_ans).order_by('time_delta')[0]
        # import pdb;pdb.set_trace()
        # print(top_result)
        try:
            if request.user.teacher:
                return render(request, 'result_sheet.html', {'results':students_result ,'top_result':top_result})
        except:
            return render(request,'result_sheet_student.html',{'results':students_result ,'top_result':top_result})

    message = 'কেউ এখনো পরীক্ষায় অংশগ্রহণ করেনি। '
    return render(request, 'result_sheet_student.html',{'message':message}) 