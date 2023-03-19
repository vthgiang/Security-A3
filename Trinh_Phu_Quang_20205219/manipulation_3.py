import mysql.connector
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

def print_top_five_drive():
    # Create a cursor object
    mycursor = mydb.cursor()
    try:
        People = int(input("Maximum people you work with \n(only you then enter 1): "))
    except ValueError:
        People = 10000000
    print("\n")
    try:
        Money = int(input("The maximum amount of money you want to spend per_month(in $): "))
    except:
        Money = 100000000
    print("\n")
    try:
        Capacity = int(input("Minimum capacity you need(in Gb): "))
    except:
        Capacity = 0
    print("\n")
    option = input("Do you need any other specific requirement? Y/n: ")
    print("\n")
    if (option == "Y" or option == "y"):
        # Use the SELECT DISTINCT statement to retrieve unique values from the MOption column
        mycursor.execute("SELECT DISTINCT MOption FROM MoreDriveOption")

        # Fetch the results using the cursor's fetchall() method
        results = mycursor.fetchall()

        # Iterate through the results and print each MOption value
        print("Here is all the addition option we have in our database: \n")
        for result in results:
            print("+ ",result[0])
        Moreoption = input("Enter the Option you want: ")
        mycursor.execute("""
        SELECT ProviderDriveOption.ProverderOpID, ProviderDriveOption.ProviderName, ProviderDriveOption.Price, ProviderDriveOption.Capacity, AVG((AveragePoint + GetAppPoint)/2) as average
        FROM ProviderDriveOption
        JOIN ProType ON ProType.ProviderName = ProviderDriveOption.ProviderName
        JOIN MoreDriveOption ON MoreDriveOption.ProverderOpID = ProviderDriveOption.ProverderOpID
        WHERE MaxPeople <= %s AND Price <= %s And Capacity >= %s and MOption = %s
        GROUP BY ProviderDriveOption.ProverderOpID, ProviderDriveOption.ProviderName
        """, (People, Money, Capacity, Moreoption))
    else:
        mycursor.execute("""
        SELECT ProviderDriveOption.ProverderOpID, ProviderDriveOption.ProviderName, ProviderDriveOption.Price, ProviderDriveOption.Capacity, AVG((AveragePoint + GetAppPoint)/2) as average
        FROM ProviderDriveOption
        JOIN ProType ON ProType.ProviderName = ProviderDriveOption.ProviderName
        JOIN MoreDriveOption ON MoreDriveOption.ProverderOpID = ProviderDriveOption.ProverderOpID
        WHERE MaxPeople <= %s AND Price <= %s And Capacity >= %s 
        GROUP BY ProviderDriveOption.ProverderOpID, ProviderDriveOption.ProviderName
        """, (People, Money, Capacity))

    #----------------------------------------------------------------------

    result = mycursor.fetchall()
    if not result:
        print("There are no suitable provider for you now, please Re-Enter the value you want for Cloud option")
        mycursor.close()
        return
    
    # Count the total number of ProviderName and ProviderOpID
    mycursor.execute("SELECT COUNT(DISTINCT ProviderName), COUNT(DISTINCT ProverderOpID) FROM ProviderDriveOption")
    count_result = mycursor.fetchone()
    print("\nFrom {} Provider with {} Cloud Option from our database, here is the best option ".format(count_result[0],count_result[1]))

    update_list = []
    for row in result:
        proverder_op_id = row[0]
        provider_name = row[1]
        price = row[2]
        capacity = row[3]
        average = row[4]
        update_list.append((average, proverder_op_id, provider_name, price, capacity))

    update_list.sort(reverse=True, key=lambda x: x[0])
    top_five = update_list[:5]
    for avg, proverder_op_id, provider_name, price, capacity  in top_five:
        print("Provider Name: {}, ProverderOpID: {}, Price: {}, Capacity: {}, Average: {}".format(provider_name, proverder_op_id ,price, capacity , avg))
    mycursor.close()

