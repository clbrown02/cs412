from django.db import models
from datetime import datetime

# Create your models here.
class Voter(models.Model):
  '''Model to represent a voter object. Includes Name, Address, and other
  personal information such as voting history and party history'''

  # Fields
  last_name = models.TextField()
  first_name = models.TextField()
  address_street_number = models.TextField()
  address_street_name = models.TextField()
  address_apt_number = models.TextField()
  zip_code = models.IntegerField()
  dob = models.DateField()
  reg_date = models.DateField()
  party = models.CharField(max_length=2)
  precint_number = models.TextField()

  v20 = models.TextField()
  v21_t = models.TextField()
  v21_p = models.TextField()
  v22 = models.TextField()
  v23 = models.TextField()

  voter_score = models.IntegerField()

  def __str__(self):
    '''Represents a string representation of the voter object'''
    return f'{self.first_name} {self.last_name} {self.party}'
  
# def load_data():
#   '''Function to load the voter data into the django database'''

#    # very dangerous line
#   Voter.objects.all().delete()
#   filename = r"C:\Users\chris\Desktop\software\newton_voters.csv"
#   f = open(filename, 'r')
#   f.readline()

#   for line in f:
#     fields = line.split(',')

#     try:

      

#       result = Voter(
#           last_name = fields[1],
#           first_name = fields[2],
#           address_street_number = fields[3],
#           address_street_name = fields[4],
#           address_apt_number = fields[5],
#           zip_code = fields[6],
#           dob = fields[7],
#           reg_date = fields[8],
#           party = fields[9],
#           precint_number = fields[10],

#           v20 = fields[11],
#           v21_t = fields[12],
#           v21_p = fields[13],
#           v22 = fields[14],
#           v23 = fields[15],

#           voter_score = fields[16],
#       )
#       result.save()
#       print(f'Created result: {result}')

#     except Exception as e:
#       print(f'Skipped: {fields} + {e}' )
      

    
# print(f"Created:  {len(Voter.objects.all())} Voters")