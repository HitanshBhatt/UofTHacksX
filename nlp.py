import os
import sys
import json
import cohere_util
from annoy import AnnoyIndex

RESOURCE_FILES = ['data/uoft.json', 'data/ontariotech.json']
ANNOY_NN_FILE = 'search.ann'
ANNOY_NN_RESOURCES = 'search.json'

if len(sys.argv) < 2:
    pass
elif sys.argv[1] == '-embed':
    # Build the embeds for each description
    for file_name in RESOURCE_FILES:
        if not os.path.exists(file_name):
            print("Couldn't find file {}.".format(file_name))
            continue
        with open(file_name, 'r') as f:
            resources = json.load(f)
    for i, resource in enumerate(resources):
        if 'embed' not in resource or not resource['embed']:
            resources[i]['embed'] = cohere_util.embed(resource['description'])
            # Write the updated changes to the file
            with open(file_name, 'w') as f:
                json.dump(resources, f)
elif sys.argv[1] == '-knn':
    all_resources=[]
    for file_name in RESOURCE_FILES:
        if not os.path.exists(file_name):
            print("Couldn't find file {}.".format(file_name))
            continue
        with open(file_name, 'r') as f:
            all_resources.extend(json.load(f))
    resource_embeds = [i.get('embed', None) for i in all_resources]
    if not all(resource_embeds):
        print("Some empty embeds exist")
    search_index = AnnoyIndex(len(resource_embeds[0]), 'angular')
    # Add embeds
    for i, embed in enumerate(resource_embeds):
        search_index.add_item(i, embed)
    search_index.build(10)  # 10 trees
    search_index.save(ANNOY_NN_FILE)
    # Save a clean copy of the resources for later
    for i in range(len(all_resources)):
        del all_resources[i]['embed']
    with open(ANNOY_NN_RESOURCES, 'w') as f:
        json.dump(all_resources, f)
elif sys.argv[1] == '-query':
    if not os.path.exists(ANNOY_NN_RESOURCES):
        print("Couldn't find the resource file {}", ANNOY_NN_RESOURCES)
        exit()
    elif not os.path.exists(ANNOY_NN_FILE):
        print("Couldn't find the annoy tree {}", ANNOY_NN_FILE)
        exit()
        
    with open(ANNOY_NN_RESOURCES, 'r') as f:
        resources = json.load(f)
    search_index = AnnoyIndex(4096, 'angular')
    search_index.load(ANNOY_NN_FILE)
    
    question = 'Who can I talk to about depression?' if len(sys.argv) == 2 else sys.argv[2]
    question_embed = cohere_util.embed(question)
    sim_id, distance = search_index.get_nns_by_vector(question_embed, 3,
                                                    include_distances=True)
    for i in range(3):
        print("Distance {} - Desc: {}".format(distance[i], resources[sim_id[i]]))
    