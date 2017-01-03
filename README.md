#Title: Yelp-App-NLP Summarizer and Recommender

##Project Summary

Going through a Yelp site for a particular restaurant or store can be exhausting. There may be hundereds or even thousands of reviews to parse through, as well as suggestions for the best dish or item at that location. Especially when hungry, this can make deciding on a restaurant very difficult and time consuming. In this project, I used NLP techniques such as LDA, Word2Vec, and TFIDF to summarize these reviews into a few words that identify the most important pieces of information. In addition, based of the reviews, similar restaurants were recommended. A Flask app was built to make this user-friendly.

##Data Sources 
Yelp Dataset Challenge - 2.7M reviews from major cities across the world.

##iPython Notebooks:
Creating Businesses Dataframe.ipynb - creates the businesses dataframe from MongoDB
GoogleWord2Vec.ipynb - Converting the Stanford and Google pretrained vector set into a format readable by Gensim package
YelpData.ipynb - grabbing data from MongoDB, Preprocessing with CountVectorizer, LDA, and Word2Vec using both Google and Stanford pretrained vector set and Nearest Neighbor approach, TFIDF
Similarities.ipynb - takes reviews and finds the closest matching restaurants (recommender)
yelp_app/app - Flask app

##Final Presentation
Yelp Reviews.pdf - Powerpoint Presentation