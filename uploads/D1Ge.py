from forms import p_chart_form,lra_form, exps_form, qsi_form
from problems.p_chart import pchartsol
from problems.xrchart import xrchartsol
from problems.single_server import sssol
from problems.multi_server import mssol
from problems.lra import lrasol
from problems.exps import expssol
from problems.qsi import qsisol
from problems.msi import msisol
from problems.csi import csisol
from flask import request, jsonify
import os, json

import shutil
import logging
from wtforms import FieldList
from flask import Flask,render_template
app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
cwd = os.getcwd()



#TEST COMMENT TO CHECK GIT SCRIPT
@app.route('/solversite')
def homepage():
    return render_template('home.html')


@app.route('/')
def mainpage():
    return render_template('main.html')




@app.route('/solversite/forecasting_methods/lra', methods=['GET','POST'])
def lra_page():
    shutil.rmtree(cwd+'/static/images')
    os.mkdir(cwd+'/static/images')
    os.mkdir(cwd+'/static/images/formulas')
    form = lra_form()
    if form.is_submitted():
        x_name = request.form.get('x_name')
        y_name = request.form.get('y_name')
        val_x = request.form.get('val_x')
        val_y = request.form.get('val_y')
        lrasol1 = lrasol(x_name,y_name,val_x,val_y)
        lrasol1 = lrasol1.lrasolcal()
        return render_template('lra.html', lra_form=form, lrasol1=lrasol1)
    else:
        return render_template('lra.html', lra_form=form)

@app.route('/solversite/forecasting_methods/exps', methods=['GET','POST'])
def exps_page():
    shutil.rmtree(cwd+'/static/images')
    os.mkdir(cwd+'/static/images')
    os.mkdir(cwd+'/static/images/formulas')
    form = exps_form()
    if form.is_submitted():


        x_name = request.form.get('x_name')
        y_name = request.form.get('y_name')
        val_x = request.form.get('val_x')
        val_y = request.form.get('val_y')
        val_alpha = request.form.get('val_alpha')
        if request.form['val_initforecast'] != '':
            initforecast = request.form.get('val_initforecast')
        else:
            initforecast = [str(x) for x in val_y.split(' ')][0]
        expssol1 = expssol(x_name,y_name,val_x,val_y,val_alpha, initforecast)
        expssol1 = expssol1.expssolcal()
        return render_template('exps.html', exps_form=form, expssol1=expssol1)
    else:
        return render_template('exps.html', exps_form=form)

@app.route('/solversite/feedback', methods=['GET','POST'])
def feedback():
    if request.method=='POST':
        f = open(cwd+'/static/feedback.txt','a+')
        fb = request.form['feedback']
        f.write('\n')
        f.write('----------------------------')
        f.write('\n')
        f.write(fb)
    return render_template('feedback.html')



