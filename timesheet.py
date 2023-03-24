import streamlit as st
from streamlit_extras.no_default_selectbox import selectbox
from store import *
from datetime import datetime
import calendar
import streamlit_authenticator as stauth  # pip install streamlit-authenticator
import pickle
from pathlib import Path
from database import *



page_title = "Attendance Tracker"
page_icon = ":hourglass_flowing_sand:"  # emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
layout = "centered"
st.set_page_config(page_title=page_title, page_icon=page_icon, layout=layout)

st.markdown("""<link href="https://fonts.googleapis.com/css2?family=Julius+Sans+One&family=Secular+One&family=Monoton&family=Nunito:ital,wght@0,200;0,300;0,400;0,500;0,600;1,300;1,400;1,500;1,600&family=Share+Tech+Mono&family=Tilt+Prism&family=Tilt+Warp&display=swap" rel="stylesheet">""",
            unsafe_allow_html=True)

# --- USER AUTHENTICATION ---
entry_table =process_entry()
names = entry_table['Staff_Name'].tolist()
usernames = entry_table['Username'].tolist()


# load hashed passwords
file_path = Path(__file__).parent / "hashed_pw.pkl"
with file_path.open("rb") as file:
    hashed_passwords = pickle.load(file)

authenticator = stauth.Authenticate(names, usernames, hashed_passwords,
    "timesheet", "abc", cookie_expiry_days=0.00208333333)

name, authentication_status, username = authenticator.login("Login", "main")

if authentication_status == False:
    st.error("Username/password is incorrect")

if authentication_status == None:
    st.warning("Please enter your username and password")


  

if authentication_status:
  
    location = get_geolocation('Get location')
    
    with open("style.css")as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True)
    

    st.header("Attendance Tracker")
    showtimer()
    table =process_data()

    dt = datetime.now()
    weekends =['Saturday','Sunday']
    day_name = calendar.day_name[dt.weekday()]
    currentDT = datetime.now()

    def error_message(message):
        st.error(message)
        authenticator.logout("Log Out", "main")
        st.stop()
    

    def success_message(message):
        my_bar = st.progress(0)
        for p in range(100):
            time.sleep(0.02)
            my_bar.progress(p+1)
        st.success(message)
        authenticator.logout("Log Out", "main")

    # LGA
    main_container = st.container()
    with main_container:
            station= selectbox(
            'Are you in your Station?',('Yes', 'No'))
            

            placeholder = st.empty()
            placeholder2 = st.empty()
            if (station=="Yes"):

                with placeholder.container():
                    facility = selectbox(
                    'Select the facility you are in Currently?',
                    list(table[table['Staff_Name']==name]['facility'].unique()),no_selection_label="")
                    
                    # side1, side2 = st.columns(2)
                    cols = st.columns(2)
                    cols[0].button('Clock In', key='Clock_in',use_container_width=True)
                    cols[1].button('Clock Out', key='Clock_out',use_container_width=True)

                    ChangeButtonColour('Clock In', '#DC4F3C', 'white') # button txt to find, colour to assign
                    ChangeButtonColour('Clock Out', 'white', '#DC4F3C') # button txt to find, colour to assign

                  
                    

                    if st.session_state["Clock_in"]:
                        if(facility is None ):
                            st.error("Please select the facility you are currently")
                            st.stop()
                        else:
                            # if ((day_name not in weekends) and ( currentDT.hour >8 and currentDT.hour <12 )):
                            if (facility):
                                filtered_df = table.loc[(table['Staff_Name']==name) & (table['facility']==facility)]
                                collections =getdetails(filtered_df,'Position','LGA',location, name, username, facility)
                                key = collections['date'] + username
                                if get_Keys(key) is  None:
                                    clockout={}
                                    insert_clockin(key,collections,clockout)
                                    success_message("You are now clocked in successfully")
                                else:
                                    error_message("You are clocked in already")
                                   
                            else:
                                error_message("You can't Clock in Now")
                              
                    
                    if st.session_state["Clock_out"]:
                        if(facility== None ):
                            st.error("Please select the facility you are currently")
                            st.stop()
                        else:
                            # (day_name not in weekends) and
                            # if ( (currentDT.hour >12 and currentDT.hour <19)):
                            if ( facility):
                                filtered_df = table.loc[(table['Staff_Name']==name) & (table['facility']==facility)]
                                clockout, reason=(True, False)
                                
                                updates =getdetails(filtered_df,'Position','LGA',location, name, username, facility,reason, clockout)
                                # def getdetails(df,pos,lga,loc, name, username, facility= None, reason=None, clockout=False):
                                key = updates['clockout.date_out'] + username
                                try:
                                    if bool(fetch_clockout(key)['clockout']) ==False:
                                        update_clockout(key, updates)
                                        success_message("You are now clocked out successfully")
                                    else:
                                        error_message("You have Clocked Out already")
                                except (TypeError,KeyError):
                                    error_message("You Can't clock out Now")

                            else:
                                error_message("You Can't clock out Now")
  
            if (station=="No"):
                with placeholder2.container():
                    explain =st.text_area(
                            "", placeholder="Please Explain why you are not in your station")     
                    submitted = st.button("Submit Response",use_container_width=True)

                    if submitted:

                        if(len(explain) < 20 ):
                            st.error("Please provide a deatiled  explanation")
                            st.stop()

                        filtered_df = table.loc[(table['Staff_Name']==name) ]
                        facility, clockout=(None, False)
                        collections =getdetails(filtered_df,'Position','LGA',location, name, username,facility,  explain,clockout)
                        collections["longitude"] = None
                        collections["latitude"] = None
                        key = collections['date'] + username
                        clockout, reason=(True, False)
                       
                        if get_Keys(key) is  None :
                            closeout=None
                            insert_clockin(key,collections,closeout)
                            success_message("You response is submitted successfully")
                             
                        else:
                            st.error("You have submitted response already")
                           



                            
                     
                            
                            
                    
                    


       