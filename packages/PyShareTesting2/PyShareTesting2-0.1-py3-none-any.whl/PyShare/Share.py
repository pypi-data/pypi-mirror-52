import time
import subprocess

def getShare(share_x):
    # Pre-Check
    if 'Address1' not in share_x.columns:
        raise ValueError("Address1 column must be provided")
    elif 'City' not in share_x.columns:
        raise ValueError("City column must be provided")
    elif 'State' not in share_x.columns:
        raise ValueError("State column must be provided")
    elif 'Zipcode' not in share_x.columns:
        raise ValueError("Zipcode column must be provided")
    elif 'RowID' in share_x.columns:
        raise ValueError("RowID column name cannot be in dataframe")

    # Add Row ID
    share_x['RowID'] = share_x.index

    # Create Dataframe to Send to Java
    JavaDF = share_x.loc[:,share_x.columns.isin(['Address1','Address2','City','State','Zipcode','Province','Country','RowID'])]

    file_directory = r'C:\Users\5117620\Downloads'
    file_name = int(time.time())

    # Set Input and Output
    input_file = '{}\{}.txt'.format(file_directory,file_name)
    output_file = '{}\{}_complete.txt'.format(file_directory,file_name)

    JavaDF.to_csv(input_file, header=True, index=False, sep='|')

    #subprocess.call(['java', '-jar', 'jarname.jar', input_file, output_file])

    # Cleanup
    del share_x['RowID']






