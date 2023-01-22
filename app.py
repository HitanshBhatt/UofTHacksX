from flask import Flask, render_template, request, jsonify, make_response
import nlp
import json
import cohere_util


app = Flask(__name__)

RESOURCE_COOKIE = 'rss_only'


@app.get("/")
def index_get():
    response = make_response(render_template("base.html"))
    response.set_cookie(RESOURCE_COOKIE, "true")
    return response


@app.post("/predict")
def predict():
    text = request.get_json().get("message")
    req_type = None
    if request.cookies.get(RESOURCE_COOKIE, "true") == "true":
        req_type = cohere_util.classify(
            text, preset='req-classification-ta6hjk').prediction
    text_embed = cohere_util.embed(text)
    response, distance = nlp.query_knn('site', 'resource', text_embed)
    if req_type and req_type == 'person':
        response_phone, phone_distance = nlp.query_knn(
            'site', 'phone', text_embed)
        response += response_phone
        distance += phone_distance
    else:
        response_video, video_distance = nlp.query_knn(
            'media', None, text_embed)
        response += response_video
        distance += video_distance
    # Filter the responses based on the distance
    close_response = []
    close_distance = []
    for i in range(len(response)):
        if distance[i] < 1.5:
            close_response.append(response[i])
            close_distance.append(distance[i])
    decorated = [(close_distance[i], i, res)
                 for i, res in enumerate(close_response)]
    decorated.sort()
    answers = [res for _, _, res in decorated[:5]]
    # Generate summary for the top
    text = 'Prompt: {}\nResources:\n'.format(text)
    for answer in answers:
        text += '{}: {}\n{}\n'.format(answer['url-type'],
                                      answer['name'], answer['description'])
    text += 'Summary:'
    print(text)
    summary = {'url-type': 'plain',
               'text': cohere_util.generate(text, preset='generate-response-tx788r')}
    message = {"answer": [summary]+answers}
    response = make_response(jsonify(message))
    response.set_cookie(RESOURCE_COOKIE, "true" if req_type ==
                        "resource" else "false")
    return response


@app.route("/cookies")
def cookies():
    res = make_response("Cookies", 200)
    res.set_cookie("rss_only", "True")
    res.set_cookie("address", "")

    return res


if __name__ == "__main__":
    app.run(debug=True)
