import os
import sys
import json
import cohere_util
from annoy import AnnoyIndex

RESOURCE_FILES = ['./data/{}'.format(i) for i in os.listdir('./data')]
BATCH_SIZE = 20
KNN_TYPES = ['site', 'video', 'app']


def get_annoy_file(type):
    return 'knn/{}-search.ann'.format(type)


def get_annoy_resource(type):
    return 'knn/{}-serach.json'.format(type)


def classifyUrl(url):
    if 'youtube' in url:
        return 'video'
    elif 'play.google' in url:
        return 'app'
    else:
        return 'site'


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
        idxs = []
        desc = []
        change = False
        for i, resource in enumerate(resources):
            if 'url-type' not in resource or not resource['url-type']:
                resources[i]['url-type'] = classifyUrl(resource['link'])
                change = True
            if 'embed' not in resource or not resource['embed']:
                idxs.append(i)
                desc.append(resource['description'])
            if len(idxs) > BATCH_SIZE:
                vector = cohere_util.embed(desc)
                for i in range(len(idxs)):
                    resources[idxs[i]]['embed'] = vector[i]
                idxs = []
                desc = []
                with open(file_name, 'w') as f:
                    json.dump(resources, f)
        if len(idxs) > 0:
            vector = cohere_util.embed(desc)
            for i in range(len(idxs)):
                resources[idxs[i]]['embed'] = vector[i]
        if len(idxs) > 0 or change:
            with open(file_name, 'w') as f:
                json.dump(resources, f)
elif sys.argv[1] == '-knn':
    all_resources = []
    for file_name in RESOURCE_FILES:
        if not os.path.exists(file_name):
            print("Couldn't find file {}.".format(file_name))
            continue
        with open(file_name, 'r') as f:
            all_resources.extend(json.load(f))
    clean_resources = [i.copy() for i in all_resources]
    for i in range(len(clean_resources)):
        del clean_resources[i]['embed']
    for type in KNN_TYPES:
        resource_embeds = [i.get('embed', None) for i in list(
            filter(lambda x:x['url-type'] == type, all_resources))]
        if not resource_embeds:
            print("No embeds of type {} found".format(type))
            continue
        if not all(resource_embeds):
            print("Some empty embeds exist for type {}".format(type))
        search_index = AnnoyIndex(len(resource_embeds[0]), 'angular')
        # Add embeds
        for i, embed in enumerate(resource_embeds):
            search_index.add_item(i, embed)
        search_index.build(10)  # 10 trees
        search_index.save(get_annoy_file(type))
        with open(get_annoy_resource(type), 'w') as f:
            json.dump(list(
                filter(lambda x: x['url-type'] == type, clean_resources)), f)
elif sys.argv[1] == '-query':
    question = 'Who can I talk to about depression?' if len(
        sys.argv) == 2 else sys.argv[2]
    question_embed = cohere_util.embed(question)
    for type in KNN_TYPES:
        if not os.path.exists(get_annoy_resource(type)):
            print("Couldn't find the resource file {}", get_annoy_resource(type))
            continue
        elif not os.path.exists(get_annoy_file(type)):
            print("Couldn't find the annoy tree {}", get_annoy_file(type))
            continue

        with open(get_annoy_resource(type), 'r') as f:
            resources = json.load(f)
        search_index = AnnoyIndex(4096, 'angular')
        search_index.load(get_annoy_file(type))
        sim_id, distance = search_index.get_nns_by_vector(question_embed, 3,
                                                          include_distances=True)
        if sim_id:
            print("Type:", type)
            for i in range(len(sim_id)):
                print(
                    "Distance {} - Desc: {}".format(distance[i], resources[sim_id[i]]))
