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
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import psycopg2, hashlib
from xls2json import *

def populate_xmeta(giturl,vid,path):
   fid = hashlib.sha1(giturl+path).hexdigest()
   xform = generate_json_from(path)
   
   with open(path, 'r') as b:
       x = b.read()
       xlsform = psycopg2.Binary(x)
   #connect = psycopg2.connect("dbname='postgres' user='postgres' password='postgres'  host='ec2-18-130-69-226.eu-west-2.compute.amazonaws.com'")
   connect = psycopg2.connect("dbname='odkewa' user='ikh' password='hernya8'  host='localhost'")
   cursor = connect.cursor()

   cursor.execute("""
     INSERT INTO xmeta (fid, vid, giturl, path, xlsform, xform)
     VALUES (%s, %s, %s, %s, %s, %s);
     """,
     (fid, vid, giturl, path, xlsform, xform))
   connect.commit()
   cursor.close()
   connect.close()
   return fid, vid

def populate_xmeta_kobo(fid,vid,kobourl,path,xlsform,xform):
   xlsform = psycopg2.Binary(xlsform)

   #connect = psycopg2.connect("dbname='postgres' user='postgres' password='postgres'  host='ec2-18-130-69-226.eu-west-2.compute.amazonaws.com'")
   connect = psycopg2.connect("dbname='odkewa' user='ikh' password='hernya8'  host='localhost'")
   cursor = connect.cursor()

   cursor.execute("""
     INSERT INTO xmeta (fid, vid, giturl, path, xlsform, xform) 
     SELECT %s, %s, %s, %s, %s, %s
     WHERE NOT EXISTS (SELECT 1 FROM xmeta WHERE fid = %s AND vid = %s)
     """,
     (fid, vid, kobourl, path, xlsform, xform, fid, vid))
   connect.commit()
   cursor.close()
   connect.close()

def populate_xdata_kobo(sid,fid,vid,device_id,device_ip,device_type,xdata):
   connect = psycopg2.connect("dbname='postgres' user='postgres' password='postgres'  host='ec2-18-130-69-226.eu-west-2.compute.amazonaws.com'")
   #connect = psycopg2.connect("dbname='odkewa' user='ikh' password='hernya8'  host='localhost'")
   cursor = connect.cursor()

   cursor.execute("""
     INSERT INTO xdata (sid, fid, vid, device_id, device_ip, device_type, xdata) 
     SELECT %s, %s, %s, %s, %s, %s, %s
     WHERE NOT EXISTS (SELECT 1 FROM xdata WHERE sid = %s)
     """,
     (sid, fid, vid, device_id, device_ip, device_type, xdata, sid))
   connect.commit()
   cursor.close()
   connect.close()

def populate_xmeta_ona(fid,vid,kobourl,path,xlsform,xform):
   xlsform = psycopg2.Binary(xlsform)

   connect = psycopg2.connect("dbname='postgres' user='postgres' password='postgres'  host='ec2-18-130-69-226.eu-west-2.compute.amazonaws.com'")
   #connect = psycopg2.connect("dbname='odkewa' user='ikh' password='hernya8'  host='localhost'")
   cursor = connect.cursor()

   cursor.execute("""
     INSERT INTO xmeta (fid, vid, giturl, path, xlsform, xform) 
     SELECT %s, %s, %s, %s, %s, %s
     WHERE NOT EXISTS (SELECT 1 FROM xmeta WHERE fid = %s AND vid = %s)
     """,
     (fid, vid, kobourl, path, xlsform, xform, fid, vid))
   connect.commit()
   cursor.close()
   connect.close()

def populate_xdata_ona(sid,fid,vid,device_id,device_ip,device_type,xdata):
   connect = psycopg2.connect("dbname='postgres' user='postgres' password='postgres'  host='ec2-18-130-69-226.eu-west-2.compute.amazonaws.com'")
   #connect = psycopg2.connect("dbname='odkewa' user='ikh' password='hernya8'  host='localhost'")
   cursor = connect.cursor()

   cursor.execute("""
     INSERT INTO xdata (sid, fid, vid, device_id, device_ip, device_type, xdata) 
     SELECT %s, %s, %s, %s, %s, %s, %s
     WHERE NOT EXISTS (SELECT 1 FROM xdata WHERE sid = %s)
     """,
     (sid, fid, vid, device_id, device_ip, device_type, xdata, sid))
   connect.commit()
   cursor.close()
   connect.close()

if __name__ == '__main__':
   if len(sys.argv) == 2:
      populate_xmeta(sys.argv[1])
   elif len(sys.argv) == 1:
      print("NO ARGUMENT GIVEN")
   else:
      print("ONE ARGUMENT EXPECTED, MORE THAN ONE GIVEN")
