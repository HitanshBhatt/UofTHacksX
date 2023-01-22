import os
import sys
import json
import cohere_util
from annoy import AnnoyIndex

RESOURCE_FILES = ['./data/{}'.format(i) for i in os.listdir('./data')]
BATCH_SIZE = 20
KNN_TYPES = ['site', 'media', 'app']
KNN_DESC = ['resource', 'phone', 'physical']

all_resources = []
for file_name in RESOURCE_FILES:
    if not os.path.exists(file_name):
        print("Couldn't find file {}.".format(file_name))
        continue
    with open(file_name, 'r') as f:
        all_resources.extend(json.load(f))


def get_annoy_file(url_type, desc_type):
    return 'knn/{}-{}-search.ann'.format(url_type if url_type else 'none', desc_type if desc_type else 'none')


def get_annoy_resource(url_type, desc_type):
    return 'knn/{}-{}-serach.json'.format(url_type if url_type else 'none', desc_type if desc_type else 'none')


def classifyUrl(url):
    if 'youtube' in url or 'itunes' in url:
        return 'media'
    elif 'play.google' in url:
        return 'app'
    else:
        return 'site'


def build_knn(url_type, desc_type):
    filtered_resources = list(filter(lambda x: (not url_type or x['url-type'] == url_type) and (
        not desc_type or x['desc-type'] == desc_type), all_resources))
    filtered_embeds = []
    clean_resources = []
    for i in filtered_resources:
        filtered_embeds.append(i['embed'])
        del i['embed']
        clean_resources.append(i)
    if len(filtered_embeds) == 0:
        print("No embeds found for {} {}".format(url_type, desc_type))
        return
    elif not all(filtered_embeds):
        print("Some empty embeds for {} {}".format(url_type, desc_type))
        return
    knn = AnnoyIndex(len(filtered_embeds[0]), 'angular')
    for i, embed in enumerate(filtered_embeds):
        knn.add_item(i, embed)
    knn.build(10)  # 10 trees
    knn.save(get_annoy_file(url_type, desc_type))
    with open(get_annoy_resource(url_type, desc_type), 'w') as f:
        json.dump(clean_resources, f)


def query_knn(url_type, desc_type, embed):
    if not url_type:
        res = []
        distance = []
        for type in KNN_TYPES:
            cur_res, cur_dis = query_knn(type, desc_type, embed)
            res += cur_res
            distance += cur_dis
        return res, distance
    elif not desc_type:
        res = []
        distance = []
        for type in KNN_DESC:
            cur_res, cur_dis = query_knn(url_type, type, embed)
            res += cur_res
            distance += cur_dis
        return res, distance
    if not os.path.exists(get_annoy_resource(url_type, desc_type)):
        print("Couldn't find the resource file {}".format(
            get_annoy_resource(url_type, desc_type)))
        return [], []
    elif not os.path.exists(get_annoy_file(url_type, desc_type)):
        print("Couldn't find the annoy tree {}".format(get_annoy_file(url_type, desc_type)))
        return [], []
    search_index = AnnoyIndex(4096, 'angular')
    search_index.load(get_annoy_file(url_type, desc_type))
    ids, distance = search_index.get_nns_by_vector(
        embed, 3, include_distances=True)
    with open(get_annoy_resource(url_type, desc_type), 'r') as f:
        resources = json.load(f)
    res = [resources[i] for i in ids]
    return res, distance


if __name__ == '__main__':
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
                if 'desc-type' not in resource or not resource['desc-type']:
                    resources[i]['desc-type'] = cohere_util.classify(
                        resource['description'], preset='desc-classification-mavvyx').prediction
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
        for type in KNN_TYPES:
            for desc in KNN_DESC:
                build_knn(type, desc)
    elif sys.argv[1] == '-query':
        question = 'Who can I talk to about depression?' if len(
            sys.argv) == 2 else sys.argv[2]
        question_embed = cohere_util.embed(question)
        for type in KNN_TYPES:
            res, distance = query_knn(type, question_embed)
            if res:
                print("Type:", type)
                for i in range(len(res)):
                    print(
                        "Distance {} - Desc: {}".format(distance[i], res[i]))
