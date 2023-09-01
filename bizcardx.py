# import easyocr
from PIL import Image
import os
import re
import numpy as np
import pandas as pd
import pymongo
import psycopg2
import streamlit as st
from streamlit_option_menu import option_menu
from io import BytesIO


st.set_page_config(page_title='BizcardX',
                   page_icon=':bar_chart:', layout="wide")
st.markdown(f'<h1 style="text-align: center;">BizCardX <br> Extracting Business Card Data with OCR</h1>',
            unsafe_allow_html=True)
st.write('')
st.write('')

pd.set_option('display.max_columns', None)


def data_extract_from_mongodb():
    gopi = pymongo.MongoClient(
        "mongodb+srv://gopiashokan:gopiroot@gopi.xdp3lkp.mongodb.net/?retryWrites=true&w=majority")
    db = gopi['bizcardx']
    col = db['image_data']

    data = []
    for i in col.find({}, {'_id': 0}):
        data.extend(i['data'])
    return data


def remove_all_files():
    folder_name = 'upload'
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    image_list = os.listdir(folder_name)

    for image in image_list:
        path = os.path.join(folder_name, image)
        try:
            os.remove(path)
        except:
            pass


def image_to_binary(image):
    folder_name = 'upload'
    image_list = os.listdir(folder_name)

    for image in image_list:
        path = os.path.join(folder_name, image)

    with open(path, "rb") as img_file:
        image_data = img_file.read()
        encoded_b2 = psycopg2.Binary(image_data)
        return encoded_b2


def image_decoded(image_name, user_name, password):
    gopi = psycopg2.connect(host='localhost',
                        user='postgres',
                        password='root',
                        database='bizcardx')
    cursor = gopi.cursor()
    cursor.execute(f"""select image from card_data
                        where image_name=%s and user_name=%s 
                        and password=%s;""",(image_name, user_name, password))
    image_data = cursor.fetchall()[0][0]

    # Create a BytesIO object to hold the image data
    image_d = BytesIO(image_data)

    # Open the image using PIL
    image = Image.open(image_d)
    return image


class image_to_text:

    def format(data):
        result = []
        for i in data:
            a = i.split(',')
            for j in a:
                if j != '':
                    b = j.split(';')
                    for k in b:
                        result.append(k.strip())
        return result

    def name_designation(data):
        name, designation = [], []

        if data[0] == data[0].upper():
            for i in data:
                if i == i.upper():
                    name.append(i)
                else:
                    designation.append(i)

        elif data[-1] == data[-1].upper():
            for i in data:
                if i == i.upper():
                    designation.append(i)
                else:
                    name.append(i)

        name = ' '.join(name)
        designation = ' '.join(designation)

        return name, designation

    def remove_name_designation(data):
        name_designation_r = data[1:]
        return name_designation_r

    def find_phone(data):
        phone = []
        phone_pattern = r"[+]?\d+-\d+-\d+"
        phone_numbers = re.findall(phone_pattern, ' '.join(data))
        phone.extend(phone_numbers)
        return phone

    def remove_phone(data):
        phone_r = []
        phone_pattern = r"[+]?\d+-\d+-\d+"
        for i in data:
            clear = re.sub(phone_pattern, '', i)
            if clear != '' and clear != ' ':
                phone_r.append(clear.strip())
        return phone_r

    def find_website(data):
        website = []
        web_pattern = r"[www|WWW|wWW|wwW|Www|WWw]+[\.|\s]+[a-zA-Z0-9]+[\.|\][a-zA-Z]+"
        web = re.findall(web_pattern, ' '.join(data))
        web_1 = re.sub("[www|WWW|wWW|wwW|Www|WWw]+\ ", "www.", web[0])
        web_2 = re.sub("[www|WWW|wWW|wwW|Www|WWw]+\.", "www.", web_1)
        website.append(web_2)
        return website

    def remove_website(data):
        website_r = []
        web_pattern = r"[www|WWW|wWW|wwW|Www|WWw]+[\.|\s]+[a-zA-Z0-9]+[\.|\][a-zA-Z]+"
        for i in data:
            clear = re.sub(web_pattern, '', i)
            if clear != '' and clear != ' ':
                website_r.append(clear.strip())
        return website_r

    def find_email(data):
        email = []
        email_pattern = r"[a-zA-Z0-9\.\-+_]+@[a-zA-Z0-9\.\-+_]+\.[a-z]+"
        email_id = re.findall(email_pattern, ' '.join(data))
        email.extend(email_id)
        return email

    def remove_email(data):
        email_r = []
        email_pattern = r"[a-zA-Z0-9\.\-+_]+@[a-zA-Z0-9\.\-+_]+\.[a-z]+"
        for i in data:
            clear = re.sub(email_pattern, '', i)
            if clear != '' and clear != ' ':
                email_r.append(clear.strip())
        return email_r