@app.route('/solversite/seasonality_index/si', methods=['GET','POST'])
def si_page():
    shutil.rmtree(cwd+'/static/images')
    os.mkdir(cwd+'/static/images')
    os.mkdir(cwd+'/static/images/formulas')
    if request.method == 'POST':
        
        valdick = {}
        noy = request.form['noy']
        forecast = request.form['forecast']
        period = request.form['period']
        if period=='qsi':
            for i in range(4):
                for j in range(int(noy)):
                    key = f'q{i+1}y{j+1}'
                    value = request.form[f'q{i+1}y{j+1}']
                    valdick[key] = value


            qsisol1 = qsisol(valdick,noy)
            qsisol1 = qsisol1.qsisolcal()
            x = []
            y = []
            number = 1
            for i in range(int(noy)):
                for j in range(4):
                    y.append(valdick[f'q{j+1}y{i+1}'])
                    x.append(f'{number}')
                    number +=1

            x = ' '.join(x)
            y = ' '.join(y)

            if forecast=='lra':
                lrasol1 = lrasol('Quarters', 'Years', x, y)
                lrasol1 = lrasol1.lrasolcal()
                lray = int(request.form['lray'])
                return jsonify({'data': render_template('siresponse.html', noy=int(noy), nop=4, keyname='Quarter', keyletter='q', qsisol1=qsisol1, lrasol1=lrasol1, lray=lray)})
            elif forecast=='exps':
                alpha = request.form['expa']
                if request.form['initforecast'] != '':
                    initforecast = request.form['initforecast']
                    ifc=True
                else:
                    initforecast = [str(x) for x in y.split(' ')][0]
                    ifc = False
                expssol1 = expssol('Quarters', 'Values', x, y, alpha, initforecast)
                expssol1 = expssol1.expssolcal()
                return jsonify({'data':render_template('siresponse.html', noy=int(noy), nop=4, keyname='Quarter', keyletter='q', qsisol1=qsisol1, expssol1=expssol1, ifc=ifc)})


        if period=='msi':
            for i in range(12):
                for j in range(int(noy)):
                    key = f'm{i+1}y{j+1}'
                    value = request.form[f'm{i+1}y{j+1}']
                    valdick[key] = value


            msisol1 = msisol(valdick,noy)
            msisol1 = msisol1.msisolcal()
            x = []
            y = []
            number = 1
            for i in range(int(noy)):
                for j in range(12):
                    y.append(valdick[f'm{j+1}y{i+1}'])
                    x.append(f'{number}')
                    number +=1

            x = ' '.join(x)
            y = ' '.join(y)

            if forecast=='lra':
                lrasol1 = lrasol('months', 'Years', x, y)
                lrasol1 = lrasol1.lrasolcal()
                lray = int(request.form['lray'])
                return jsonify({'data': render_template('siresponse.html', noy=int(noy), nop=12, keyname='Month', keyletter='m', qsisol1=msisol1, lrasol1=lrasol1, lray=lray)})
            elif forecast=='exps':
                alpha = request.form['expa']
                if request.form['initforecast'] != '':
                    initforecast = request.form['initforecast']
                    ifc=True
                else:
                    initforecast = [str(x) for x in y.split(' ')][0]
                    ifc = False
                expssol1 = expssol('months', 'Values', x, y, alpha, initforecast)
                expssol1 = expssol1.expssolcal()
                return jsonify({'data': render_template('siresponse.html', noy=int(noy),nop=12, keyname='Month', keyletter='m', qsisol1=msisol1, expssol1=expssol1, ifc=ifc)})


        if period=='csi':
            nop = int(request.form['nop'])
            for i in range(int(nop)):
                for j in range(int(noy)):
                    key = f'p{i+1}y{j+1}'
                    value = request.form[f'p{i+1}y{j+1}']
                    valdick[key] = value
            csisol1 = csisol(valdick,noy,nop)
            csisol1 = csisol1.csisolcal()
            x = []
            y = []
            number = 1
            for i in range(int(noy)):
                for j in range(nop):
                    y.append(valdick[f'p{j+1}y{i+1}'])
                    x.append(f'{number}')
                    number +=1

            x = ' '.join(x)
            y = ' '.join(y)

            if forecast=='lra':
                lrasol1 = lrasol('Periods', 'Years', x, y)
                lrasol1 = lrasol1.lrasolcal()
                lray = int(request.form['lray'])
                return jsonify({'data': render_template('siresponse.html', noy=int(noy), nop=nop,keyname='Period', keyletter='c', qsisol1=csisol1, lrasol1=lrasol1, lray=lray)})
            elif forecast=='exps':
                alpha = request.form['expa']
                if request.form['initforecast'] != '':
                    initforecast = request.form['initforecast']
                    ifc=True
                else:
                    initforecast = [str(x) for x in y.split(' ')][0]
                    ifc = False
                expssol1 = expssol('Periods', 'Values', x, y, alpha, initforecast)
                expssol1 = expssol1.expssolcal()
                return jsonify({'data': render_template('siresponse.html', noy=int(noy),nop=nop,keyname='Period', keyletter='c', qsisol1=csisol1, expssol1=expssol1, ifc=ifc)})

    else:
        return render_template('si2.html')

@app.route('/solversite/seasonality_index/qsi', methods=['GET','POST'])
def qsi_page():
    if request.method == 'POST':
        valdick = {}
        noy = request.form['noy']

        for i in range(4):
            for j in range(int(noy)):
                key = f'q{i+1}y{j+1}'
                value = request.form[f'q{i+1}y{j+1}']
                valdick[key] = value
        #

        qsisol1 = qsisol(valdick,noy)
        qsisol1 = qsisol1.qsisolcal()
        return render_template('qsi.html', noy=int(noy), qsisol1=qsisol1)
    else:
        return render_template('qsi.html')

@app.route('/solversite/seasonality_index/msi', methods=['GET','POST'])
def msi_page():
    if request.method == 'POST':
        valdick = {}
        noy = request.form['noy']
        for i in range(12):
            for j in range(int(noy)):
                key = f'm{i+1}y{j+1}'
                value = request.form[f'm{i+1}y{j+1}']
                valdick[key] = value
        #

        msisol1 = msisol(valdick,noy)
        msisol1 = msisol1.msisolcal()
        return render_template('msi.html', noy=int(noy), msisol1=msisol1)
    else:
        return render_template('msi.html')
