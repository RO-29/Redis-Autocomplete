import csv
import pdb
from redis_util import RedisHelper
import json


#zrangebylex rev_ad [hdfc:de "[hdfc:de\xff"
f = open('raw_data_bank.csv', 'r')

"""
    Structure of bank_details:
    { bank_name: {city : [{ifsc:code, branch: name, address:details, district:name, state:name, bank_id: ID }, ...] }
    , .... }
    
    Structure of bank_id_mapping :
    {bank_name : "bINDEX1", bank_name_2:"bINDEX2",...}

    Structure of bank_city_autocompete:
    [bank_id:city_name, bank-id2:city_name2,....]
"""

bank_details = {}
bank_id_mapping = {}
bank_index = 1
bank_city_autocompete = []


try:
    reader = csv.reader(f);
    #Pop metadata
    reader.next()

    for row in reader:
        ifsc, bank_id, branch, address, city, district, state ,bank_name = row[0], row[1], row[2], row[3],row[4], row[5], row[6], row[7]
        if bank_name not in bank_details:
            bank_id_mapping[bank_name] = "b{id}".format(id = bank_index)
            bank_details[bank_name] = {}
            bank_index+=1

        if city not in bank_details[bank_name]:
            bank_details[bank_name][city] = []
            bank_city_autocompete.append('{bank_id}:{city_name}'.format(bank_id = bank_id_mapping[bank_name], city_name = city))
            
        #map bank-details
        bank_details[bank_name][city].append({"ifsc":ifsc, "bank_id": bank_id, "branch": branch, "address":address, "district":district, "state":state })

finally:
    f.close()


#Pre-Load bank+city-- all branches data in redis
for bank_name in bank_details.keys():
    RedisHelper().set_redis_hash(bank_id_mapping[bank_name], bank_details[bank_name])

#Load all bank_id_mappings in redis
RedisHelper().set_redis_hash("bank_id_mapping", bank_id_mapping)

#load autocompete index in redis
#with zero score for all city so as to use zrangebylex
autocompete_dictonary_score = { value:0 for value in bank_city_autocompete}
RedisHelper().set_sorted_list("autocompete", autocompete_dictonary_score)
