import mysql.connector
from sklearn.cluster import KMeans
import numpy as np
def connect_to_database():
    # Read MySQL config from config.txt file
    with open("config.txt") as f:
        host = f.readline().strip()
        user = f.readline().strip()
        password = f.readline().strip()
        database = f.readline().strip()

    try:
        conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        if conn.is_connected():
            print('Connection Successful')
            return conn
    except mysql.connector.Error as e:
        print(f"Error connecting to MySQL: {e}") 
        exit()

def cluster_and_update(field_name, num_clusters, sort_order, checktype, table):
    query = f"SELECT {field_name} FROM {table}"
    mycursor.execute(query)
    field_values = [value[0] for value in mycursor.fetchall()]

    # Convert data to a NumPy array
    if sort_order == True:
        field_values = np.sort(field_values, axis=0, kind='quicksort')
    else:
        field_values = np.sort(field_values, axis=0, kind='quicksort')[::-1]
    field_values = np.array(field_values).reshape(-1, 1)

    # Cluster data using KMeans
    kmeans = KMeans(n_clusters=num_clusters, n_init=5)
    kmeans.fit_predict(field_values)

    # Zip the data and labels together
    clustered_data = list(zip(field_values, kmeans.labels_))

    # Re-labeling so that both data and labels are in ascending order
    old_label = -1
    new_label = 0
    for i, (value, label) in enumerate(clustered_data):
        if label != old_label:
            old_label = label
            new_label += 1
            label = new_label
            clustered_data[i] = (value, label)
        else:
            label = new_label
            clustered_data[i] = (value, label)

    # Iterate through the re-labeled data and update the appropriate field
    for value, label in clustered_data:
        if checktype == 0:
            values = (label, value[0])
            query = f"UPDATE {table} SET {field_name}Point=%s WHERE ROUND({field_name},4) = %s"
        else:
            values = (label, int(value[0]))
            query = f"UPDATE {table} SET {field_name}Point=%s WHERE {field_name} = %s"
        mycursor.execute(query, values)
        mydb.commit()

# Connect to the database
mydb = connect_to_database()
# Create a cursor object
mycursor = mydb.cursor()

#turn off safe mode
mycursor.execute("SET SQL_SAFE_UPDATES = 0")
mydb.commit()

#Set GbPerPrice in ProviderDriveOption table
mycursor.execute("Update ProviderDriveOption SET GbPerPrice=ROUND(Price/Capacity, 4)")
mydb.commit()

# Cluster and update all type of point
#format (field_name, num_clusters, sort_order, checktype, table_name)
#check type: 0 is float, 1 is int
cluster_and_update('Price', 5, False,0,'ProviderHostOption')
cluster_and_update('Core', 5, True,1,'ProviderHostOption')
cluster_and_update('Ram', 5, True,1,'ProviderHostOption')
cluster_and_update('Bandwidth', 5, True,1,'ProviderHostOption')
cluster_and_update('GbPerPrice', 5, True,0,'ProviderDriveOption')
cluster_and_update('MaxPeople', 5, True,1,'ProviderDriveOption')

#Update AveragePoint in each table
mycursor.execute("Update ProviderDriveOption SET AveragePoint = ROUND((GbPerPricePoint+MaxPeoplePoint)/2, 4)")
mydb.commit()
mycursor.execute("Update ProviderHostOption SET AveragePoint = ROUND((PricePoint+CorePoint+RamPoint+Bandwidthpoint)/4, 4)")
mydb.commit()

mycursor.execute("SELECT GetAppPoint FROM ProType WHERE GetAppPoint IS NOT NULL")
result = mycursor.fetchall()
total = sum([row[0] for row in result])
num_values = len(result)
average = total / num_values
mycursor.execute("UPDATE ProType SET GetAppPoint = %s WHERE GetAppPoint IS NULL", (average,))
mydb.commit()

mycursor.close()
mydb.close()