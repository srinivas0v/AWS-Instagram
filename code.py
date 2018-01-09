import os
from boto3.s3.transfer import S3Transfer
from flask import Flask, render_template, request, redirect
import boto3
import requests
from botocore.client import Config

accessKey = 'AKIAI5DPP36U25U2EV3Q'
secretKey = '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'
s3_bname = 'ubantusris3'

client = boto3.client('s3', 'us-east-2')
transfer = S3Transfer(client)

upath = 'C:/Users/srinivas venkatesh/Documents/cloud computing/assg3/files/'
# /home/ubuntu/flaskapp/files/
# /home/ubuntu/flaskapp/downloads/
dpath = 'C:/Users/srinivas venkatesh/Documents/cloud computing/assg3/download/'
spath = 'C:/Users/srinivas venkatesh/Documents/cloud computing/assg3/static/'

s3 = boto3.resource(
    's3',
    aws_access_key_id=accessKey,
    aws_secret_access_key=secretKey,
    config=Config(signature_version='s3v4')
)

app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def main():
    if request.method == 'POST':
        if request.form['submit'] == 'upload':
            f = request.files['fileUpload']
            com = request.form['comment']
            Upload(f,com)

        elif request.form['submit'] == 'download':
            fname = request.form['fileDownload']
            Download(fname)
            return redirect('/view/' + fname)

        elif request.form['submit'] == 'view':
            fname = request.form['fview']
            # view(fname)
            return redirect('/view/' + fname)

        elif request.form['submit'] == 'delete':
            fname = request.form['fdelete']
            deletek(fname)

        elif request.form['submit'] == 'deletecomm':
            wrd = request.form['word']
            deletecom(wrd)

        elif request.form['submit'] == 'list':
            print 'a'
            return redirect('/list')
            print 'aa'
    return render_template('index.html')


# creating a bucket
def createb(bname):
    s3.create_bucket(Bucket=bname)
    s3.create_bucket(Bucket=bname, CreateBucketConfiguration={
        'LocationConstraint': 'us-east-2'})


# delete a bucket
def deleteb(bname):
    b = s3.Bucket(bname)
    for key in b.objects.all():
        key.delete()
    b.delete()


def deletek(fname):
    print fname
    print 'delete function'
    for bucket in s3.buckets.all():
        for key in bucket.objects.all():
            if key.key == fname:
                print(key.key)
                key.delete()
            else:
                print 'not found'



def Upload(file,comm):

        fname = file.filename
        fdata = open(upath + fname, 'rb')
        fdata2= comm
        filename,ext=fname.split('.')
        s3.Bucket(s3_bname).put_object(Key=fname, Body=fdata)
        s3.Bucket(s3_bname).put_object(Key=filename+'_com.txt', Body=fdata2)
        return 'successfully uploaded'


def Download(fname):
    print 'download' + fname
    s3 = boto3.client('s3')
    #s3.download_file(s3_bname, fname, dpath + fname)
    #s3.download_file(s3_bname, fname, spath + fname)
    temp = open('temp.txt','rb')
    fdata = temp.read()
    img,comm=fdata.split('$$$$')
    fl = open(dpath+fname, "wb")
    fl.write(img)
    fl.close()
    f2 = open(spath+fname,"wb")
    f2.write(img)
    f2.close()
    return 'successfully downloaded'


@app.route('/list', methods=['POST', 'GET'])
def list():
    l = []

    for bucket in s3.buckets.all():
        for key in bucket.objects.all():
            filename, ext = key.key.split('.')
            if(ext == 'jpg' or ext =='JPG'):
             print(key.key )
             print key.key, key.last_modified
             a = ''
             a = a+'filename:'+key.key + '   time:' + str(key.last_modified) +''
            elif(ext == 'txt') :
              print key.key
              s = boto3.client('s3')
              s.download_file(s3_bname, key.key, 'temp2.txt')
              temp = open('temp2.txt', 'rb')
              contents = temp.read()
              temp.close()
              a = a+ '    comments:'+contents
              print a
              l.append(a)
    return render_template('list.html', flist=l)

def deletecom(wrd):
    word = wrd

    for bucket in s3.buckets.all():
        for key in bucket.objects.all():
            filename, ext = key.key.split('.')
            if (ext == 'jpg' or ext == 'JPG'):
                print(key.key)
                counter = 0
                print(key.key)
                cname = filename+'_com.txt'
                print cname
                s = boto3.client('s3')
                s.download_file(s3_bname, cname, 'temp.txt')
                temp = open('temp.txt', 'rb')
                comment = temp.read()
                print comment
                temp.close()
                counter = len([x for x in comment.split() if x == wrd])
                print counter
                if (counter>0):
                    print 'deleting'
                    key.delete()
                    
            else:
                print 'not found'


@app.route('/view/<fname>', methods=['POST', 'GET'])
def view(fname):
    print fname
    return render_template('view.html', img=fname)


if __name__ == '__main__':
    app.run(debug=True, port=8080)