@app.route('/solversite/control_charts/pchart', methods=['GET','POST'])
def p_chart_page():

    shutil.rmtree(cwd+'/static/images')
    os.mkdir(cwd+'/static/images')
    os.mkdir(cwd+'/static/images/formulas')

    if request.method=='POST':
        resp = request.json
        print(f'RESP RESP ::::::::: {resp}')
        print(resp)
        sample_size = int(resp['sample_size'])
        if 'sample_name' in resp and resp['sample_name']!='':
            sample_name = resp['sample_name']
        elif resp['sample_name']=='':
            sample_name= 'Samples'
        else:
            sample_name = 'Samples'
        print(sample_name)
        val_desc = resp['val_desc']
        abc = [sample_size,sample_name,val_desc]
        pchartsol1 = pchartsol(sample_name,sample_size,val_desc)
        print(abc)
        pchartsol1 = pchartsol1.p_chart_cal()
        defdrill = pchartsol1.defdrill

        x = [x for x in pchartsol1.fd if x < pchartsol1.LCL or x > pchartsol1.UCL]

        if pchartsol1.stbl == 0:

            stbldefdrills = [x for x in pchartsol1.defdrill]
            stblfd = [x for x in pchartsol1.fd]
            stblsize = sample_size - len(stbldefdrills)

            for i in x:
                a = stblfd.index(i)
                stblfd.pop(a)
                stbldefdrills.pop(a)

            stbldefdrills = [str(x) for x in stbldefdrills]
            stbldefdrills = ' '.join(stbldefdrills)
            pchartstbl = pchartsol(sample_name, stblsize, stbldefdrills)
            pchartstbl = pchartstbl.p_chart_cal()
            stbldefdrill = pchartstbl.defdrill
            return jsonify({'data': render_template('pchartresponse.html', formdata=abc, pchartsol1=pchartsol1, pchartstbl = pchartstbl, defdrill = defdrill, stbldefdrill = stbldefdrill, x=x)})
        else:
            return jsonify({'data':render_template('pchartresponse.html', formdata=abc, pchartsol1=pchartsol1, defdrill = defdrill)})

    else:
        return render_template('pchart2.html')

