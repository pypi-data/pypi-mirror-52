from __future__ import absolute_import, division, print_function

def get_sims_from_exp(client, experiment_id):
    # given a database client and experiment id, return a list of simulation ids
    simulation_ids = set()
    query_dict = {'experiment_id': experiment_id}
    data = client.find(query_dict)
    for row in data:
        simulation_id = row['simulation_id']
        simulation_ids.add(simulation_id)
    return list(simulation_ids)

def db_to_dict(data, data_keys):
    # organize data into a dict
    data_dict = {key: {} for key in data_keys}
    time_vec = []
    for row in data:
        time_vec.append(row['time'])
        for key in data_dict.iterkeys():
            key_row = row[key]
            for mol_id, value in key_row.iteritems():
                if mol_id in data_dict[key].keys():
                    data_dict[key][mol_id].append(value)
                else:
                    data_dict[key][mol_id] = [value]
    data_dict['time'] = time_vec

    return data_dict