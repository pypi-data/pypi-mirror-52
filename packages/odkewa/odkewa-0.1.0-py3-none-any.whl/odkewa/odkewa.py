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
PFX = '/odkewa'

######################################################

import sys
reload(sys)
sys.setdefaultencoding('utf8')
from flask import Flask, render_template, request, g, Response, send_file
import hashlib, psycopg2, json, datetime
from json2html import *
import io
import pyaconf

app = Flask(__name__, static_url_path=PFX)

def jsonify(data):
   return Response( response=json.dumps(data), status=200, mimetype='application/json')

def getConn():
   conn = getattr(g, '_database', None)
   if conn is None:
      #conn = g._database = psycopg2.connect("dbname='postgres' user='postgres' password='postgres'  host='ec2-18-130-69-226.eu-west-2.compute.amazonaws.com'")
      conn = g._database = psycopg2.connect("host='localhost' dbname='odkewa' user='ikh' password='hernya8'")
   return conn

def populate_xdata(data):
   data['ts'] = datetime.datetime.utcnow()
   data['device_id'] = hashlib.sha1(str(data['device_ip'])+str(data['device_type'])).hexdigest()

   sid = hashlib.sha1(str(data)).hexdigest()
   fid = data['form_id']
   vid = data['form_version']
   device_id = data['device_id']
   device_ip = data['device_ip']
   device_type = data['device_type']
   xdata = json.dumps(data['data'])
   # print(dir(xdata))
   # print(type(json.loads(xdata)))
   # print(json.loads(xdata))
   
   form = getForm(fid,vid)['survey']

   conn = getConn()
   cur = conn.cursor()
   cur.execute("""
      INSERT INTO xdata (sid, fid, vid, device_id, device_ip, device_type, xdata)
      VALUES (%s, %s, %s, %s, %s, %s, %s);
      """,
      (sid, fid, vid, device_id, device_ip, device_type, xdata))
   conn.commit()
   cur.close()
   return sid

def populate_xdatamedia(data):
   content = data.stream.read()
   ts = datetime.datetime.utcnow()
   msid = hashlib.sha1(content).hexdigest()
   conn = getConn()
   cur = conn.cursor()
   cur.execute("""
     INSERT INTO xdatamedia (msid, filename, mimetype, content)
     SELECT %s, %s, %s, %s
     WHERE NOT EXISTS (SELECT 1 FROM xdatamedia WHERE msid = %s)
     """,
     (msid, data.filename, data.mimetype, psycopg2.Binary(content), msid))
   conn.commit()
   cur.close()
   return msid

def getForm(fid,vid):
   conn = getConn()
   cur = conn.cursor()
   cur.execute("""SELECT xform FROM xmeta WHERE fid = %s AND vid = %s""", (fid,vid))
   row = cur.fetchone()
   cur.close()
   return row[0]


@app.teardown_appcontext
def closeConn(exception):
   conn = getattr(g, '_database', None)
   if conn is not None:
      conn.close()

app.debug = True

@app.route(PFX+'/form/<fid>/<vid>')
def xlsform(fid,vid):
   form = JSON_xlsform(getForm(fid,vid), pfx=PFX).generateForm()
   return render_template('index.html', form=form)

@app.route(PFX+'/submit_form', methods=['POST'])
def submit_form():
   if request.method == "POST":
      form_data = json.loads(request.data)
      form_data['device_ip'] = str(request.remote_addr)
      sid = populate_xdata(form_data)

      return jsonify({"sid": sid})

@app.route(PFX+'/upload_media', methods=['POST'])
def submit_file():
   if request.method == "POST":
      media_data = request.files['file']
      msid = populate_xdatamedia(media_data)
      return jsonify({"msid": msid})

def query(s, args=None):
   c = getConn().cursor()
   c.execute(s, args)
   ds = c.description
   xs = c.fetchall()
   rs = map( lambda z: dict( map( lambda x,y: (x[0],y), ds, z)), xs )
   #print c.query
   c.close()
   return rs

@app.route(PFX+"/mforms")
def showformsmeta():
   rs = query("select fid,vid,giturl,path,ts::text from xmeta order by fid,vid;")
   return jsonify(rs)

@app.route(PFX+"/mform/<fid>/<vid>")
def showformmeta(fid,vid):
   rs = query("select fid,vid,giturl,path,ts::text,xform from xmeta where fid=%s and vid=%s;",(fid,vid))
   return jsonify(rs)

@app.route(PFX+"/submission/<sid>")
def showsubmission(sid):
   rs = query("select sid,fid,vid,device_id,device_ip,device_type,ts::text,xdata from xdata where sid=%s;",(sid,))
   return jsonify(rs)

@app.route(PFX+"/media/<msid>")
def showmedia(msid):
   rs = query("select msid,filename,mimetype,ts::text,content from xdatamedia where msid=%s;",(msid,))
   return send_file(io.BytesIO(rs[0]['content']), mimetype=rs[0]['mimetype'])

@app.route(PFX+"/mmedia/<msid>")
def showmediameta(msid):
   rs = query("select msid,filename,mimetype,ts::text from xdatamedia where msid=%s;",(msid,))
   return jsonify(rs)

if __name__ == '__main__':
   #app.run(host='ec2-18-130-69-226.eu-west-2.compute.amazonaws.com',port=4000, debug=True, ssl_context='adhoc')
   app.run(host='localhost',port=4000, debug=True, ssl_context='adhoc')