@app.route('/solversite/serving_models/single', methods=['GET','POST'])
def single_server():
    if request.method == 'POST':
        resp = request.json
        if 'cust_name' in resp:
            cust_name = resp['cust_name']
        else:
            cust_name = 'Customer'
        ar_type = resp['arrival']
        sr_type = resp['services']
        if ar_type == 'ar_rate': #AR GIVEN CALCULATE IAR
            ar_rate = float(resp['ar_rate_cust'])
            ar_rate_time = resp['ar_rate_time']
            if ar_rate_time == 'days':
                ar_rate = round((ar_rate/24),2)
            if ar_rate_time == 'hours':
                ar_rate = round(ar_rate,2)
            if ar_rate_time == 'minutes':
                ar_rate =  ar_rate*60
            if ar_rate_time == 'seconds':
                ar_rate = ar_rate*3600

            iar_rate = 1/ar_rate
            ar_type = 1

        else: #IAR GIVEN CALCULATE AR
            iar_rate = float(resp['iar_rate_cust'])
            iar_rate_time = (resp['iar_rate_time'])
            if iar_rate_time == 'days':
                iar_rate = iar_rate*24
            if iar_rate_time == 'hours':
                iar_rate = round(iar_rate,2)
            if iar_rate_time == 'minutes':
                iar_rate =  round((iar_rate/60),2)
            if iar_rate_time == 'seconds':
                iar_rate = round((iar_rate/3600),2)

            ar_rate = 1/iar_rate
            ar_type = 2
        if sr_type == 'sr_rate': #SERVICE RATE GIVEN CALCULATE TBS
            sr_rate = float(resp['sr_rate_cust'])
            sr_rate_time = (resp['sr_rate_time'])
            if sr_rate_time == 'days':
                sr_rate = round((sr_rate/24),2)
            if sr_rate_time == 'hours':
                sr_rate = round(sr_rate,2)
            if sr_rate_time == 'minutes':
                sr_rate =  sr_rate*60
            if sr_rate_time == 'seconds':
                sr_rate = sr_rate*3600

            tbs_rate = 1/sr_rate
            sr_type = 1

        else: #TIME BETWEEN SERVICE IS GIVEN CALCULATE SERVICE RATE
            tbs_rate = float(resp['tbs_rate_cust'])
            tbs_time = (resp['tbs_time'])
            if tbs_time == 'days':
                tbs_rate = round((tbs_rate/24),2)
            if tbs_time == 'hours':
                tbs_rate = round(tbs_rate,2)
            if tbs_time == 'minutes':
                tbs_rate =  round((tbs_rate/60),2)
            if tbs_time == 'seconds':
                tbs_rate = round((tbs_rate/3600),2)
            sr_type = 2
            sr_rate = 1/tbs_rate
        x = {}
        y = {}

        if resp['probcustno'][0] != '':
            for i in range(0,len(resp['probcustno'])):
                x[i+1] = [resp['probcusttime'][i], int(resp['probcustno'][i])] 

        if resp['probwaitno'][0] != '':
            for i in range(0,len(resp['probwaitno'])):
                a = resp[f'probwaittime'][i]
                b = float(resp[f'probwaitno'][i])
                time = resp[f'probwaittime2'][i]
                if time == 'days':
                    b = b/24
                if time == 'hours':
                    b = b
                if time == 'minutes':
                    b =  b/60
                if time == 'seconds':
                    b = b/3600
                b = round(b,4)
                y[i+1] = [a,b]
            
        sssol1 = sssol(ar_rate, iar_rate, sr_rate, tbs_rate)
        sssol1 = sssol1.sssolcal()
        if x!={} and y!={}:
            x = sssol1.sssol_pcustcal(x)
            y = sssol1.sssol_pwaitcal(y)
            return jsonify({'data': render_template('single_serverresponse.html', sssol1 = sssol1, x=x,y=y, sr_type=sr_type, ar_type=ar_type)})
        elif x != {}:

            x = sssol1.sssol_pcustcal(x)

            return jsonify({'data':render_template('single_serverresponse.html', sssol1=sssol1, x=x, sr_type=sr_type, ar_type=ar_type)})
        elif y != {}:

            y = sssol1.sssol_pwaitcal(y)

            return jsonify({'data': render_template('single_serverresponse.html', sssol1=sssol1, y=y, sr_type=sr_type, ar_type=ar_type)})
        else:
            return jsonify({'data': render_template('single_serverresponse.html',sssol1=sssol1, sr_type=sr_type, ar_type=ar_type)})
    else:
        return render_template('single_server2.html')

