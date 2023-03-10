# MentalBase
## Functionality
MentalBase is a platform that interfaces through a chatbot that provides relevant mental health resources for university students by using Artificial Intelligence to best match student needs.
MentalBase allows the student to:
- Anonymously talk to an Artificial Intelligence bot and in return, provide a list of mental health resources relevant to the search query
- Speak to an agent anonymously, who will not know who you are unless you choose to disclose that information

## How We Built It
The major component to getting information about existing mental health resources was to scrape websites (Beautiful Soup) that provided such information. We used Python to construct an algorithm to scrape data from websites and store it in our database. The data is fed into our NLP (Natural Language Processing) algorithm to train the chatbot AI to generate responses to specific queries. The AI involves sophisticated NLP techniques to parse through an user input query and take note of keywords for semantic similarity analysis. After training and empirically tuning the AI, we linked the frontend (our website) to the backend (Python scripts) using a server hosted on Flask.

## Running the Code

### Scraping the Resources
We currently only pull data from 3 university websites, UofT, Ontario Tech and McMaster. To scrape each site, run each of their respective scrapers under the `scraper` folder. They should then spit the contents of each site into a file under `data`.

### co:here API
Make sure there is a `.env` file present in the root directory with a valid `cohere-token` so the API calls will work.

### Converting the Text to Vectors
Under the root directory, run `python nlp.py -embed` to convert all the description into embedings. This will modify the files in the `data` folder.

### Creating the KNN trees
Run `python nlp.py -knn` to generate the `annoy` KNN trees to be queried later. These trees are saved in the `knn` folder.

### Testing Querying the KNN
To test the KNN, we can run `python nlp.py -query [text]` to try and see what the closes matches are in the KNN.

### Running the Flask Server
In the root directory, run `python -m flask run` to start the local web server. The chatbot is hosted on the root page of `localhost:5000/`
