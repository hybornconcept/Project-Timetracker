import pickle
from pathlib import Path
from store import process_entry

import streamlit_authenticator as stauth

data =process_entry()
names = data['Staff_Name'].tolist()
usernames = data['Username'].tolist()
passwords = data['Password'].tolist()


hashed_passwords = stauth.Hasher(passwords).generate()

file_path = Path(__file__).parent / "hashed_pw.pkl"
with file_path.open("wb") as file:
    pickle.dump(hashed_passwords, file)