@app.route('/solversite/serving_models/multi', methods=['GET','POST'])
def multi_server():
    if request.method == 'POST':
        if 'cust_name' in request.form:
            cust_name = request.form['cust_name']
        else:
            cust_name = 'Customer'
        noc = int(request.form['noc'])
        ar_type = request.form['arrival']
        sr_type = request.form['services']
        if ar_type == 'ar_rate': #AR GIVEN CALCULATE IAR
            ar_rate = float(request.form['ar_rate_cust'])
            ar_rate_time = request.form['ar_rate_time']
            if ar_rate_time == 'days':
                ar_rate = round((ar_rate/24),2)
            if ar_rate_time == 'hours':
                ar_rate = round(ar_rate,2)
            if ar_rate_time == 'minutes':
                ar_rate =  ar_rate*60
            if ar_rate_time == 'seconds':
                ar_rate = ar_rate*3600

            iar_rate = 1/ar_rate
            ar_type = 1

        else: #IAR GIVEN CALCULATE AR
            iar_rate = float(request.form['iar_rate_cust'])
            iar_rate_time = (request.form['iar_rate_time'])
            if iar_rate_time == 'days':
                iar_rate = iar_rate*24
            if iar_rate_time == 'hours':
                iar_rate = round(iar_rate,2)
            if iar_rate_time == 'minutes':
                iar_rate =  round((iar_rate/60),2)
            if iar_rate_time == 'seconds':
                iar_rate = round((iar_rate/3600),2)

            ar_rate = 1/iar_rate
            ar_type = 2
        if sr_type == 'sr_rate': #SERVICE RATE GIVEN CALCULATE TBS
            sr_rate = float(request.form['sr_rate_cust'])
            sr_rate_time = (request.form['sr_rate_time'])
            if sr_rate_time == 'days':
                sr_rate = round((sr_rate/24),2)
            if sr_rate_time == 'hours':
                sr_rate = round(sr_rate,2)
            if sr_rate_time == 'minutes':
                sr_rate =  sr_rate*60
            if sr_rate_time == 'seconds':
                sr_rate = sr_rate*3600

            tbs_rate = 1/sr_rate
            sr_type = 1

        else: #TIME BETWEEN SERVICE IS GIVEN CALCULATE SERVICE RATE
            tbs_rate = float(request.form['tbs_rate_cust'])
            tbs_time = (request.form['tbs_time'])
            if tbs_time == 'days':
                tbs_rate = round((tbs_rate/24),2)
            if tbs_time == 'hours':
                tbs_rate = round(tbs_rate,2)
            if tbs_time == 'minutes':
                tbs_rate =  round((tbs_rate/60),2)
            if tbs_time == 'seconds':
                tbs_rate = round((tbs_rate/3600),2)
            sr_type = 2
            sr_rate = 1/tbs_rate
        x = {}
        y = {}
        if request.form['prob_cust_no1'] != '': #FIRST KINDA PROB
            i = 1
            while f'prob_cust_no{i}' in request.form:
                a = request.form[f'prob_cust{i}']
                b = int(request.form[f'prob_cust_no{i}'])
                x[i] = [a,b]
                i = i+1

        if request.form['prob_wait_no1'] != '': #FIRST KINDA PROB
            j = 1
            while f'prob_wait_no{j}' in request.form:
                a = request.form[f'prob_wait{j}']
                b = float(request.form[f'prob_wait_no{j}'])
                time = request.form[f'prob_wait_time{j}']
                if time == 'days':
                    b = b/24
                if time == 'hours':
                    b = b
                if time == 'minutes':
                    b =  b/60
                if time == 'seconds':
                    b = b/3600
                b = round(b,4)
                y[j] = [a,b]
                j = j+1
        mssol1 = mssol(ar_rate, iar_rate, sr_rate, tbs_rate, noc)
        mssol1 = mssol1.mssolcal()
        if x!={} and y!={}:
            x = mssol1.mssol_pcustcal(x)
            y = mssol1.mssol_pwaitcal(y)
            return render_template('multi_server.html', mssol1 = mssol1, x=x,y=y, sr_type=sr_type, ar_type=ar_type)
        elif x != {}:

            x = mssol1.mssol_pcustcal(x)

            return render_template('multi_server.html', mssol1=mssol1, x=x, sr_type=sr_type, ar_type=ar_type)
        elif y != {}:

            y = mssol1.mssol_pwaitcal(y)

            return render_template('multi_server.html', mssol1=mssol1, y=y, sr_type=sr_type, ar_type=ar_type)
        else:
            return render_template('multi_server.html',mssol1=mssol1, sr_type=sr_type, ar_type=ar_type)
    else:
        return render_template('multi_server.html')

@app.route('/solversite/control_charts/xrchart', methods=['GET','POST'])
def xrchart():
    if request.method == 'POST':
        if request.form['choice'] == 'c1':
            nos = int(request.form['smpl'])
            nog = int(request.form['subg'])
            x = {}
            y = {}
            valdic= {}
            valdic2={}
            for i in range(1,nos+1):
                sum = 0.0
                l = []
                for j in range(1,nog+1):
                    sum = sum + float(request.form[f's{i}g{j}'])
                    l.append(float(request.form[f's{i}g{j}']))
                valdic[i] = l

                x[f'{i}'] = sum/nog
                y[f'{i}'] = max(l)-min(l)

            xrchartsol1 = xrchartsol(x,y,nog)
            xrchartsol1 = xrchartsol1.xrchartsolcal()

            if xrchartsol1.flag == 1:
                z = {x:valdic[x] for x in valdic.keys() if x-1 not in xrchartsol1.flags }
                a = 1
                z2 = {}
                for i in z:
                    z2[a] = z[i]
                    a = a + 1


                print(f'Z :: 1{z}')
                print(f' Z :: 2{z2}')
                return render_template('xrchart.html', nos=nos, nog=nog, xr=xrchartsol1, c1='c1', valdic=valdic, valdic2=z2)
            else:
                return render_template('xrchart.html', nos=nos, nog=nog, xr=xrchartsol1, c1='c1', valdic=valdic)
        if request.form['choice'] == 'c2':
            nos = int(request.form['smpl'])
            nog = int(request.form['subg'])
            x = {}
            y = {}
            for i in range(1,nos+1):
                x[f'{i}'] = float(request.form[f'mean{i}'])
                y[f'{i}'] = float(request.form[f'range{i}'])
            xrchartsol1 = xrchartsol(x,y,nog)
            xrchartsol1 = xrchartsol1.xrchartsolcal()
            print(f'FLAG ={xrchartsol1.flag}')
            return render_template('xrchart.html', nos=nos, nog=nog,xr=xrchartsol1, c2='c2')
    return render_template('xrchart.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0")
