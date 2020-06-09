from numpy.distutils.fcompiler import none

from app import app, db
from flask import jsonify, render_template, request, redirect, url_for, session, flash
from app.forms import RegistrationForm, LoginForm, ChangeEmailForm, AddressInputForm
from app.models import User, Address
from flask_login import current_user, login_user, logout_user, login_required
import censusgeocode as cg
import matplotlib.pyplot as plt, mpld3
# import requests
import pandas as pd
import numpy as np
import os
from dotenv import load_dotenv
# import folium
# import tabula
# import requests
# from bs4 import BeautifulSoup
# import shapefile as shp
# import seaborn as sns


@app.route('/', methods=['GET'])  # function decorator/wrapper function that executes a function
@login_required
def index():
    # data = requests.get('http://ergast.com/api/f1/2008/5/qualifying.json').json()
    # wake_map = folium.Map(location=[35.8032, -78.5661])
    context = {
        'user': current_user
    }

    # print(data.content) - don't do this
    # return jsonify({'data': [f"Hello, {i}" for i in names]})
    # print(session.get['some_data'], None)

    return render_template('index.html')




@app.route('/register', methods=['GET', 'POST'])  # when the route is hit - it will run this one.
def register():
    if current_user.is_authenticated:
        print(current_user.is_authenticated)
        print(current_user.is_active)
        print(current_user.is_anonymous)
        print(current_user.get_id)
        return redirect(url_for('index'))
    form = RegistrationForm()
    context = {
        'form': form
        # 'some_data_to_pass': session.get('some_data', None)
    }
    # flask way DELETE {{ form.hidden_tag() }} above first field in register.py
    if request.method == "POST":
        u = User(email=request.form.get('email'), password=request.form.get('password'))
        u.generate_password(u.password)
        db.session.add(u)
        db.session.commit()

    # or do the flask form method ADD {{ form.hidden_tag() }} above first field in register.py
    # if form.validate_on_submit():
    #     u = User(email=request.form.get('email'), password=request.form.get('password'))
    #     u.generate_password(u.password)
    #     db.session.add(u)
    #     db.session.commit()

    # print(request.form.get('email')
    # print("It works!")
    return render_template('register.html', **context)


@app.route('/login', methods=['GET', 'POST'])  # when the route is hit - it will run this one.
def login():
    form = LoginForm()
    context = {
        'form': form
    }
    if request.method == 'POST':
        user = User.query.filter_by(email=request.form.get('email')).first()
        if user is not None and user.check_password(request.form.get('password')):
            flash("The user logged in successfully!", "success")
            login_user(user, remember=request.form.get('remember_me'))
            return redirect(url_for('index'))
        flash("The user was not found!", "danger")
        return redirect(url_for('login'))
    return render_template('login.html', **context)


@app.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = ChangeEmailForm()
    form.email.data = current_user.email
    context = {
        'form': form
    }
    if form.validate_on_submit():  # need hidden field
        current_user.email = request.form.get('email')
        db.session.commit()
        flash('Email has been updated!', 'success')
        return redirect(url_for('profile'))

    return render_template('profile.html', **context)

@app.route('/new_address', methods=['GET','POST'])  # function decorator/wrapper function that executes a function
@login_required
def new_address():
    form = AddressInputForm()
    context = {
        'form': form,
    }
    # reqaddress = f"{request.form.get('address')}, city={request.form.get('city')}, state='NC', zipcode={request.form.get('zipcode')}"
    # ceninfo = cg.address(reqaddress)
    # data={
    #     ceninfo[0]
    # }
    return render_template('new_address.html', **context)