class data_extraction:

    data = data_extract_from_mongodb()

    formatted_data = image_to_text.format(data)

    name, designation = image_to_text.name_designation(
        formatted_data[0].split())
    data1 = image_to_text.remove_name_designation(formatted_data)

    # phone
    if len(image_to_text.find_phone(data1)) > 1:
        phone = image_to_text.find_phone(
            data1)[0] + ' / ' + image_to_text.find_phone(data1)[1]
    else:
        phone = image_to_text.find_phone(data1)[0]

    data2 = image_to_text.remove_phone(data1)

    website = image_to_text.find_website(data2)[0]
    data3 = image_to_text.remove_website(data2)

    email = image_to_text.find_email(data3)[0]
    data4 = image_to_text.remove_email(data3)

    company = data4[-1]
    data5 = data4[:-1]

    area = data5[0]
    data6 = data5[1:]

    city = data6[0]
    data7 = data6[1:]

    if len(data7)==1:
        state = data4[7].split()[0]
        pincode = data4[7].split()[1]
    elif len(data7)==2:
        state = data7[0]
        pincode = data7[1]


    user_data = {'company_name': company,
                 'card_holder_name': name,
                 'designation': designation,
                 'mobile_number': phone,
                 'email_address': email,
                 'website_url': website,
                 'area': area,
                 'city': city,
                 'state': state,
                 'pincode': pincode}

    display_data = {'Company Name': company,
                    'Card Holder Name': name,
                    'Designation': designation,
                    'Mobile Number': phone,
                    'Email Address': email,
                    'Website': website,
                    'Area': area,
                    'City': city,
                    'State': state,
                    'Pincode': pincode}


