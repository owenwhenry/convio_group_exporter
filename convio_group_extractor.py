# -*- coding: utf-8 -*-
"""
Created on Mon Jul 10 09:45:40 2017

@author: owen.henry

The purpose of this script is to take a list of Convio groups that have been
selected for loading into an alternate CRM
"""

import csv
import convio_variables
import requests

#variables for the API
auth_token = convio_variables.auth_token
key = convio_variables.key
v = convio_variables.v

too_long_list = []

too_long_file = open('manual_backup.csv', 'w')
long_writer = csv.writer(too_long_file)
#Each of these files contains a list of group IDs that need to be exported'
target_files = ['backup_groups.csv', 'migration_groups.csv']


#Step 1: Open the file
for cur_file in target_files:    
    print('Starting work on %s' %cur_file)
    with open(cur_file, 'r', encoding="utf-8-sig") as groups_file:
        #step 2: iterate through the file for the IDs
        reader = csv.reader(groups_file)
        for row in reader:
            #Step 3: Initiate an API call for each ID number
            print('Calling API for group ID#%s' %row[0])
            payload = {'method': 'getGroupMembers', 'api_key': key, 'v': v, 
                       'group_id' : row[0], 'response_format': 'json', 
                       'fields' : 'cons_id', 'sso_auth_token' : auth_token}
            response = requests.post('https://secure.crs.org/site/CRConsAPI?',
                                     params = payload)
            data = response.json()
            #Step 4: if the number of people is too many, add to the list
            if int(data['getGroupMembersResponse']['total_number']) > 1000:
                too_long_list.append(row)
                long_writer.writerow(row)
"""
            elif int(data['getGroupMembersResponse']['total_number']) == 0:
                print('O member group, moving on')
            else:
                try:
                    file_name = 'group_' + row[0]
                    with open(file_name, 'w') as outfile:
                        the_writer = csv.DictWriter(outfile, fieldnames=['cons_id'])
                        for row_id in data['getGroupMembersResponse']['member']:
                            the_writer.writerow(row_id)
                except:
                    print(data)
"""
print(too_long_list)
too_long_file.close()
