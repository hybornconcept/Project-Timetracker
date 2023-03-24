from deta import Deta  # Import Deta

# Initialize with a Project Key
deta = Deta("a0nizqblgvr_7csJryaMMnHsbGsBnBuQsUaMY5JvGfGQ")

# This how to connect to or create a database.
db_clockin = deta.Base("clockin_base")
# db_clockout = deta.Base("clockin_base")


# Returns the report on a successful creation, otherwise raises an error
def insert_clockin(key,data, clockout):
    return db_clockin.put({"key" :key,"data" :data, "clockout":clockout})

def update_clockout(key, updates):
# If the item is updated, returns None Otherwise,an exception is raised
    return db_clockin.update(updates, key)

# def insert_clockout(key,data) :
#     return db_clockout.put({"key" :key,"data" :data})

# If not found, the function will return None
def get_Keys(key):
    return db_clockin.get(key)

def fetch_clockout(key):
 return  db_clockin.get(key)
# def get_Keys_out(keys):
#     return db_clockout.get(keys)

