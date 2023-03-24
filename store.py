import streamlit as st
import pandas as pd
from streamlit.components.v1 import html
import socket
from streamlit_js_eval import get_geolocation
from datetime import datetime
from datetime import date
import time
import streamlit_authenticator as stauth 
import streamlit.components.v1 as components



@st.cache_data ()
def process_entry():
    df =pd.read_pickle('use_list.pkl')
    return df
    

def showtimer():
    my_html = """
    <script>
    function showTime(){
        var date = new Date();
        var h = date.getHours(); // 0 - 23
        var m = date.getMinutes(); // 0 - 59
        var s = date.getSeconds(); // 0 - 59
        var session = "AM";
        
        if(h == 0){
            h = 12;
        }
        
        if(h > 12){
            h = h - 12;
            session = "PM";
        }
        
        h = (h < 10) ? "0" + h : h;
        m = (m < 10) ? "0" + m : m;
        s = (s < 10) ? "0" + s : s;
        
        var time = h + ":" + m + ":" + s + " " + session;
        document.getElementById("MyClockDisplay").innerText = time;
        document.getElementById("MyClockDisplay").textContent = time;
        
        setTimeout(showTime, 1000);
        
    }

    window.onload = function () {

        showTime();
    };
    </script>

    <body>
    <h3 id="MyClockDisplay" style="font-family:'Arial'; color:white;font-size:50px;margin-top:-2vh; text-align:center;"></h3>
    </body>
    """

    html(my_html)

@st.cache_data ()
def process_data():
    df =pd.read_pickle('staff_list.pkl')
    return df

def getdetails(df,pos,lga,loc, name, username, facility= None, reason=None, clockout=False):
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    location2 = loc['coords']
    timestamp = loc["timestamp"]
    time_in=str(datetime.fromtimestamp(timestamp // 1000))
    if clockout:
       return  {
        "clockout.device_out":hostname,
        "clockout.ip_address_out":ip_address,
        "clockout.facility_out":facility,
        "clockout.date_out":str(time_in).split(' ')[0],
        "clockout.time_out":timestamp,
        "clockout.long_out":location2["longitude"],
        "clockout.lat_out":location2["latitude"],
        }

    else:
     return   {
        "device_name":hostname,
        "ip_address":ip_address,
        "designation":df[pos].values[0],
        "LGA":df[lga].values[0],
        "time_in": timestamp,
        "longitude":location2["longitude"],
        "latitude":location2["latitude"],
        "date":str(time_in).split(' ')[0],
        "staff_name":name,
        "username":username,
        "facility_in":facility,
        "reason":reason,
     
    }
 
    
    


 
 


def ChangeButtonColour(widget_label, font_color, background_color='transparent'):
    htmlstr = f"""
        <script>
            var elements = window.parent.document.querySelectorAll('button');
            for (var i = 0; i < elements.length; ++i) {{ 
                if (elements[i].innerText == '{widget_label}') {{ 
                    elements[i].style.color ='{font_color}';
                    elements[i].style.background = '{background_color}'
                }}
            }}
        </script>
        """
    html(f"{htmlstr}", height=0, width=0)