@app.route('/confirm_address', methods=['GET', 'POST'])  # function decorator/wrapper function that executes a function
@login_required
def confirm_address():
    data = (cg.address(request.form.get('address'), city=request.form.get('city'), state=request.form.get('state'),
                       zipcode=request.form.get('zipcode')))
    id = []
    context = {
        'data': data,
    }
    if request.method == "POST":
        address = Address(address=data[0]['matchedAddress'], census_tract=data[0]['geographies']['Census Tracts'][0]['BASENAME'], latitude=data[0]['geographies']['Census Tracts'][0]['CENTLAT'], longitude=data[0]['geographies']['Census Tracts'][0]['CENTLON'], zip=data[0]['addressComponents']['zip'])
        db.session.add(address)
        db.session.commit()
        id = address.id
        session['confirm_address_id']=id
        print(session['confirm_address_id'])
    return render_template('confirm_address.html', **context)

    #     link_add = f"/tract_profile/{cur_id}"
    # return redirect(url_for(link_add))
        # x = data[0]['coordinates']['x']
        # y = data[0]['coordinates']['y']
        # tr_geoid = db.Column(db.Integer)
        # address = db.Column(db.String(180))
        # census_tract = db.Column(db.Float)
        # latitude = db.Column(db.Float)
        # logitude = db.Column(db.Float)
        # coords
        #
        # requested_on
        # reqaddress = f"{request.form.get('address')}, city={request.form.get('city')}, state='NC', zipcode={request.form.get('zipcode')}"
    # ceninfo = cg.address(reqaddress)
    # data={
    #     ceninfo[0]
    # }

# geodata = (cg.address(request.form.get('address'), city=request.form.get('city'), state=request.form.get('state'), zipcode=request.form.get('zipcode')))

# a = Address(address=request.form.get('address'), city=request.form.get('city'), state=request.form.get('state'),
    # zipcode=request.form.get('zipcode')) return redirect(url_for('index')) confirm_address if request.method ==
    # "POST": data = { address: } form = _ co cg.address('1600 Pennsylvania Avenue', city='Washington', state='DC') a
    # = Address(address=request.form.get('address'), city=request.form.get('city'), state=request.form.get('state'),
    # zipcode=request.form.get('zipcode'))
    # 'data': {
    #     'address': geodata[0]['matchedAddress'],
    #     'census_tract': geodata['Census Tracts']['BASENAME'],
    #     'latitude': geodata['Census Tracts']['CENTLAT'],
    #     'logitude': geodata['Census Tracts']['CENTLON'],
    #     'tr_geoid': geodata['Census Tracts']['GEOID'],
    # }

#         db.session.add(a)
#         db.session.commit()



