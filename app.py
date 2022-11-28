from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.view import view_config
import shutil

from pyramid.response import Response
import os
import csv
import math


@view_config(
    route_name='home',
    renderer='templates/home.jinja2', request_method= 'POST')


def home(request):
    uploaded_file = request.POST['file']
    input_file = uploaded_file.file
    filename  = uploaded_file.filename

    file_path = os.path.join('/', os.path.abspath(os.path.dirname(__file__)) + '/tmp', filename)
    input_file.seek(0)

    with open(file_path, 'wb') as output_file:
      shutil.copyfileobj(input_file, output_file)
    
    # print(file_path)

def read_file(file_path):
  first_digits = []

  with open(file_path) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    

    for row in csv_reader:
      first_digit = get_first_digit(row[0])
      first_digits.append(first_digit)
  os.remove(file_path)

  first_digits=[int(x) for x in sorted(first_digits)]

  unique=(set(first_digits))#a list with unique values of first_digit list
  data_count=[]
  
  for i in unique:
    count=first_digits.count(i)
    data_count.append(count)
    total_count=sum(data_count)
    data_percentage=[(i/total_count)*100 for i in data_count]




  BENFORD = [30.1, 17.6, 12.5, 9.7, 7.9, 6.7, 5.8, 5.1, 4.6]
  def get_expected_counts(total_count):
    """Return list of expected Benford's Law counts for total sample count."""
    return [round(p * total_count / 100) for p in BENFORD]
    expected_counts=get_expected_counts(total_count)


  chi_square = 0
  chi_square_stat= 0
  json_list = {}
  
  for f_digit in set(first_digits):
    count_of_f_digit = first_digits.count(f_digit)

    try:

      def chi_square_test(data_count,expected_counts):
        chi_square_stat = 0  # chi square test statistic
        for data, expected in zip(data_count,expected_counts):
            chi_square = math.pow(data - expected, 2)
            chi_square_stat += chi_square / expected
            print("\nChi-squared Test Statistic = {:.3f}".format(chi_square_stat))
            print("Critical value at a P-value of 0.05 is 15.51.")   
            return chi_square_stat
        

    except:
      print("Some error while calcualtion of digit {val}" . format(val = f_digit))
  
  is_justified = "Benford law is valid" if (chi_square < 15.51) else "Benford is not valid"

  #for degree of freedom 8, the critical chi-square value is 15.51
  
  return {"Final Message": is_justified}

def get_first_digit(digit):
  if(digit.isdigit()):
    if(int(digit) >= 10):
      digit = str(digit)[0]
    
    return int(digit);






if __name__ == '__main__':
    with Configurator() as config:
        config.add_route('home', '/')
        config.include('pyramid_jinja2')
        config.scan()

        # config.add_view(hello_world, route_name='hello')
        app = config.make_wsgi_app()
    server = make_server('0.0.0.0', 6543, app)
    server.serve_forever()