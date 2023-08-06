#
# Copyright (c) 2018-2019 Innokentiy Kumshayev <kumshkesh@gmail.com>
# Copyright (c) 2018-2019 IRI, Columbia University
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
# this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation
# and/or other materials provided with the distribution.
# 3. Neither the name of the copyright holder nor the names of its contributors
# may be used to endorse or promote products derived from this software without
# specific prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
# 
from __future__ import print_function
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import xlrd, json
from expression_converter import *

def generate_json_from(filename):
   xlsform = xlrd.open_workbook(filename)

   json_form = {}

   survey = xlsform.sheet_by_name("survey");
   json_form["survey"] = generate_json_survey(survey, filename)

   if "choices" in xlsform.sheet_names():
      choices = xlsform.sheet_by_name("choices");
      json_choices = generate_json_choices(choices, filename)
      json_form["choices"] = json_choices


   if "settings" in xlsform.sheet_names():
      settings = xlsform.sheet_by_name("settings");
      json_settings = generate_json_settings(settings, filename)
      json_form["settings"] = json_settings

   json_form = json.dumps(json_form, sort_keys=True,
                     indent=4, separators=(',', ': '))

   #GENERATE JSON FILENAME
#   split_filename = filename.split('.')
 #  del split_filename[-1]
  # split_filename.append('json')
 #  json_filename = ".".join(split_filename)
 #  json_filename = "./static/"+json_filename

   #WRITE JSON FILE
 #  with open(json_filename, 'w') as json_file:
 #     json_file.write(json_form)

   return json_form

def unicode_to_utf8(unicode_row):
   utf8_row = []
   for element in unicode_row:
      if ( type(element) == unicode ):
         utf8_row.append(element.encode("utf-8"))
      else:
         utf8_row.append(element)
   return utf8_row

#################

def generate_json_survey(survey, filename):
   survey_attributes = unicode_to_utf8(survey.row_values(0))
   json_survey = []
   make_json_rows(json_survey, survey, survey_attributes, 1)

   return json_survey

def make_json_rows(result, survey, survey_attributes, current_index):
   while current_index < survey.nrows:
      xls_row = unicode_to_utf8(survey.row_values(current_index))
      json_row = make_survey_row(survey_attributes, xls_row)
      row_type = json_row["type"].split(" ")[0]

      json_row_exp = ExpressionConverter(json_row)

      if json_row.get('constraint','') != '':
         json_row_exp.tokenize('constraint')
         json_row['constraint'] = {
            'original': json_row['constraint'],
            'tokenized': json_row_exp.tokenized['constraint']
         }
      if json_row.get('relevant','') != '':
         json_row_exp.tokenize('relevant')
         json_row['relevant'] = {
            'original': json_row['relevant'],
            'tokenized': json_row_exp.tokenized['relevant']
         }
      if json_row.get('choice_filter','') != '':
         json_row_exp.tokenize('choice_filter')
         json_row['choice_filter'] = {
            'original': json_row['choice_filter'],
            'tokenized': json_row_exp.tokenized['choice_filter']
         }
      if json_row.get('calculation','') != '':
         json_row_exp.tokenize('calculation')
         json_row['calculation'] = {
            'original': json_row['calculation'],
            'tokenized': json_row_exp.tokenized['calculation']
         }

      if row_type == "select_one" or row_type == "select_multiple":
         json_row["list_name"] = json_row["type"].split(" ")[1]
         json_row["type"] = row_type
      
      if (row_type == 'begin_group' or row_type == 'begin_repeat'):
         group_type = json_row['type'].split('_')[1]

         repeat_group = {}

         fields = [] 
         current_index = make_json_rows(fields, survey, survey_attributes, current_index+1)
         
         repeat_group['type'] = group_type
         repeat_group['name'] = json_row['name']
         repeat_group['fields'] = fields
         result.append(repeat_group)
      elif (row_type == 'end_group' or row_type == 'end_repeat'):
         return current_index + 1
      else:
         result.append(json_row)
         current_index += 1

   return current_index

def make_survey_row(attributes, xls_row):
   row = {}
   q_type = ''
   for attr_index in range(len(attributes)):
      attr = attributes[attr_index]
      if attr == 'type':
         q_type = xls_row[attr_index]
      if not (xls_row[attr_index] == ''):
         if attr == 'choice_filter' and (q_type == 'select_one' or q_type == 'select_multiple'):
               row[attr] = xls_row[attr_index]
         else:
            row[attr] = xls_row[attr_index]
   return row

#################

def get_question_types(choices):
   question_types = []
   for row_number in range(choices.nrows):
      row = unicode_to_utf8(choices.row_values(row_number))
      for col_number in range(choices.ncols):
         if row[col_number] == "list_name":
            question_types = unicode_to_utf8(list(set(choices.col_values(col_number))))
            del question_types[question_types.index("list_name")]
   return question_types

def make_choices_row(attributes, xls_row, question_type):
   row = {}
   for attr_index in range(1,len(attributes)):
      attribute = attributes[attr_index]
      if xls_row[attr_index] != '':
         row[attribute] = xls_row[attr_index]
   return row

def generate_json_choices(choices, filename):
   json_choices = {}
   if choices.nrows > 0:
      choices_attributes = unicode_to_utf8(choices.row_values(0))

      question_types = get_question_types(choices)

      for q_type in question_types:
         json_choices[q_type] = []
         for row_number in range(1,choices.nrows):
            xls_row = unicode_to_utf8(choices.row_values(row_number))
            if xls_row[0] == q_type:
               json_row = make_choices_row(choices_attributes, xls_row, q_type)
               json_choices[q_type].append(json_row)

   return json_choices

#################

def generate_json_settings(settings, filename):
   json_settings = {}

   if settings.nrows > 0:
      settings_attributes = unicode_to_utf8(settings.row_values(0))

      for attr_index in range(len(settings_attributes)):
         attr = settings_attributes[attr_index]
         values = unicode_to_utf8(settings.row_values(1))
         json_settings[attr] = values[attr_index]


   return json_settings

if __name__ == '__main__':
   if len(sys.argv) == 2:
      print(generate_json_from(sys.argv[1]))
   elif len(sys.argv) == 1:
      print("NO ARGUMENT GIVEN")
   else:
      print("ONE ARGUMENT EXPECTED, MORE THAN ONE GIVEN")