@app.route('/tract_profile', methods=['GET'])  # function decorator/wrapper function that executes a function
@login_required
def tract_profile():
    data = Address.query.filter_by(id=session['confirm_address_id']).first()
    apikey = os.environ.get('GOOGLE_API_KEY')
    map = f"https://www.google.com/maps/embed/v1/search?key=+{apikey}+&q=Daycares+in+{data.zip}+{data.address}"

    zipcode = data.zip
    Tract = data.census_tract

    df_cap = pd.read_csv('wake_centers_cap.csv')
    ccol = ['Unnamed: 0', 'Ind Month', 'Shift', 'LIC', 'Employees',
            'Category Operation', 'Operation Site']
    for c in ccol:
        del df_cap[c]
    df_cap["pk_tot"] = df_cap[' Infant'] + df_cap["1"] + df_cap["2"] + df_cap["3"] + df_cap["4"] + df_cap["5"]
    # df_income = pd.read_csv('wake_tract_income.csv')
    df_income = pd.read_csv('wake_tract_income.csv')

    incol = ['2015 MSA/MD Statewide non-MSA/MD Median Family Income',
             '2019 FFIEC Est. MSA/MD non-MSA/MD Median Family Income',
             '% Below Poverty Line', 'Tract Median Family Income %',
             '2015 Tract Median Family Income',
             '2015 Tract Median Household Income']
    for c in incol:
        del df_income[c]
    df_dc_tracts = pd.read_csv('GeocodeResults2.csv')
    df_dc_tracts['Tract'] = df_dc_tracts['Tract Code'] / 100
    tcols = ['Record ID Number', 'TIGER Address Range Match Indicator', 'TIGER Match Type',
             'TIGER Output Address', 'TIGER Line ID', 'TIGER Line ID Side', 'State Code', 'County Code',
             'Tract Code', 'Block Code']
    for c in tcols:
        del df_dc_tracts[c]
    df_dc_info = pd.read_csv('wake_daycare_info.csv')
    infocol = ['Index', 'Unnamed: 2', 'City', 'State', 'Phone', 'License']
    for c in infocol:
        del df_dc_info[c]
    df_tpop = pd.read_csv('tract_pop.csv')
    tpopcol = ['Geographic Area Name', 'Percent Estimate!!SEX AND AGE!!Total population!!Under 5 years', 'Unnamed: 3']
    for c in tpopcol:
        del df_tpop[c]
    df_zpop = pd.read_csv('zip_pop.csv')
    df_zpop['2010_pop_under_5'] = df_zpop['Total!!Male!!Under 5 years'] + df_zpop['Total!!Female!!Under 5 years']
    zpopcol = ['id', 'Geographic Area Name', 'Total', 'Total!!Male!!Under 5 years', 'Total!!Female!!Under 5 years',
               'id.1']
    for c in zpopcol:
        del df_zpop[c]
    df_dc_info2 = df_dc_info.merge(df_cap, left_on="Facility Name", right_on="Unnamed: 1")
    df_dc_fin = df_dc_info2.merge(df_dc_tracts, left_on="Contact Information", right_on="address")
    fininfocol = ['Contact Information', 'ZIP', 'Unnamed: 1']
    for c in fininfocol:
        del df_dc_fin[c]
    df_tract_fin = df_tpop.merge(df_income, left_on="Unnamed: 4", right_on="Tract Code")
    del df_tract_fin['Unnamed: 4']
    df_tract_fin = df_tract_fin.rename(
        columns={'Estimate!!SEX AND AGE!!Total population!!Under 5 years': '2018_pop_under_5', "Tract Code": "Tract",
                 '2019 Est. Tract Median Family Income': "2019_median_income"})
    df_dc_fin = df_dc_fin.rename(columns={"LIC MAX": 'lic_max'})
    df_childzip = pd.DataFrame(df_dc_fin.groupby(['zip']).ALL.sum())
    df_childzip2 = pd.DataFrame(df_dc_fin.groupby(['zip']).lic_max.sum())
    df_childzip3 = pd.DataFrame(df_dc_fin.groupby(['zip']).pk_tot.sum())
    df_childzipNEW = df_childzip.merge(df_childzip2, on="zip")
    df_childzipNEW = df_childzipNEW.merge(df_childzip3, on="zip")
    df_childzipNEW = df_childzipNEW.reset_index()
    df_zpop = pd.DataFrame(df_zpop)
    df_childzipNEW['zip'] = df_childzipNEW['zip'].astype('int64')
    df_childzipNEW = df_childzipNEW.merge(df_zpop, on='zip')
    df_childzipNEW['utilization'] = df_childzipNEW['pk_tot'] / df_childzipNEW['2010_pop_under_5']
    df_childzipNEW['lic_space'] = df_childzipNEW['lic_max'] / df_childzipNEW['2010_pop_under_5']
    df_childzipNEW["seats_needed"] = df_childzipNEW['2010_pop_under_5'] - df_childzipNEW['pk_tot']

    df_childzipNEW.query('zip == @zipcode')
    df_childzipNEW.query('zip == @zipcode')['utilization']
    df_childzipNEW = df_childzipNEW.merge(df_zpop, on='zip')
    df_childzipNEW = df_childzipNEW.rename(columns={'2010_pop_under_5_x': '2010_pop_under_5'})
    del df_childzipNEW['2010_pop_under_5_y']
    df_childzipNEW['utilization'] = df_childzipNEW['pk_tot'] / df_childzipNEW['2010_pop_under_5']
    df_childzipNEW['lic_space'] = df_childzipNEW['lic_max'] / df_childzipNEW['2010_pop_under_5']
    # df_childzipNEW['utilization']= ["{0:.2f}%".format(val*100) for val in df_childzipNEW['utilization']]
    # df_childzipNEW['lic_space']= ["{0:.2f}%".format(val*100) for val in df_childzipNEW['lic_space']]
    df_childzipNEW["seats_needed"] = df_childzipNEW['2010_pop_under_5'] - df_childzipNEW['pk_tot']
    lg = len(df_childzipNEW)
    zip_ut_all = df_childzipNEW.groupby('zip').utilization.min().nsmallest(lg)
    zip_under_ut = df_childzipNEW.groupby('zip').utilization.min().nsmallest(10)
    ut = df_childzipNEW.query('zip == @zipcode')
    new_zip = ut.utilization

    # rcount = 0
    # # for z in zip_under_ut.index:
    #     rcount+=1
    #     if z == int(zipcode):
    #         ziprank = rcount
    #     else:
    #         ziprank = "N/A"
    # print(ziprank) # can go back to function but need to switch to the all zip db and add if st for color
    def rank(ser, zip):
        count = 0
        for z in ser:
            count += 1
            if z == zip:
                return count

    ziprank = rank(list(zip_ut_all.index), int(zipcode))
    print(ziprank)

    def bar_color(ser, count):
        num = len(ser)
        color = []
        for n in range(num):
            color.append("b")
        if count <= len(ser):
            color[int(count) - 1] = 'r'
            return color
        else:
            for n in range(num):
                color.append("b")
        return color

    fig2 = plt.figure()
    new_zip.plot(kind='bar', figsize=(1, 6), color="r", grid=True)
    plt.title("Address' Zipcode")
    plt.ylabel('')
    plt.ylim(top=1.8)
    plt.xlabel(zipcode)
    plt.xticks(horizontalalignment='right')
    plt.tick_params(labelbottom=False, labelright=False, labeltop=True, labelleft=False, colors="w")
    my_add_zip = mpld3.fig_to_html(fig2)
    # fig 2 will print indiv data

    color = bar_color(zip_under_ut, ziprank)
    fig = plt.figure()
    zip_under_ut.plot(kind='bar', figsize=(6, 6), color=color, grid=True)
    plt.title("The Top 10 zip codes with the lowest child to daycare ratios")
    plt.ylabel('Number of occupied preK seats per child in the zipcode')
    plt.ylim(top=1.8)
    # plt.xlabel('Zipcode')
    zip_comp_bar = mpld3.fig_to_html(fig)
    # Fig 1

    ziplength = len(zip_ut_all)
    zip_p = float(new_zip) * 100
    zip_p_st = "{0:.2f}%".format(zip_p)
    RankState = f"The zipcode {zipcode} ranks number {ziprank} out of {ziplength} zipcodes with available data. Currently, licensed daycare centers in this zipcode can care for {zip_p_st} of the children living in the zipcode."
    # Statement 1

    pktot = int((df_childzipNEW.query('zip == @zipcode'))['pk_tot'])
    pop5 = int((df_childzipNEW.query('zip == @zipcode'))['2010_pop_under_5'])
    nseats = int((df_childzipNEW.query('zip == @zipcode'))['seats_needed'])
    zut = int(((df_childzipNEW.query('zip == @zipcode'))['utilization']) * 100)

    # df_childTract = pd.DataFrame(df_dc_fin.groupby(['Tract']).ALL.sum())
    # df_childTract2 = pd.DataFrame(df_dc_fin.groupby(['Tract']).lic_max.sum())
    # df_childTract3 = pd.DataFrame(df_dc_fin.groupby(['Tract']).pk_tot.sum())
    # df_childTractNEW = df_childTract.merge(df_childTract2, on="Tract")
    # df_childTractNEW = df_childTractNEW.merge(df_childTract3, on="Tract")
    # df_childTractNEW = df_childTractNEW.reset_index()
    # df_tpop = df_tpop.rename(
    #     columns={'Estimate!!SEX AND AGE!!Total population!!Under 5 years': "pop_under_5", "Unnamed: 4": "Tract"})
    # df_tpop = pd.DataFrame(df_tpop)
    # df_childTractNEW['Tract'] = df_childTractNEW['Tract'].astype('float')
    # df_childTractNEW = df_childTractNEW.merge(df_tpop, on='Tract')
    # df_childTractNEW['utilization'] = df_childTractNEW['pk_tot'] / df_childTractNEW['pop_under_5']
    # df_childTractNEW['lic_space'] = df_childTractNEW['lic_max'] / df_childTractNEW['pop_under_5']
    # df_childTractNEW["seats_needed"] = df_childTractNEW['pop_under_5'] - df_childTractNEW['pk_tot']
    # df_childTractNEW.query('Tract == @Tract')
    # df_childTractNEW.query('Tract == @Tract')['utilization']
    # df_childTractNEW = df_childTractNEW.merge(df_tpop, on='Tract')
    # df_childTractNEW = df_childTractNEW.rename(columns={'pop_under_5_x': 'pop_under_5'})
    # del df_childTractNEW['pop_under_5_y']
    # df_childTractNEW['utilization'] = df_childTractNEW['pk_tot'] / df_childTractNEW['pop_under_5']
    # df_childTractNEW['lic_space'] = df_childTractNEW['lic_max'] / df_childTractNEW['pop_under_5']
    # # df_childTractNEW['utilization']= ["{0:.2f}%".format(val*100) for val in df_childTractNEW['utilization']]
    # # df_childTractNEW['lic_space']= ["{0:.2f}%".format(val*100) for val in df_childTractNEW['lic_space']]
    # df_childTractNEW["seats_needed"] = df_childTractNEW['pop_under_5'] - df_childTractNEW['pk_tot']
    # tpktot = int((df_childTractNEW.query('Tract == @Tract'))['pk_tot'])
    # tpop5 = int((df_childTractNEW.query('Tract == @Tract'))['pop_under_5'])
    # tnseats = int((df_childTractNEW.query('Tract == @Tract'))['seats_needed'])
    # tzut = int(((df_childTractNEW.query('Tract == @Tract'))['utilization']) * 100)
    #
    # d = {'col1': ["Children in preK", "0-5 populaion", "Seats needed"],
    #      'Zipcode': [pktot, pop5, nseats],
    #      'Tract': [tpktot, tpop5, tnseats]}
    # df = pd.DataFrame(data=d)
    # # bars = d['col2']
    #
    # fig3 = plt.figure()
    # df.plot(kind='bar', figsize=(8, 6), grid=True)
    # # y_pos = np.arange(len(bars))
    # plt.title("Zipcode Data on Selected Address")
    # plt.ylabel('Number of Students')
    # plt.xlabel('Daycare needs in Wake county')
    # # plt.xticks(y_pos, bars, rotation=90)
    # my_zip_stats = mpld3.fig_to_html(fig3)
    # # fig 3

    #
    color = []
    if nseats > 0:
        color = ['blue', 'blue', "green"]
    else:
        color = ['blue', 'blue', "red"]
    dstats = ["Children in preK", "0-5 population", "Seats needed"]
    dstatnum = [pktot, pop5, nseats]
    x_pos = [i for i, _ in enumerate(dstats)]
    fig3 = plt.figure()
    plt.bar(x_pos, dstatnum, color=color)
    plt.xticks(x_pos, dstats)
    plt.title("Zipcode Data on Selected Address")
    plt.ylabel('Number of Students')
    plt.xlabel('Daycare needs in Wake county')
    my_zip_stats = mpld3.fig_to_html(fig3)
    #fig3
    needsState = f"Currently, there are {nseats} preschool seats needed in the zipcode."
                 # f" and {tnseats} preschool seats needed in the tract."

    # create license types by zip table
    df_dc_fin = df_dc_fin.rename(columns={"License Type": 'license_type'})
    zlic_type3 = df_dc_fin.query('license_type == "3 Star C 2C"').groupby('zip').count()
    zlic_type3 = pd.DataFrame(zlic_type3)
    lcol = ['Facility Name', ' Infant', '1', '2', '3', '4', '5', '5-12', 'ALL', 'lic_max', 'pk_tot',
            'Interpolated Longitude, Latitude', 'address', 'city', 'state', 'Tract', 'SCC']
    for l in lcol:
        del zlic_type3[l]
    zlic_type3 = zlic_type3.rename(columns={'license_type': '3 Star C 2C'})

    zlic_type5 = df_dc_fin.query('license_type == "5 Star C 2C"').groupby('zip').count()
    zlic_type5 = pd.DataFrame(zlic_type5)
    lcol = ['Facility Name', ' Infant', '1', '2', '3', '4', '5', '5-12', 'ALL', 'lic_max', 'pk_tot',
            'Interpolated Longitude, Latitude', 'address', 'city', 'state', 'Tract', 'SCC']
    for l in lcol:
        del zlic_type5[l]
    zlic_type5 = zlic_type5.rename(columns={'license_type': '5 Star C 2C'})

    zlic_type4 = df_dc_fin.query('license_type == "4 Star C 2C"').groupby('zip').count()
    zlic_type4 = pd.DataFrame(zlic_type4)
    lcol = ['Facility Name', ' Infant', '1', '2', '3', '4', '5', '5-12', 'ALL', 'lic_max', 'pk_tot',
            'Interpolated Longitude, Latitude', 'address', 'city', 'state', 'Tract', 'SCC']
    for l in lcol:
        del zlic_type4[l]
    zlic_type4 = zlic_type4.rename(columns={'license_type': '4 Star C 2C'})

    zlic_type1 = df_dc_fin.query('license_type == "1 Star C 2C"').groupby('zip').count()
    zlic_type1 = pd.DataFrame(zlic_type1)
    lcol = ['Facility Name', ' Infant', '1', '2', '3', '4', '5', '5-12', 'ALL', 'lic_max', 'pk_tot',
            'Interpolated Longitude, Latitude', 'address', 'city', 'state', 'Tract', 'SCC']
    for l in lcol:
        del zlic_type1[l]
    zlic_type1 = zlic_type1.rename(columns={'license_type': '1 Star C 2C'})

    zlic_typetc = df_dc_fin.query('license_type == "Temp C"').groupby('zip').count()
    zlic_typetc = pd.DataFrame(zlic_typetc)
    lcol = ['Facility Name', ' Infant', '1', '2', '3', '4', '5', '5-12', 'ALL', 'lic_max', 'pk_tot',
            'Interpolated Longitude, Latitude', 'address', 'city', 'state', 'Tract', 'SCC']
    for l in lcol:
        del zlic_typetc[l]
    zlic_typetc = zlic_typetc.rename(columns={'license_type': 'Temp C'})

    zlic_typeO = df_dc_fin.query('license_type == "Other"').groupby('zip').count()
    zlic_typeO = pd.DataFrame(zlic_typeO)
    lcol = ['Facility Name', ' Infant', '1', '2', '3', '4', '5', '5-12', 'ALL', 'lic_max', 'pk_tot',
            'Interpolated Longitude, Latitude', 'address', 'city', 'state', 'Tract', 'SCC']
    for l in lcol:
        del zlic_typeO[l]
    zlic_typeO = zlic_typeO.rename(columns={'license_type': 'Other'})

    zlic_typePLC = df_dc_fin.query('license_type == "Prob Lic C"').groupby('zip').count()
    zlic_typePLC = pd.DataFrame(zlic_typePLC)
    lcol = ['Facility Name', ' Infant', '1', '2', '3', '4', '5', '5-12', 'ALL', 'lic_max', 'pk_tot',
            'Interpolated Longitude, Latitude', 'address', 'city', 'state', 'Tract', 'SCC']
    for l in lcol:
        del zlic_typePLC[l]
    zlic_typePLC = zlic_typePLC.rename(columns={'license_type': 'Prob Lic C'})

    zlic_typeSPC = df_dc_fin.query('license_type == "SProv C"').groupby('zip').count()
    zlic_typeSPC = pd.DataFrame(zlic_typeSPC)
    lcol = ['Facility Name', ' Infant', '1', '2', '3', '4', '5', '5-12', 'ALL', 'lic_max', 'pk_tot',
            'Interpolated Longitude, Latitude', 'address', 'city', 'state', 'Tract', 'SCC']
    for l in lcol:
        del zlic_typeSPC[l]
    zlic_typeSPC = zlic_typeSPC.rename(columns={'license_type': 'SProv C'})

    zlic_type_all = pd.concat(
        [zlic_type5, zlic_type4, zlic_type3, zlic_type1, zlic_typetc, zlic_typeO, zlic_typePLC, zlic_typeSPC], axis=1,
        sort=False)

    zlic_type_all = zlic_type_all.fillna(0)
    zlic_type_all["other_license"] = zlic_type_all['Temp C'] + zlic_type_all['Other'] + zlic_type_all['Prob Lic C'] + \
                                     zlic_type_all['SProv C']
    olic = ['Temp C', 'Other', 'Prob Lic C', 'SProv C']
    for l in olic:
        del zlic_type_all[l]
    stzip = str(zipcode)
    zlic_zip = zlic_type_all.query('index == @stzip')

    lics = ['5 Star', '4 Star', '3 Star', '1 Star', 'Other']
    nums = [int(zlic_zip['5 Star C 2C']), int(zlic_zip['4 Star C 2C']), int(zlic_zip['3 Star C 2C']),
            int(zlic_zip['1 Star C 2C']), int(zlic_zip['other_license'])]
    x_pos = [i for i, _ in enumerate(lics)]
    fig5 = plt.figure()
    plt.bar(x_pos, nums)
    plt.xticks(x_pos, lics)
    plt.xlabel("License Type")
    plt.ylabel("Number of Licenses")
    plt.title("Number of Licenses Currently in the Zipcode")
    dc_bar = mpld3.fig_to_html(fig5)

    df_income = df_income.rename(columns={'Tract Code': 'tract', 'Tract Income Level': "ilevel",
                                          '2019 Est. Tract Median Family Income': 'med_income'})
    df_income.med_income = df_income.med_income.apply(lambda x: x.strip("$"))
    df_income.med_income = df_income.med_income.apply(lambda x: x.replace(",", ''))
    df_income.med_income = df_income.med_income.astype(int)
    tract = data.census_tract
    lg2 = len(df_income)
    tincome = df_income.groupby('tract').med_income.min().nsmallest(lg2)
    n = rank(list(tincome.index), tract)
    perc = int((n / lg2) * 100)
    df_ti = df_income.query('tract == @tract')
    m_inc = int(df_ti.med_income)
    def th_ending(n):
        l = []
        for d in str(n):
            l.append(d)
        print(l[-1])
        if l[-1] == '1':
            per = f"{n}st"
        elif l[-1] == '2':
            per = f"{n}nd"
        elif l[-1] == '3':
            per = f"{n}rd"
        else:
            per = f"{n}th"
        return per
    percentile = th_ending(perc)
    lev = df_ti['ilevel'].max()
    per_mes = f"Census Tract {tract}: {lev} Income Level. This tract falls in the {percentile} percentile for median income among tracts in Wake County."

    # USE: Create an array structure for rings.
    # INPUT: a df of row length 1 with the first column as the current metric value and the second colum is the target metric value
    # OUTPUT: an aray of arrays representing each ring
    def calculate_rings(first, second, pending):
        if first < second and first + pending <= second:
            rings = [[first, pending, second - first - pending]]
        elif first < second and first + pending > second:
            rings = [[first, second - first, 0]]
        else:
            rings = [[1, 0, 0]]
        return rings

    # USE: Determine if the label for the rotating number label should be left/center/right
    # INPUT: a df of row length 1 with the first column as the current metric value and the second colum is the target metric value
    # OUTPUT: the proper text alignment
    def horizontal_aligner(first, second):
        metric = 1.0 * first % second / second
        if metric in (0, 0.5):
            align = 'center'
        elif metric < 0.5:
            align = 'left'
        else:
            align = 'right'
        return align

    def vertical_aligner(first, second):
        metric = 1.0 * first % second / second
        if metric < 0.25:
            align = 'bottom'
        elif metric < 0.75:
            align = 'top'
        elif metric > 0.75:
            align = 'bottom'
        else:
            align = 'center'
        return align

    # USE: Create a center label in the middle of the radial chart.
    # INPUT: a df of row length 1 with the first column as the current metric value and the second column is the target metric value
    # OUTPUT: the proper text label
    def add_center_label(first, second):
        # percent = str(round(1.0 * first / second * 100, 1)) + '%'
        label = 'Median Income:'
        return plt.text(0,
                        0.3,
                        label,
                        horizontalalignment='center',
                        verticalalignment='center',
                        fontsize=24,
                        family='sans-serif')

    # USE: Formats a number with the apropiate currency tags.
    # INPUT: a currency number
    # OUTPUT: the properly formmated currency string
    def get_currency_label(num):
      currency = ''
      if num < 10**3:
        currency = '$' + str(num)
      elif num < 10**6:
          currency = '$' + str(round(1.0*num/10**3,1)) + 'K'
      elif num < 10**9:
        currency = '$' + str(round(num/10**6,1)) + 'M'
      else:
        currency = '$' + str(round(num/10**9,1)) + 'B'

      return currency

    def get_percent_label(num):
        currency = ''
        if num < 10 ** 3:
            currency = str(num) + "%"
        elif num < 10 ** 6:
            currency = str(round(1.0 * num / 10 ** 3, 1)) + 'K' + "%"
        elif num < 10 ** 9:
            currency = str(round(num / 10 ** 6, 1)) + 'M' + "%"
        else:
            currency = str(round(num / 10 ** 9, 1)) + 'B' + "%"

        return currency

    # USE: Create a dynamic outer label that servers a pointer on the ring.
    # INPUT: a df of row length 1 with the first column as the current metric value and the second column is the target metric value
    # OUTPUT: the proper text label at the apropiate position
    def add_current_label(first, second, percentile):
        percent = f"{percentile} PCTL"

        return plt.text(1.5 * np.cos(0.5 * np.pi - 2 * np.pi * (first / second)) if first < second else 0,
                        1.5 * np.sin(0.5 * np.pi - 2 * np.pi * first / second) if first < second else 1.5,
                        percent,
                        horizontalalignment=horizontal_aligner(first, second) if first < second else 'center',
                        verticalalignment=vertical_aligner(first, second) if first < second else 'bottom',
                        fontsize=16,
                        family='sans-serif')

    def add_sub_center_label(m_inc):
        amount = get_currency_label(m_inc)
        return plt.text(0,
                        -.1,
                        amount,
                        horizontalalignment='center',
                        #             verticalalignment='top',
                        verticalalignment='center',
                        fontsize=22, family='sans-serif')

    #######################################################################
    ###                                                    MAIN FUNCTION                                                        ###
    #######################################################################

    def chart(current, goal, m_inc, perc, pipeline=0, colors=["black", 'gray', 'lightgray'], overachiever_color='#0c561d', width=5,
              height=5, dpi=100):

        first = current
        second = goal

        # base styling logic
        ring_width = 0.3
        outer_radius = 1.5
        inner_radius = outer_radius - ring_width

        # set up plot
        ring_arrays = calculate_rings(first, second, pipeline)
        fig, ax = plt.subplots(figsize=(width, height), dpi=dpi)
        ax = fig.add_axes([0, 0, 1, 1])
        if first >= second:
            outer_edge_color = None
            inner_edge_color = 'white'
            colors = [overachiever_color, 'white', 'white']
        else:
            outer_edge_color, inner_edge_color = ['white', None]

        # plot logic
        outer_ring, _ = ax.pie(ring_arrays[0], radius=1.5,
                               colors=colors,
                               startangle=90,
                               counterclock=False)

        # add labels
        add_center_label(first, second)
        add_current_label(first, second, perc)
        add_sub_center_label(m_inc)
        plt.setp(outer_ring, width=ring_width, edgecolor=outer_edge_color)
        ax.xaxis.set_visible(False)
        ax.yaxis.set_visible(False)
        plt.margins(.2, .2)
        plt.autoscale('enable')

        return fig

    # TODO: EDIT these to reflect where the variables exist in your data frame

    current = float(n)  # float(df.iloc[0,0]
    goal = float(lg2)  # float(df.iloc[0,1]
    m_inc = m_inc
    percentile = percentile

    # this is an optional parameter if you do have pipeline
    pipeline = float(30)  # float(df.iloc[0,1]

    # fig6 = plt.figure()
    # fig6 = plt.title("Percentile of the Census Tract")
    fig6 = chart(current, goal, m_inc, perc=percentile, pipeline=0, colors=["green", 'yellow', 'lightgreen'], overachiever_color='#0c561d', width=5,
          height=5, dpi=100)
    circle_chart = mpld3.fig_to_html(fig6)
    # https://support.sisense.com/hc/en-us/community/posts/360038303453-Radial-Bar-Chart-with-Pending-Pipeline

    context = {
        'data': data,
        'map': map,
        'zlic_zip': zlic_zip,
        'my_add_zip': [my_add_zip],
        'my_zip_stats': [my_zip_stats],
        'RankState': RankState,
        'zip_comp_bar': [zip_comp_bar],
        'dc_bar': [dc_bar],
        'circle_chart': [circle_chart],
        'per_mes': per_mes,
        'needsState': needsState
    }

    return render_template('tract_profile.html', **context)

