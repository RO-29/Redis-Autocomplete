import csv
import pdb
from redis_util import RedisHelper

f = open('raw_data_bank.csv', 'r')

"""
    Structure of bank_details:
    { bank_name: {city : [{ifsc:code, branch: name, address:details, district:name, state:name, bank_id: ID }, ...] }
    , .... }
    
"""
bank_details = {}
bank_city_mapping = {}

try:
    reader = csv.reader(f);
    #Pop metadata 
    #ifsc,bank_id,branch,address,city,district,state,bank_name
    reader.next()

    for row in reader:
        ifsc, bank_id, branch, address, city, district, state ,bank_name = row[0], row[1], row[2], row[3],row[4], row[5], row[6], row[7]
        if bank_name not in bank_details:
            bank_details[bank_name] = {}
            bank_city_mapping[bank_name] = []

        if city not in bank_details[bank_name]:
            bank_details[bank_name][city] = []
            bank_city_mapping[bank_name].append(city)
        
        bank_details[bank_name][city].append({"ifsc":ifsc, "bank_id": bank_id, "branch": branch, "address":address, 
                                            "district":district, "state":state })
finally:
    f.close()


for bank_name in bank_details.keys():
    RedisHelper().set_redis_hash(bank_name, bank_details[bank_name])
    RedisHelper().set_redis_list(bank_name +'_city', bank_city_mapping[bank_name])

RedisHelper().set_redis_list("bank_names", bank_details.keys())