class sql:

    def create_table():
        gopi = psycopg2.connect(host='localhost',
                                user='postgres',
                                password='root',
                                database='bizcardx')
        cursor = gopi.cursor()
        cursor.execute(f"""create table if not exists card_data(
                                    image			 bytea,
                                    image_name		 varchar(255),
                                    company_name 	 varchar(255),
                                    card_holder_name varchar(255),
                                    designation		 varchar(255),
                                    mobile_number	 varchar(255),
                                    email_address	 varchar(255),
                                    website_url		 varchar(255),
                                    area			 varchar(255),
                                    city 			 varchar(255),
                                    state 			 varchar(255),
                                    pincode			 varchar(255),
                                    user_name   	 varchar(255),
                                    password		 varchar(255),
                                    unique (image_name,user_name,password));""")
        gopi.commit()


    def data_migrate_to_sql(card_image, image_name, user_name, password):

        gopi = psycopg2.connect(host='localhost',
                                user='postgres',
                                password='root',
                                database='bizcardx')
        cursor = gopi.cursor()

        data = data_extraction.display_data

        with st.form("Details"):
            company_name = st.text_input('Company Name:', value=data['Company Name'])
            card_holder_name = st.text_input('Card Holder Name:', value=data['Card Holder Name'])
            designation = st.text_input('Designation:', value=data['Designation'])
            mobile_number = st.text_input('Mobile Number:', value=data['Mobile Number'])
            email_address = st.text_input('Email Address:', value=data['Email Address'])
            website_url = st.text_input('Website:', value=data['Website'])
            area = st.text_input('Area:', value=data['Area'])
            city = st.text_input('City:', value=data['City'])
            state = st.text_input('State:', value=data['State'])
            pincode = st.text_input('Pincode:', value=data['Pincode'])

            submit_button = st.form_submit_button(label="Upload")

        if submit_button:
            final_data = {'image': card_image,
                          'image_name': image_name,
                          'company_name': company_name,
                          'card_holder_name': card_holder_name,
                          'designation': designation,
                          'mobile_number': mobile_number,
                          'email_address': email_address,
                          'website_url': website_url,
                          'area': area,
                          'city': city,
                          'state': state,
                          'pincode': pincode,
                          'user_name': user_name,
                          'password': password}
            df = pd.DataFrame([final_data])
            df_t = tuple(df.values.tolist()[0])

            cursor.execute(f"""insert into card_data(image, image_name, company_name, card_holder_name,
                                designation, mobile_number, email_address, website_url, area,
                                city, state, pincode, user_name, password)
                                values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);""", df_t)
            gopi.commit()
            st.success('Successfully data uploaded to Database')


    def get_image_name_list(user_name, password):
        gopi = psycopg2.connect(host='localhost',
                                user='postgres',
                                password='root',
                                database='bizcardx')
        cursor = gopi.cursor()
        cursor.execute(f"""select image_name from card_data
                            where user_name=%s and password=%s;""",(user_name, password))
        s = cursor.fetchall()
        s = [i[0] for i in s]
        s.sort(reverse=False)
        return s


    def get_record(image_name, user_name, password):
        gopi = psycopg2.connect(host='localhost',
                                user='postgres',
                                password='root',
                                database='bizcardx')
        cursor = gopi.cursor()
        cursor.execute(f"""select * from card_data
                            where image_name=%s and user_name=%s 
                            and password=%s;""",(image_name, user_name, password))
        s = cursor.fetchall()
        return s[0]


    def database_image_with_table(image_name, user_name, password):

        col1, col2 = st.columns(2, gap='large')
        with col1:
            st.subheader('Business Card Image')
            edit_image = image_decoded(option, user_name, password)
            st.image(edit_image)

        with col2:
            sql_data = sql.get_record(image_name, user_name, password)

            display_data = {'Company Name': sql_data[2],
                            'Card Holder Name': sql_data[3],
                            'Designation': sql_data[4],
                            'Mobile Number': sql_data[5],
                            'Email Address': sql_data[6],
                            'Website': sql_data[7],
                            'Area': sql_data[8],
                            'City': sql_data[9],
                            'State': sql_data[10],
                            'Pincode': sql_data[11]}
            # Transpose column to rows
            df = pd.DataFrame([display_data]).T
            html_table = df.to_html(header=False, index=True)

            # Display the HTML table using st.write()
            st.write(html_table, unsafe_allow_html=True)


    def delete_record(image_name, user_name, password):
        gopi = psycopg2.connect(host='localhost',
                                user='postgres',
                                password='root',
                                database='bizcardx')
        cursor = gopi.cursor()
        cursor.execute(f"""delete from card_data
                            where image_name=%s and user_name=%s 
                            and password=%s;""",(image_name, user_name, password))
        gopi.commit()


    def edit_record(image_name, user_name, password):
        sql_data = sql.get_record(image_name, user_name, password)

        gopi = psycopg2.connect(host='localhost',
                                user='postgres',
                                password='root',
                                database='bizcardx')
        cursor = gopi.cursor()
        
        with st.form("sql_record"):
            company_name = st.text_input('Company Name:', value=sql_data[2])
            card_holder_name = st.text_input('Card Holder Name:', value=sql_data[3])
            designation = st.text_input('Designation:', value=sql_data[4])
            mobile_number = st.text_input('Mobile Number:', value=sql_data[5])
            email_address = st.text_input('Email Address:', value=sql_data[6])
            website_url = st.text_input('Website:', value=sql_data[7])
            area = st.text_input('Area:', value=sql_data[8])
            city = st.text_input('City:', value=sql_data[9])
            state = st.text_input('State:', value=sql_data[10])
            pincode = st.text_input('Pincode:', value=sql_data[11])

            submit_button = st.form_submit_button(label="Update")

        if submit_button:
            final_data = {'image': sql_data[0],
                          'image_name': sql_data[1],
                          'company_name': company_name,
                          'card_holder_name': card_holder_name,
                          'designation': designation,
                          'mobile_number': mobile_number,
                          'email_address': email_address,
                          'website_url': website_url,
                          'area': area,
                          'city': city,
                          'state': state,
                          'pincode': pincode,
                          'user_name': user_name,
                          'password': password}
            
            df = pd.DataFrame([final_data])
            df_t = tuple(df.values.tolist()[0])

            sql.delete_record(image_name,user_name,password)

            cursor.execute(f"""insert into card_data(image, image_name, company_name, card_holder_name,
                                designation, mobile_number, email_address, website_url, area,
                                city, state, pincode, user_name, password)
                                values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""", df_t)
            gopi.commit()
            st.success('Updated Successfully')



# create option Menu

