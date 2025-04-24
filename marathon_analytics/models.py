from django.db import models

# Create your models here.

class Result(models.Model):
    '''
    Store/represent the data from one runner at the Chicago Marathon 2023.
    BIB,First Name,Last Name,CTZ,City,State,Gender,Division,
    Place Overall,Place Gender,Place Division,Start TOD,Finish TOD,Finish,HALF1,HALF2
    '''
    # identification
    bib = models.IntegerField()
    first_name = models.TextField()
    last_name = models.TextField()
    ctz = models.TextField()
    city = models.TextField()
    state = models.TextField()

    # gender/division
    gender = models.CharField(max_length=6)
    division = models.CharField(max_length=6)

    # result place
    place_overall = models.IntegerField()
    place_gender = models.IntegerField()
    place_division = models.IntegerField()

    # timing-related
    start_time_of_day = models.TimeField()
    finish_time_of_day = models.TimeField()

    time_finish = models.TimeField()
    time_half1 = models.TimeField()
    time_half2 = models.TimeField()


    def __str__(self):
        '''Return a string representation of this model instance.'''
        return f'{self.first_name} {self.last_name} ({self.city}, {self.state}), {self.time_finish}'

# def load_data():
#     '''Function to load data reecords from CSV file into the Django database'''

#     # very dangerous line
#     Result.objects.all().delete()
#     filename = r"C:\Users\chris\Desktop\software\newton_voters.csv"
#     f = open(filename, 'r')

#     f.readline()

#     for line in f:
      
#         try:
#           fields = line.strip().split(',')
#           # print(fields)
#           # for j in range(len(fields)):
#           #     print(f'fields[{j}] = {fields[j]}')
#           #  fields[0] = 6
#           # fields[1] = Seifu
#           # fields[2] = Tura Abdiwak
#           # fields[3] = ETH
#           # fields[4] = Addis Abeba
#           # fields[5] = Addis Abeba
#           # fields[6] = Male
#           # fields[7] = 25-29
#           # fields[8] = 5
#           # fields[9] = 5
#           # fields[10] = 2
#           # fields[11] = 7:30:02
#           # fields[12] = 9:35:31
#           # fields[13] = 2:05:29
#           # fields[14] = 1:02:21
#           # fields[15] = 1:03:08
#           result = Result(bib=fields[0],
#                             first_name=fields[1],
#                             last_name=fields[2],
#                             ctz = fields[3],
#                             city = fields[4],
#                             state = fields[5],
                            
#                             gender = fields[6],
#                             division = fields[7],

#                             place_overall = fields[8],
#                             place_gender = fields[9],
#                             place_division = fields[10],
                        
#                             start_time_of_day = fields[11],
#                             finish_time_of_day = fields[12],
#                             time_finish = fields[13],
#                             time_half1 = fields[14],
#                             time_half2 = fields[15],
#                         )
#           result.save()
#          # print(f'Created result: {result}')
      
#         except:
#             print("Something went wrong")
#             print(f"line={line}")

#     print(f"Created:  {len(Result.objects.all())} Results")