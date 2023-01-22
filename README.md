# MentalBase
## Functionality
MentalBase is a platform that interfaces through a chatbot that provides relevant mental health resources for university students by using Artificial Intelligence to best match student needs.
MentalBase allows the student to:
- Anonymously talk to an Artificial Intelligence bot and in return, provide a list of mental health resouces relevant to the search query
- Speak to an agent anonymously, who will not know who you are unless you choose to disclose that information

## How We Built It
The major component to getting information about existing mental health resources was to scrape websites the provided such information. We used Python to construct an algorithm to scrape data from websites and store it in our database. The data is fed into our NLP (Natural Language Processing) algorithm to train the chatbot AI to generate responses to specific queries. The AI involves sophisticated NLP techniques to parse through an user input query and take note of keywords for semantic similarity analysis. After training and empirically tuning the AI, we linked the frontend (our website) to the backend (Python scripts) using a server hosted on Flask.