with st.sidebar:
    option = option_menu(menu_title=None,
                         options=['Extract','Upload', 'Edit', 'Delete', 'Exit'],
                         icons=['file', 'cloud-upload','pencil-square', 'gear', 'list-task'],
                         default_index=0,
                         orientation='vertical',
                         styles={'nav-link': {'font-size': '20px',
                                              'text-align': 'centre',
                                              'margin': '10px',
                                              '--hover-color': '#7F00FF'},
                                 'icon': {'font-size': '25px'},
                                 'container': {'max-width': '3000px'},
                                 'nav-link-selected': {'background-color': '#7F00FF'}})


if option == 'Extract':

    upload_image = st.file_uploader(label='Choose business card image',
                                    type=['png', 'jpg', 'jpeg'],
                                    accept_multiple_files=False)

    if upload_image:
        st.write('')
        col1, col2 = st.columns(2, gap='large')

        with col1:
            st.subheader('Business Card Image')
            img1 = Image.open(upload_image)

            image_name = upload_image.name
            remove_all_files()

            # Create a folder named 'uploads' if it doesn't exist
            if not os.path.exists('upload'):
                os.makedirs('upload')

            # Save the uploaded image to the folder
            path = 'upload/' + str(image_name)
            img1.save(path)

            img2 = img1.resize(size=(470, 300))
            st.image(img2)

        with col2:
            display_data = data_extraction.display_data

            # Transpose column to rows
            df = pd.DataFrame([display_data]).T
            html_table = df.to_html(header=False, index=True)

            # Display the HTML table using st.write()
            st.write(html_table, unsafe_allow_html=True)


elif option == 'Upload':
    image_list = os.listdir('upload')
    image_name = image_list[0]
    upload_image = Image.open('upload/'+str(image_name))

    col1, col2, col3 = st.columns(3)
    with col1:
        user_name = st.text_input(label='User Name')
    with col2:
        password = st.text_input(label='Password', type='password')

    if user_name and password:
        card_image = image_to_binary(upload_image)
        sql.create_table()
        try:
            sql.data_migrate_to_sql(card_image, image_name, user_name, password)
        except:
            col1, col2 = st.columns(2)
            with col1:
                st.warning('Data already exists')


elif option == 'Edit':
    col1, col2, col3 = st.columns(3)
    with col1:
        user_name = st.text_input(label='User Name')
    with col2:
        password = st.text_input(label='Password', type='password')

    if user_name and password:
        image_name_list = ['Select One']
        list1 = sql.get_image_name_list(user_name, password)
        image_name_list.extend(list1)
        
        if len(image_name_list)>1:
            col1,col2 = st.columns(2)
            with col1:
                option = st.selectbox('Select Image Name:', options=image_name_list)

            if option == 'Select One':
                pass
            else:
                st.write('')
                st.write('')
                sql.database_image_with_table(option, user_name, password)
                st.write('')
                st.write('')
                sql.edit_record(option, user_name, password)
        
        else:
            col1, col2 = st.columns(2)
            with col1:
                st.info("No Records Found")


elif option == 'Delete':
    try:
        col1, col2, col3 = st.columns(3)
        with col1:
            user_name = st.text_input(label='User Name')
        with col2:
            password = st.text_input(label='Password', type='password')

        if user_name and password:
            image_name_list = ['Select One']
            list1 = sql.get_image_name_list(user_name, password)
            image_name_list.extend(list1)

            if len(image_name_list)>1:
                col1,col2 = st.columns(2)
                with col1:
                    option = st.selectbox('Select Image Name:', options=image_name_list)
                    delete_button = st.button('Delete')

                if option == 'Select One':
                    pass
                else:
                    st.write('')
                    st.write('')
                    sql.database_image_with_table(option, user_name, password)
                    st.write('')
                    st.write('')

                if delete_button:
                    if option == 'Select One':
                        pass
                    else:
                        sql.delete_record(option, user_name, password)
                        col1, col2 = st.columns(2)
                        with col1:
                            st.success('Deleted Successfully')
            
            else:
                col1, col2 = st.columns(2)
                with col1:
                    st.info("No Records Found")
    except:
        pass


elif option == 'Exit':
    remove_all_files()
    gopi = psycopg2.connect(host='localhost',
                                user='postgres',
                                password='root',
                                database='bizcardx')
    cursor = gopi.cursor()
    gopi.close()

    st.success('Thank you for your time. Exiting the application')
    st.balloons()

