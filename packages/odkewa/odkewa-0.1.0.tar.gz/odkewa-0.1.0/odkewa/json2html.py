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
import json, re, hashlib
from expression_converter import *

def open_json(json_filename):
   with open(json_filename, 'r') as json_file:
      json_object = json.load(json_file)
      return json_object

class JSON_xlsform:

   def __init__(self, json_xlsform, pfx):
      self.pfx = pfx

      self.jsonSurvey = json_xlsform["survey"]
      self.jsonChoices = json_xlsform["choices"]
      self.jsonSettings = json_xlsform["settings"]

      self.form = ""
      self.formOpen = """
                      <div class="container">
                        <form name=\"ODKewaForm\" ng-controller=\"ODKewaCntrl\" ng-submit=\"submitForm();\">
      """
      self.formHeader = ""
      self.formHeaderOpen = """
                        <div class="row">
                           <div class="col-sm-12">
                              <h1>
      """
      self.formHeaderClose = """<img src='"""+self.pfx+"""/iri128.png' align="right" style="height: 50px; margin-top: -7px;">
                              </h1>
                           </div>
                        </div>
                        <br/>
      """
      self.formHTML = ""
      self.formClose = """    <div class=\"row rowgroup\">
                                 <div class=\"col-sm-6\">
                                    <input class=\"btn btn-success\" type=\"submit\" ngClick=\"Submit\" ng-disabled=\"formSubmitted\">
                                 </div>
                                 <div class=\"col-sm-6\">
                                    <div class=\"alert alert-success\" role=\"alert\" ng-show=\"successBool\">
                                       <strong>{{successMessage}}{{sid}}</strong>
                                    </div>
                                    <div class=\"alert alert-danger\" role=\"alert\" ng-show=\"failureBool\">
                                       <strong>{{failureMessage}}</strong>
                                    </div>
                                 </div>
                              </div>
                           </form>
                        </div>
      """

      self.ng = ""
      self.ngScriptOpen = "<script>"
      self.ngScriptClose = "</script>"
      self.ngApp = "var ODKewa = angular.module(\"ODKewa\", ['ngFileUpload']);"
      self.ngCntrl = ""
      self.ngCntrlOpen = """
            ODKewa.controller("ODKewaCntrl", ['$scope', '$http', 'Upload', '$timeout', function ($scope, $http, Upload, $timeout) {
      """
      self.ngCntrlClose = "}]);"
      self.ngScope = """
               $scope.form_id = window.location.pathname.split('/')[window.location.pathname.split('/').length-2];
               $scope.form_version = window.location.pathname.split('/')[window.location.pathname.split('/').length-1];
	       $scope.device_type = navigator.appVersion;
	       $scope.failureMessage = "Unable to submit form. Some conditions have not been satisfied. Please double check your responses!"
               $scope.successMessage = "Form submitted successfully! The submission ID is: ";
               $scope.successBool = false;
               $scope.failureBool = false;
               $scope.formSubmitted = false;
               \n
      """
      self.ngChoicesOpen = "\n$scope.choices = {\n"
      self.ngChoices = ""
      self.ngChoicesClose = "};\n"
      self.ngDataOpen = "\n$scope.data = {\n"
      self.ngData = ""
      self.ngDataClose = "};\n"
      self.ngFunctions = """
               $scope.selected = function(field,selection) {
                  return field == selection;
               };

               $scope.prog_bar_class = function(progress) {
                  if (progress >= 0 && progress < 100) {
                     return "progress-bar progress-bar-success progress-bar-striped active"
                  } 
                  return "progress-bar progress-bar-success"
               };

               $scope.$watch('data', function() {
                  console.log("watcher");
                     if ($scope.formSubmitted) {
                        $scope.formSubmitted = false;
                        $scope.successBool = false;
                        $scope.failureBool = false;
                     };
               }, true);

               $scope.submitForm = function() {
                  var form_data = {
                                 data: $scope.data,
                                 form_id: $scope.form_id,
                                 form_version: $scope.form_version,
                                 device_type: $scope.device_type,
                  };
                  if (!$scope.ODKewaForm.$pristine) {
                     console.log($scope.ODKewaForm.$valid);
                     if ($scope.ODKewaForm.$valid) {
                        $http({
                           url: '""" + self.pfx + """/submit_form',
                           method: 'POST',
                           headers: {'Content-Type': 'application/json'},
                           data: form_data
                        }).then(function successCallback(response){
                           console.log(response.data);
                           console.log("form submitted successfully");
                           $scope.successBool = true;
                           $scope.failureBool = false;
                           $scope.formSubmitted = true;
                           $scope.sid = response.data['sid'];
                        });
                     } else if ($scope.ODKewaForm.$invalid) {
                        console.log("form NOT submitted");
                        $scope.successBool = false;
                        $scope.failureBool = true;
                        $scope.formSubmitted = true;
                     };
                  } else {
                     alert("You haven't entered anything yet!")
                  };
               };\n\n
      """
      self.ngDirectives = "\n"
      self.HTML = ""

   def generateForm(self):
      jsonSurvey = self.jsonSurvey
      jsonChoices = self.jsonChoices
      jsonSettings = self.jsonSettings

      self.generateList(jsonSurvey)
      self.generateNg(jsonSurvey)
      self.generateNgChoices(jsonChoices)

      self.formHeader = self.formHeaderOpen+self.jsonSettings["form_title"]+self.formHeaderClose
      self.form = self.formOpen+self.formHeader+self.formHTML+self.formClose

      self.ngData = self.ngDataOpen+self.ngData+self.ngDataClose
      self.ngChoices = self.ngChoicesOpen+self.ngChoices+self.ngChoicesClose
      self.ngCntrl = self.ngCntrlOpen+self.ngScope+self.ngData+self.ngChoices+self.ngFunctions+self.ngCntrlClose
      self.ng = self.ngScriptOpen+self.ngApp+self.ngCntrl+self.ngDirectives+self.ngScriptClose

      self.HTML = self.form+self.ng

      return self.HTML

   def generateNg(self, fields):
      for question in fields:
         question_type = question["type"]
         default = str(question.get("default",''))

         if question_type == "text":
            self.createNgText(question)
         elif question_type == "integer": 
            self.createNgInteger(question)
         elif question_type == "decimal":
            self.createNgDecimal(question)
         elif question_type == "date":
            self.createNgDate(question)
         elif question_type == "time":
            self.createNgTime(question)
         elif question_type == "datetime":
            self.createNgDateTime(question)
         elif question_type == "geopoint":
            self.createNgGeopoint(question)
         elif question_type == "image":
            self.createNgImage(question)
         elif question_type == "note":
            self.createNgNote(question)
         elif question_type == "select_one":
            self.createNgSelectOne(question)
         elif question_type == "select_multiple":
            self.createNgSelectMultiple(question)
         elif question_type == "group":
            self.createNgGroup(question)
         elif question_type == "repeat":
            self.generateNg(question["fields"])
   
   def generateNgChoices(self, choices):
      for list_name in choices:
         self.ngChoices += "\t"+list_name+": [\n"
         for choice in choices[list_name]:
            # print('list_name=%s choice=%s' % ( list_name, choice ))
            choice_attrs = choice.keys()
            self.ngChoices += '\t{\n'
            for attr in choice_attrs:
               self.ngChoices += "\t\t "+attr+": \""+str(choice[attr])+"\", \n"
            self.ngChoices += '\t},\n'
         self.ngChoices += "],\n"

   def generateList(self, fields):
      for question in fields:
         question_type = question["type"]

         if question_type == "text":
            self.createTextField(question)
         elif question_type == "integer": 
            self.createIntegerField(question)
         elif question_type == "decimal":
            self.createDecimalField(question)
         elif question_type == "date":
            self.createDateField(question)
         elif question_type == "time":
            self.createTimeField(question)
         elif question_type == "datetime":
            self.createDateTimeField(question)
         elif question_type == "geopoint":
            self.createGeopointField(question)
         elif question_type == "image":
            self.createImageField(question)
         elif question_type == "note":
            self.createNoteField(question)
         elif question_type == "select_one":
            self.createSelectOneField(question)
         elif question_type == "select_multiple":
            self.createSelectMultipleField(question)
         elif question_type == "range":
            self.createRangeField(question)
         elif question_type == "group":
            self.createGroup(question)
         elif question_type == "repeat":
            self.createRepeat(question)

   ## ANGULAR GENERATION METHODS

   def createNgText(self, question):
      ec = ExpressionConverter(question)
      default = str(question.get("default",''))

      self.ngFunctions += ec.to_ng_function("relevant")
      self.ngDirectives += ec.to_ng_function("constraint")
      self.ngData += "\t"+question["name"]+": \""+default+"\",\n"

   def createNgInteger(self, question):
      ec = ExpressionConverter(question)
      default = str(question.get("default",''))

      self.ngFunctions += ec.to_ng_function("relevant")
      self.ngDirectives += ec.to_ng_function("constraint")
      self.ngData += "\t"+question["name"]+": "+default+",\n" if default != '' else "\t"+question["name"]+": \"\",\n"

   def createNgDecimal(self, question):
      ec = ExpressionConverter(question)
      default = str(question.get("default",''))

      self.ngFunctions += ec.to_ng_function("relevant")
      self.ngDirectives += ec.to_ng_function("constraint")
      self.ngData += "\t"+question["name"]+": "+default+",\n" if default != '' else "\t"+question["name"]+": \"\",\n"

   def createNgDate(self, question):
      ec = ExpressionConverter(question)
      default = str(question.get("default",''))

      self.ngFunctions += ec.to_ng_function("relevant")
      self.ngDirectives += ec.to_ng_function("constraint")
      self.ngData += "\t"+question["name"]+": \""+default+"\",\n"

   def createNgTime(self, question):
      ec = ExpressionConverter(question)
      default = str(question.get("default",''))

      self.ngFunctions += ec.to_ng_function("relevant")
      self.ngDirectives += ec.to_ng_function("constraint")
      self.ngData += "\t"+question["name"]+": \""+default+"\",\n"

   def createNgDateTime(self, question):
      ec = ExpressionConverter(question)
      default = str(question.get("default",''))

      self.ngFunctions += ec.to_ng_function("relevant")
      self.ngDirectives += ec.to_ng_function("constraint")
      self.ngData += "\t"+question["name"]+": \""+default+"\",\n"

   def createNgGeopoint(self, question):
      ec = ExpressionConverter(question)
      default = str(question.get("default",''))

      self.ngFunctions += ec.to_ng_function("relevant")
      self.ngDirectives += ec.to_ng_function("constraint")

      self.ngFunctions += """
         $scope.gp__"""+question["name"]+""" = function gp__"""+question["name"]+"""() {
            console.log("geopoint function")
            if (navigator.geolocation) {
               navigator.geolocation.getCurrentPosition(function(position) {
                  $scope.data."""+question["name"]+""".latitude = new Intl.NumberFormat('en-US', {maximumFractionDigits:4}).format(position.coords.latitude);
                  $scope.data."""+question["name"]+""".longitude = new Intl.NumberFormat('en-US', {maximumFractionDigits:4}).format(position.coords.longitude);
                  document.getElementById(\"lat_"""+question["name"]+"""\").value = new Intl.NumberFormat('en-US', {maximumFractionDigits:4}).format(position.coords.latitude);
                  document.getElementById(\"lon_"""+question["name"]+"""\").value = new Intl.NumberFormat('en-US', {maximumFractionDigits:4}).format(position.coords.longitude);
               });
            } else {
                alert("Geolocation is not supported by this browser.");
            }
         };
      """
      self.ngData += "\t"+question["name"]+": { latitude: '', longitude: ''},\n"

   def createNgImage(self, question):
      ec = ExpressionConverter(question)
      default = str(question.get("default",''))

      self.ngFunctions += ec.to_ng_function("relevant")
      self.ngDirectives += ec.to_ng_function("constraint")
      self.ngData += "\t"+question["name"]+": \""+default+"\",\n"
      self.ngFunctions += """
               $scope.upload_"""+question["name"]+""" = function(file, errFiles) {
                  $scope.f_"""+question["name"]+""" = file;
                  $scope.errFile_"""+question["name"]+""" = errFiles && errFiles[0];
                  if (file) {
                     // console.log(file);
                     file.upload = Upload.upload({
                        url: '""" + self.pfx + """/upload_media',
                        data: {file: file}
                     });

                     file.upload.then(function (response) {
                        $timeout(function () {
                           console.log(file);
                           file.result = response.data;
                           $scope.data."""+question["name"]+""" = response.data['msid']
                           document.getElementById("display_"""+question['name']+"""").value = file.name
                        });
                     }, function (response) {
                        if (response.status > 0)
                           $scope.errorMsg_"""+question["name"]+""" = response.status + ': ' + response.data;
                     }, function (evt) {
                        file.progress = Math.min(100, parseInt(100.0 * 
                                                evt.loaded / evt.total));
                     });
                  }
               };\n
      """

   def createNgNote(self, question):
      ec = ExpressionConverter(question)
      default = str(question.get("default",''))

      self.ngFunctions += ec.to_ng_function("relevant")
      self.ngDirectives += ec.to_ng_function("constraint")
      self.ngData += "\t"+question["name"]+": \""+default+"\",\n"



   def createNgSelectOne(self, question):
      ec = ExpressionConverter(question)

      self.ngFunctions += ec.to_ng_function("relevant")
      self.ngFunctions += ec.to_ng_function("choice_filter")["filter"]
      self.ngDirectives += ec.to_ng_function("constraint")
      self.ngData += "\t"+question["name"]+": undefined,\n"


   def createNgSelectMultiple(self, question):
      ec = ExpressionConverter(question)

      self.ngFunctions += ec.to_ng_function("relevant")
      self.ngFunctions += ec.to_ng_function("choice_filter")["filter"]
      self.ngDirectives += ec.to_ng_function("constraint")
      self.ngData += "\t"+question["name"]+": undefined,\n"


   def createNgGroup(self, question):
      ec = ExpressionConverter(question)
      default = str(question.get("default",''))

      self.ngFunctions += ec.to_ng_function("relevant")
      self.ngDirectives += ec.to_ng_function("constraint")
      self.generateNg(question["fields"])

   ## FIELD GENERATION METHODS

   def createTextField(self, question):
      name = question["name"]
      sha_name = hashlib.sha1(name).hexdigest()
      label = question.get('label','')
      hint = question["hint"]  if "hint" in question else ""

      field_name = "name=\""+name+"\" "

      c_validation = ''
      c_name = ''
      if 'constraint' in question:
         c_name = sha_name
         msg = question.get("constraint_message",'invalid value')
         flag = "ODKewaForm.%s.$invalid && !ODKewaForm.%s.$pristine" % (name,name)
         c_validation = "<span ng-show=\""+flag+"\" style=\"color:#f00\" >"+msg+"</span>"

      required = ''
      if "required" in question and (question["required"] == "yes" or question["required"] == "true"):
            required = 'required'

      ng_show = "ng-show=\"relevant__"+name+"()\" " if question.get("relevant",'') != '' else ""

      html = """
                  <div class=\"row rowgroup\" """+ng_show+""">
                     <div class=\"form-group """+required+"""\">
                        <div class=\"col-sm-6\">
                           <label class="control-label" for=\""""+name+"""\" >
                              """+label+"""
                           </label>
                        </div>
                        <div class=\"col-sm-6\">
                           <input type=\"text\" 
                                  class=\"form-control\" 
                                  id=\""""+name+"""\" 
                                  """+field_name+""" 
                                  ng-model=\"data."""+name+"""\" 
                                  """+required+""" """+c_name+"""
                           />
                           """+c_validation+"""
                        </div>
                     </div>
                  </div>
      """
      self.formHTML += html

   def createIntegerField(self, question):
      name = question["name"]
      sha_name = hashlib.sha1(name).hexdigest()
      label = question.get('label','')

      field_name = "name=\""+name+"\" "

      c_validation = ''
      c_name = ''
      if 'constraint' in question:
         c_name = sha_name
         msg = question.get("constraint_message",'invalid value')
         flag = "ODKewaForm.%s.$invalid && !ODKewaForm.%s.$pristine" % (name,name)
         c_validation = "<span ng-show=\""+flag+"\" style=\"color:#f00\" >"+msg+"</span>"

      required = ''
      if "required" in question and (question["required"] == "yes" or question["required"] == "true"):
            required = 'required'

      ng_show = "ng-show=\"relevant__"+name+"()\" " if question.get("relevant",'') != '' else ""

      html = """
                  <div class=\"row rowgroup\" """+ng_show+""">
                     <div class=\"form-group """+required+"""\">
                        <div class=\"col-sm-6\">
                           <label class="control-label" for=\""""+name+"""\" >
                              """+label+"""
                           </label>
                        </div>
                        <div class=\"col-sm-6\">
                           <input type=\"number\" 
                                  value=\"0\" 
                                  class=\"form-control\" 
                                  id=\""""+name+"""\" 
                                  """+field_name+""" 
                                  ng-model=\"data."""+name+"""\" 
                                  """+required+""" """+c_name+"""
                           />
                           """+c_validation+"""
                        </div>
                     </div>
                  </div>
      """
      self.formHTML += html

   def createDecimalField(self, question):
      name = question["name"]
      sha_name = hashlib.sha1(name).hexdigest()
      label = question.get('label','')
      hint = question["hint"] if "hint" in question else ""

      field_name = "name=\""+name+"\" "

      c_validation = ''
      c_name = ''
      if 'constraint' in question:
         c_name = sha_name
         msg = question.get("constraint_message",'invalid value')
         flag = "ODKewaForm.%s.$invalid && !ODKewaForm.%s.$pristine" % (name,name)
         c_validation = "<span ng-show=\""+flag+"\" style=\"color:#f00\" >"+msg+"</span>"

      required = ''
      if "required" in question and (question["required"] == "yes" or question["required"] == "true"):
            required = 'required'

      ng_show = "ng-show=\"relevant__"+name+"()\" " if question.get("relevant",'') != '' else ""

      html = """
                  <div class=\"row rowgroup\" """+ng_show+""">
                     <div class=\"form-group """+required+"""\">
                        <div class=\"col-sm-6\">
                           <label class="control-label" for=\""""+name+"""\" >
                              """+label+"""
                           </label>
                        </div>
                        <div class=\"col-sm-6\">
                           <input type=\"number\" 
                                  value=\"0.00\" 
                                  step=\"0.01\" 
                                  class=\"form-control\" 
                                  id=\""""+name+"""\" 
                                  """+field_name+""" 
                                  ng-model=\"data."""+name+"""\" 
                                  """+required+""" """+c_name+"""
                           />
                           """+c_validation+"""
                        </div>
                     </div>
                  </div>
      """
      self.formHTML += html

   def createDateField(self, question):
      name = question["name"]
      sha_name = hashlib.sha1(name).hexdigest()
      label = question.get('label','')

      field_name = "name=\""+name+"\" "

      c_validation = ''
      c_name = ''
      if 'constraint' in question:
         c_name = sha_name
         msg = question.get("constraint_message",'invalid value')
         flag = "ODKewaForm.%s.$invalid && !ODKewaForm.%s.$pristine" % (name,name)
         c_validation = "<span ng-show=\""+flag+"\" style=\"color:#f00\" >"+msg+"</span>"

      required = ''
      if "required" in question and (question["required"] == "yes" or question["required"] == "true"):
            required = 'required'

      ng_show = "ng-show=\"relevant__"+name+"()\" " if question.get("relevant",'') != '' else ""

      html = """
                  <div class=\"row rowgroup\" """+ng_show+""">
                     <div class=\"form-group """+required+"""\">
                        <div class=\"col-sm-6\">
                           <label class="control-label" for=\""""+name+"""\" >
                              """+label+"""
                           </label>
                        </div>
                        <div class=\"col-sm-6\">
                           <input type=\"date\" 
                                  class=\"form-control\" 
                                  id=\""""+name+"""\" 
                                  """+field_name+""" 
                                  ng-model=\"data."""+name+"""\" 
                                  """+required+""" """+c_name+"""
                           />
                           """+c_validation+"""
                        </div>
                     </div>
                  </div>
      """
      self.formHTML += html

   def createTimeField(self, question):
      name = question["name"]
      sha_name = hashlib.sha1(name).hexdigest()
      label = question.get('label','')

      field_name = "name=\""+name+"\" "

      c_validation = ''
      c_name = ''
      if 'constraint' in question:
         c_name = sha_name
         msg = question.get("constraint_message",'invalid value')
         flag = "ODKewaForm.%s.$invalid && !ODKewaForm.%s.$pristine" % (name,name)
         c_validation = "<span ng-show=\""+flag+"\" style=\"color:#f00\" >"+msg+"</span>"

      required = ''
      if "required" in question and (question["required"] == "yes" or question["required"] == "true"):
            required = 'required'

      ng_show = "ng-show=\"relevant__"+name+"()\" " if question.get("relevant",'') != '' else ""

      html = """
                  <div class=\"row rowgroup\" """+ng_show+""">
                     <div class=\"form-group """+required+"""\">
                        <div class=\"col-sm-6\">
                           <label class="control-label" for=\""""+name+"""\" >
                              """+label+"""
                           </label>
                        </div>
                        <div class=\"col-sm-6\">
                           <input type=\"time\" 
                                  class=\"form-control\" 
                                  id=\""""+name+"""\" 
                                  """+field_name+""" 
                                  ng-model=\"data."""+name+"""\" 
                                  """+required+""" """+c_name+"""
                           />
                           """+c_validation+"""
                        </div>
                     </div>
                  </div>
      """
      self.formHTML += html

   def createDateTimeField(self, question):
      name = question["name"]
      sha_name = hashlib.sha1(name).hexdigest()
      label = question.get('label','')

      field_name = "name=\""+name+"\" "

      c_validation = ''
      c_name = ''
      if 'constraint' in question:
         c_name = sha_name
         msg = question.get("constraint_message",'invalid value')
         flag = "ODKewaForm.%s.$invalid && !ODKewaForm.%s.$pristine" % (name,name)
         c_validation = "<span ng-show=\""+flag+"\" style=\"color:#f00\" >"+msg+"</span>"

      required = ''
      if "required" in question and (question["required"] == "yes" or question["required"] == "true"):
            required = 'required'

      ng_show = "ng-show=\"relevant__"+name+"()\" " if question.get("relevant",'') != '' else ""

      html = """
                  <div class=\"row rowgroup\" """+ng_show+""">
                     <div class=\"form-group """+required+"""\">
                        <div class=\"col-sm-6\">
                           <label class="control-label" for=\""""+name+"""\" >
                              """+label+"""
                           </label>
                        </div>
                        <div class=\"col-sm-6\">
                           <input type=\"datetime-local\" 
                                  step=\"60\" 
                                  class=\"form-control\" 
                                  id=\""""+name+"""\" 
                                  """+field_name+""" 
                                  ng-model=\"data."""+name+"""\" 
                                  """+required+""" """+c_name+"""
                           />
                           """+c_validation+"""
                  </div>
      """
      self.formHTML += html

   def createGeopointField(self, question):
      name = question["name"]
      sha_name = hashlib.sha1(name).hexdigest()
      label = question.get("label",'')

      # field_name = "name=\""+name+"\""
      # c_validation = ''
      # c_name = ''
      # if 'constraint' in question:
      #    c_name = hashlib.sha1(name).hexdigest()
      #    msg = question.get("constraint_message",'invalid value')
      #    flag = "ODKewaForm.%s.$invalid && !ODKewaForm.%s.$pristine" % (name,name)
      #    c_validation = "<span ng-show=\""+flag+"\" style=\"color:#f00\" >"+msg+"</span>"

      required = ''
      if "required" in question and (question["required"] == "yes" or question["required"] == "true"):
            required = 'required'

      ng_show = "ng-show=\"relevant__"+name+"()\" " if question.get("relevant",'') != '' else ""

      html = """
 
            <div class=\"row rowgroup\" """+ng_show+""">                 
               <div class=\"form-group """+required+"""\">
                  <div class=\"col-sm-6\">
                     <input class=\"btn btn-warning\" 
                            type=\"button\" 
                            value=\""""+label+"""\" 
                            ng-click=\"gp__"""+name+"""()\"
                     />
                  </div>
                  <div class=\"col-sm-3\">
                     <input class=\"form-control\" 
                            type=\"text\" 
                            name=\"latitude\" 
                            id=\"lat_"""+name+"""\" 
                            placeholder=\"Latitude\" 
                            ng-model=\"data."""+name+""".latitude\" 
                            """+required+"""
                     />
                     """+"""
                  </div>
                  <div class=\"col-sm-3\">
                     <input class=\"form-control\" 
                            type=\"text\" 
                            name=\"longitude\" 
                            id=\"lon_"""+name+"""\" 
                            placeholder=\"Longitude\" 
                            ng-model=\"data."""+name+""".longitude\" 
                            """+required+"""
                     />
                     """+"""
                  </div>
               </div>
            </div>
      """
      self.formHTML += html


   def createImageField(self, question):
      name = question["name"]
      sha_name = hashlib.sha1(name).hexdigest()
      label = question.get('label','')

      field_name = "name=\""+name+"\" "

      c_validation = ''
      c_name = ''
      if 'constraint' in question:
         c_name = sha_name
         msg = question.get("constraint_message",'invalid value')
         flag = "ODKewaForm.%s.$invalid && !ODKewaForm.%s.$pristine" % (name,name)
         c_validation = "<span ng-show=\""+flag+"\" style=\"color:#f00\" >"+msg+"</span>"

      required = ''
      if "required" in question and (question["required"] == "yes" or question["required"] == "true"):
            required = 'required'

      ng_show = "ng-show=\"relevant__"+name+"()\" " if question.get("relevant",'') != '' else ""

      html = """
                  <div class=\"row rowgroup\" """+ng_show+""">
                     <div class=\"form-group """+required+"""\">
                        <div class=\"col-sm-6\">
                           <label class="control-label" for=\""""+name+"""\" >
                              """+label+"""
                           </label>
                        </div>
                        <div class="col-sm-6">
                           <div class="input-group">
                              <label class="input-group-btn">
                                 <span class="btn btn-primary">Browse&hellip;
                                    <input id=\""""+name+"""\" 
                                           type=\"file\" 
                                           accept=\"image/*\" 
                                           """+field_name+""" 
                                           ngf-select=\"upload_"""+name+"""($file, $invalidFiles)\" 
                                           ngf-max-size=\"10MB\" 
                                           style=\"display: none;\" 
                                           class=\"form-control\" 
                                           """+required+""" """+c_name+"""
                                    />
                                 </span>
                              </label>
                              <input id=\"display_"""+name+"""\" 
                                     type=\"text\" 
                                     readonly 
                                     class=\"form-control\"
                              >
                              """+c_validation+"""
                           </div>
                           <br>
                           <div class=\"progress\" ng-show=\"f_"""+name+""".progress >= 0\">
                              <div ng-class=\"prog_bar_class(f_"""+name+""".progress)\" 
                                   role=\"progressbar\" 
                                   aria-valuenow=\"{{f_"""+name+""".progress}}\" 
                                   aria-valuemin=\"0\" 
                                   aria-valuemax=\"100\" 
                                   style=\"width:{{f_"""+name+""".progress}}%\"  
                                   ng-bind=\"f_"""+name+""".progress + '%'\">
                              </div>
                           </div>
                          {{errorMsg_"""+name+"""}}
                        </div>
                     </div>
                  </div>
      """
      self.formHTML += html

   def createNoteField(self, question):
      name = question["name"]
      label = question.get('label','')

      ng_show = "ng-show=\"relevant__"+name+"()\" " if question.get("relevant",'') != '' else ""

      html = """
                  <div class=\"row rowgroup\" """+ng_show+""">
                     <div class=\"form-group\">
                        <div class=\"col-sm-6\">
                           <label class="control-label" for=\""""+name+"""\">
                              """+label+"""
                           </label>
                        </div>
                     </div>
                  </div>
      """
      self.formHTML += html

   def createSelectOneField(self, question):
      name = question["name"]
      sha_name = hashlib.sha1(name).hexdigest()
      label = question.get('label','')
      hint = question.get("hint",'')
      appearance = question.get("appearance",'')
      list_name = question["list_name"]

      ec = ExpressionConverter(question)
      cf_vars = "{"+ec.to_ng_function("choice_filter")["vars"][0:-2]+"}"

      choice_filter = name+"__filter("+cf_vars+")" if "choice_filter" in question.keys() else "choices."+list_name

      field_name = "name=\""+name+"\" "

      c_validation = ''
      c_name = ''
      if 'constraint' in question:
         c_name = sha_name
         msg = question.get("constraint_message",'invalid value')
         flag = "ODKewaForm.%s.$invalid && !ODKewaForm.%s.$pristine" % (name,name)
         c_validation = "<span ng-show=\""+flag+"\" style=\"color:#f00\" >"+msg+"</span>"

      required = ''
      if "required" in question and (question["required"] == "yes" or question["required"] == "true"):
            required = 'required'

      ng_show = "ng-show=\"relevant__"+name+"()\" " if question.get("relevant",'') != '' else ""


      html = """
                  <div class=\"row rowgroup\" """+ng_show+""">
                     <div class=\"form-group """+required+"""\">
                        <div class=\"col-sm-6\">
                           <label class="control-label" for=\""""+name+"""\" >
                              """+label+"""
                           </label>
                        </div>
                        <div class=\"col-sm-6\">
                           <select class=\"form-control\" 
                                   id=\""""+name+"""\" 
                                   """+field_name+""" 
                                   ng-model=\"data."""+name+"""\" 
                                   ng-options=\"c.name as c.label for c in """+choice_filter+"""\" 
                                   """+required+""" """+c_name+""" >
                                   <option value=\"\">Please select...</option>
                           </select>
                           """+c_validation+"""
                        </div>
                     </div>
                  </div>
      """
      self.formHTML += html

   def createSelectMultipleField(self, question):
      name = question["name"]
      sha_name = hashlib.sha1(name).hexdigest()
      label = question.get('label','')
      hint = question.get("hint",'')
      appearance = question.get("appearance",'')
      list_name = question["list_name"]

      ec = ExpressionConverter(question)
      cf_vars = "{"+ec.to_ng_function("choice_filter")["vars"][0:-2]+"}"

      choice_filter = name+"__filter("+cf_vars+")" if "choice_filter" in question.keys() else "choices."+list_name

      field_name = "name=\""+name+"\" "

      c_validation = ''
      c_name = ''
      if 'constraint' in question:
         c_name = sha_name
         msg = question.get("constraint_message",'invalid value')
         flag = "ODKewaForm.%s.$invalid && !ODKewaForm.%s.$pristine" % (name,name)
         c_validation = "<span ng-show=\""+flag+"\" style=\"color:#f00\" >"+msg+"</span>"

      required = ''
      if "required" in question and (question["required"] == "yes" or question["required"] == "true"):
            required = 'required'

      ng_show = "ng-show=\"relevant__"+name+"()\" " if question.get("relevant",'') != '' else ""

      html = """
                  <div class=\"row rowgroup\" """+ng_show+""">
                     <div class=\"form-group """+required+"""\">
                        <div class=\"col-sm-6\">
                           <label class="control-label" for=\""""+name+"""\" >
                              """+label+"""
                           </label>
                        </div>
                        <div class=\"col-sm-6\">
                           <select multiple
                                   class=\"form-control\" 
                                   id=\""""+name+"""\" 
                                   """+field_name+""" 
                                   ng-model=\"data."""+name+"""\" 
                                   ng-options=\"c.name as c.label for c in """+choice_filter+"""\" 
                                   """+required+""" """+c_name+""" >
                           </select>
                           """+c_validation+"""
                        </div>
                     </div>
                  </div>
      """
      self.formHTML += html

   def createRangeField(self, question):
      self.formHTML += ""

   def createGroup(self, question):
      fields = question["fields"]
      ng_show = "ng-show=\"relevant__"+question["name"]+"()\" " if question.get("relevant",'') != '' else ""
      self.formHTML += "<br/><div class=\"group\" "+ng_show+">"
      self.generateList(fields)
      self.formHTML += "</div><br/>"

   def createRepeat(self, question):
      fields = question["fields"]
      self.formHTML += "<br/><div class=\"repeat\" >"
      self.generateList(fields)
      self.formHTML += "</div><br/>"

if __name__ == '__main__':
   if len(sys.argv) == 2:
      form = JSON_xlsform(open_json(sys.argv[1])).generateForm()
   elif len(sys.argv) == 1:
      print("NO ARGUMENT GIVEN")
   else:
      print("ONE ARGUMENT EXPECTED, MORE THAN ONE GIVEN")