def print_top_five_host():
    # Create a cursor object
    mycursor = mydb.cursor()
    try:
        Money = int(input("The maximum amount of money you want to spend per_month(in $): "))
    except:
        Money = 100000000
    print("\n")  
    try:
        Capacity = int(input("Minimum capacity you need(in Gb): "))
    except:
        Capacity = 0
    print("\n")

    try:
        Core = int(input("Minimum CPU core you need: "))
    except:
        Core = 0
    print("\n")
    try:
        Ram = int(input("Minimum Ram you need(in Gb): "))
    except:
        Ram = 0
    print("\n")
    try:
        Bandwidth = int(input("Minimum BandWidth you need a month(in Gb): "))
    except:
        Bandwidth = 0
    print("\n")
    #Addition option
    option = input("Do you need any other specific requirement? Y/n: ")
    print("\n")
    if (option == "Y" or option == "y"):
        # Use the SELECT DISTINCT statement to retrieve unique values from the MOption column
        mycursor.execute("SELECT DISTINCT MOption FROM MoreHostOption")

        # Fetch the results using the cursor's fetchall() method
        results = mycursor.fetchall()

        # Iterate through the results and print each MOption value
        print("Here is all the addition option we have in our database: \n")
        for result in results:
            print("+ ",result[0])
        Moreoption = input("Enter the Option you want: ")
        mycursor.execute("""
        SELECT ProviderHostOption.ProverderOpID, ProviderHostOption.ProviderName, ProviderHostOption.Price, ProviderHostOption.Core, ProviderHostOption.RAM, ProviderHostOption.Bandwidth,ProviderHostOption.Capacity, AVG((AveragePoint + GetAppPoint)/2) as average
        FROM ProviderHostOption
        JOIN ProType ON ProType.ProviderName = ProviderHostOption.ProviderName
        JOIN MoreHostOption ON MoreHostOption.ProverderOpID = ProviderHostOption.ProverderOpID
        WHERE Price <= %s And Capacity >= %s  And Core >= %s And RAM >= %s  And Bandwidth >= %s And MOption = %s
        GROUP BY ProviderHostOption.ProverderOpID, ProviderHostOption.ProviderName
        """, (Money, Capacity, Core, Ram, Bandwidth, Moreoption))
    else:
        mycursor.execute("""
        SELECT ProviderHostOption.ProverderOpID, ProviderHostOption.ProviderName, ProviderHostOption.Price, ProviderHostOption.Core, ProviderHostOption.RAM, ProviderHostOption.Bandwidth,ProviderHostOption.Capacity, AVG((AveragePoint + GetAppPoint)/2) as average
        FROM ProviderHostOption
        JOIN ProType ON ProType.ProviderName = ProviderHostOption.ProviderName
        JOIN MoreHostOption ON MoreHostOption.ProverderOpID = ProviderHostOption.ProverderOpID
        WHERE Price <= %s And Capacity >= %s  And Core >= %s And RAM >= %s  And Bandwidth >= %s   
        GROUP BY ProviderHostOption.ProverderOpID, ProviderHostOption.ProviderName
        """, (Money, Capacity, Core, Ram, Bandwidth))

    #----------------------------------------------------------------------
    
    result = mycursor.fetchall()
    if not result:
        print("There are no suitable provider for you now, please Re-Enter the value you want for Cloud option")
        mycursor.close()
        return

    # Count the total number of ProviderName and ProviderOpID
    mycursor.execute("SELECT COUNT(DISTINCT ProviderName), COUNT(DISTINCT ProverderOpID) FROM ProviderHostOption")
    count_result = mycursor.fetchone()
    print("\nFrom {} Provider with {} Cloud Option from our database, here is the best option ".format(count_result[0],count_result[1]))
    update_list = []
    for row in result:
        proverder_op_id = row[0]
        provider_name = row[1]
        price = row[2]
        CPUs = row[3]
        Rams = row[4]
        Bands = row[5]
        capacity = row[6]
        average = row[7]
        update_list.append((average, proverder_op_id, provider_name, price, CPUs, Rams, Bands, capacity ))
        
    print("Top option and provider for you base on what you need:")
    update_list.sort(reverse=True, key=lambda x: x[0] if x[0] is not None else 0)

    top_five = update_list[:5]
    for avg, proverder_op_id, provider_name, price, CPUs, Rams, Bands, capacity  in top_five:
        print("Provider Name: {}, ProverderOpID: {}, Price: {}, CPU_core: {}, Ram: {}Gb, Bandwidth {}Gb, Capacity: {} ,Average: {}".format(provider_name, proverder_op_id, price, CPUs, Rams, Bands,capacity , avg))
    mycursor.close()

# Connect to the database
mydb = connect_to_database()

print("1. Search for Cloud Storage Provider \n2. Search for Hosting Provider ")
choose = input("Your the Number of your choose: ")
if (choose == "1"):
    print("If you NOT SURE how much you need or DON'T CARE of about the question, press Enter\n")
    print_top_five_drive()
elif (choose == "2"):
    print("If you NOT SURE how much you need or DON'T CARE of about the question, press Enter\n")
    print_top_five_host()
else:
    print("Wrong input, please rerun the program")
    exit()

mydb.close()