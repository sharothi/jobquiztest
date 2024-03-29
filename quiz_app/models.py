from django.db import models
from django.utils import timezone
from datetime import datetime
from ckeditor.fields import RichTextField

# Create your models here.



####.................site info..................####
class InstitutionInfo(models.Model):
    event_name = models.CharField(max_length=250, default='কুইজ প্রতিযোগিতা' )
    top_header = models.CharField(max_length=200, null=True)
    homepage_message = RichTextField(null=True)
    activation_message = RichTextField(null=True)
    after_payment_message = RichTextField(null=True)

    def __str__(self):
        return self.event_name


#####------------------ user info ------------------------#####



class Teacher(models.Model):
    user_info = models.OneToOneField('auth.User', on_delete = models.CASCADE ,blank=True ,null=True)
    phone_number = models.IntegerField(null=True)
    is_teacher = models.BooleanField(default=True)
    approved = models.BooleanField(default=True)

    def __str__(self):
        return self.user_info.username

    def activate_teacher(self):
        self.approved = True
        self.save()
        return None

    def deactivate_teacher(self):
        self.approved=False
        self.save()
        return None


class Student(models.Model):
    user_info = models.OneToOneField('auth.User', on_delete = models.CASCADE ,blank=True ,null=True)
    roll_num = models.IntegerField()
    # total_time = models.DecimalField(max_digits=5,decimal_places=2)
    phone_number = models.IntegerField(null=True)
    is_student = models.BooleanField(default=True)
    approved = models.BooleanField(default=False)
    approved_by = models.ForeignKey('Teacher', on_delete = models.SET_NULL, blank=True, null=True)

    # stu_quiz_info = models.OneToOneField('UserQuizInfo',on_delete = models.RESTRICT)

    def __str__(self):
        return self.user_info.username
        
    
    def activate_student(self):
        self.approved = True
        self.save()
        return None


    def deactivate_student(self):
        self.approved = False
        self.save()
        return None


class Payment(models.Model):
    user_info = models.ForeignKey('Student', related_name='stu_pay_info', on_delete = models.CASCADE, blank=True ,null = True )
    phone_number = models.IntegerField(null=True)




class UserQuizInfo(models.Model):
    user_info = models.ForeignKey('Student', related_name='stud_info', on_delete = models.CASCADE ,blank=True ,null=True)
    examination_info = models.ForeignKey('ExaminationInfo',related_name='exami_info', on_delete=models.CASCADE, blank=True ,null=True )
    last_answered_quiz_pk = models.IntegerField(default=0)
    num_of_correct_ans = models.IntegerField(default=0)
    exam_done = models.BooleanField(default=False)
    start_time = models.DateTimeField(auto_now_add=True, blank=True, null= True)
    end_time = models.DateTimeField(null=True, blank=True)
    time_delta = models.DurationField(null=True, blank=True)

    @property
    def result(self):
        return self.num_of_correct_ans*self.examination_info.per_ques_marks

    def exam_done_ok(self):
        self.exam_done = True
        self.save()
        return None


    def exam_end_time(self):
        self.end_time = timezone.now()
        # self.time_delta = (self.end_time - self.start_time)
        
        self.time_delta = self.end_time - self.start_time
        self.save()
        return None







# class Payment(models.Model):
#     created_date = models.DateTimeField(auto_now_add=True)
#     payment_status = models.BooleanField(default=False)
#     payment_date = models.DateTimeField(null=True, blank=True)
#     institution_info = models.ForeignKey('Institution',related_name='insti', on_delete=models.SET_NULL, null=True, blank=True)


    
#     def make_payment(self):
#         self.payment_status = True
#         self.payment_date = datetime.now()
#         self.save()
#         return None

#     def __str__(self):
#         return str(self.institution_info.institution_name)

    
#####-------------------- Exam info with institution --------------------#####

class Subject(models.Model):
    title = models.CharField(max_length=50)

    def __str__(self):
        return self.title



class ExaminationInfo(models.Model):

    STATUS_CHOISE = [
        ('pending','pending'),
        ('created','created')
    ]

    exam_name = models.CharField(max_length=200)
    subject_name = models.ForeignKey('Subject', related_name='topic', on_delete=models.SET_NULL, blank=True, null=True)
    teacher = models.ForeignKey('Teacher', related_name= 'teacher_info', on_delete=models.SET_NULL, blank=True, null=True)
    per_ques_marks = models.IntegerField()
    total_time = models.DecimalField(max_digits=5,decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOISE, default='pending')
    published = models.BooleanField(default=False) 
    created_date = models.DateTimeField(auto_now_add=True, blank=True, null= True)


    def __str__(self):
        return self.exam_name

    def publish(self):
        self.published = True
        self.save()
        return None

    def change_status(self):
        self.status = 'created'
        self.save()
        return None


# class Subject(models.Model):
#     title = models.CharField(max_length=50)

#     def __str__(self):
#         return self.title



# class Topic(models.Model):
#     subject = models.ForeignKey('Subject', related_name='topic', on_delete=models.CASCADE,)
#     title = models.CharField(max_length=70)

#     def __str__(self):
#         return self.title



class Quiz(models.Model):
    exam_info = models.ForeignKey('ExaminationInfo', related_name='exam_data', on_delete=models.SET_NULL , null=True ,blank=True)
    title = models.CharField(max_length=1000)
    hints = models.CharField(max_length=3000, null=True ,blank=True)
    is_approved = models.BooleanField(default=False)


    def __str__(self):
        return self.title

    def approved(self):
        self.is_approved = True
        self.save()
        return None
    



class Option(models.Model):
    quiz = models.ForeignKey('Quiz', related_name='option', on_delete=models.CASCADE,)
    title = models.CharField(max_length=500)
    is_correct = models.BooleanField(default=False)
    

    def __str__(self):
        return self.title
