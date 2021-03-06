# django-twitter-spark
Thesis project: topic categorization and sentiment analysis on twitter

Summary
---------------
The presently work was (in a previously version) an academic thesis presented at the Central University of Venezuela (2018), about how to make topic categorization and sentiment analysis of tweets in Spanish with Python, using Text Mining and Natural Language Processing (NLP) with Apache Spark. Adittionally a web application in Django was developed to display various graphics indicators such as: a wordcloud and other interesting graphics.

Improvements and Current Status:
---------------
I've oriented all the project to API REST with Django Rest Framework (DRF) and added several improvements:

- Applying DRF Serializers
- Applying Swagger Doc
- Applying Django Classes Based Views 
- Complementing custom Sentiment Analysis by user with a Voting Classifier, based on different Machine Learning classifiers algoritms from Sklearn
- Using Zookeeper High Availability for the master node
- Differents improvements in logic, order, installation steps with makefile, environment variables to allow more scalability, and more things.

Original Idea:
---------------
- [Manuel Araujo](https://github.com/manuelaraujo1511)

- [Manuel Carrero](https://github.com/LegolasVzla)

## Technologies
- [Django](https://www.djangoproject.com/) the web framework for perfectionists with deadlines.

- [Django REST framework](https://www.django-rest-framework.org/) is a powerful and flexible toolkit for building Web APIs.

- [React](https://es.reactjs.org/) a JavaScript library for building user interfaces

- [PostgreSQL](https://www.postgresql.org/) is the World's Most Advanced Open Source Relational Database.

- [Tweepy](https://www.tweepy.org/) is an easy-to-use Python library for accessing the Twitter API.

- [Apache Spark](https://spark.apache.org/) is a unified analytics engine for large-scale data processing.

- [Apache ZooKeeper](https://zookeeper.apache.org/) is an effort to develop and maintain an open-source server which enables highly reliable distributed coordination.

- [NLTK (Natural Language Toolkit)](https://www.nltk.org/) is a leading platform for building Python programs to work with human language data.

- [Scikit-Learn](https://scikit-learn.org/stable/) is a Python module for machine learning.

What would happen if we integrate these technologies?...Let's check it!

## Requirements
- Ubuntu 16 or higher

## Installation

Clone this project:

	git clone https://github.com/LegolasVzla/django-twitter-spark

```Makefile``` will help you with all the installation. First of all, in ```django-twitter-spark/backend/``` path, execute:

	make setup

This will install PostgreSQL and pip on your system. After that, you need to create and fill up **settings.ini** file, with the structure as below:

	[postgresdbConf]
	DB_ENGINE=django.db.backends.postgresql
	DB_NAME=dbname
	DB_USER=user
	DB_PASS=password
	DB_HOST=host
	DB_PORT=port

	[tweepyConf]
	CONSUMER_KEY = <consumer_key>
	CONSUMER_SECRET = <consumer_secret>
	ACCESS_TOKEN = <access_token>
	ACCESS_TOKEN_SECRET = <access_token_secret>

	[sparkConf]
	SPARK_WORKERS = <host:port,...>
	SPARK_EXECUTOR_MEMORY = <spark_executor_memory (suggested value greater or equal than 2)>
	SPARK_EXECUTOR_CORES = <spark_executor_cores (suggested value greater or equal than 2)>
	SPARK_CORE_MAX = <spark_core_max (suggested value greater or equal than 2)>
	SPARK_DRIVER_MEMORY = <spark_driver_memory (suggested value greater or equal than 2)>
	SPARK_UDF_FILE = /udf.zip

	[tassConf]
	TASS_FILES_LIST=['file1.xml','file2.xml',...]

	[frontendClient]
	REACT_DOMAIN=<host>
	REACT_PORT=<port>

- postgresdbConf section: fill in with your own PostgreSQL credentials. By default, DB_HOST and DB_PORT in PostgreSQL are localhost/5432.

- tweepyConf section: register a [Tweepy account](https://developer.twitter.com/en/apply-for-access) and fill in with your own credentials.

- sparkConf section: list of master workers to start spark and path where are defined pyspark udf (udf/pyspark_udf.py for this project)  

- tassConf section: refers to the TASS datasets (XML files list from 2019 edition)

- frontendClient section: refers to React's domain and port (3000 by default)

Then, activate your virtualenv already installed (by default, is called ```env``` in the ```Makefile```):

	source env/bin/activate

And execute:

	make install

This will generate the database with default data and also it will install python requirements and nltk resources. Default credentials for admin superuser are: admin@admin.com / admin. 

Run django server (by default, host and port are set as 127.0.0.1 and 8000 respectively in the ```Makefile```):

	make execute

You could see the home page in:

	http://127.0.0.1:8000/socialanalyzer/

Then, in another terminal start master worker of Apache Spark:

	make start-spark

It will display a message similar as below:

	20/01/28 22:27:33 INFO Master: I have been elected leader! New state: ALIVE

By default port for master worker service to listen is 7077 (i.e: spark://192.xxx.xx.xxx:7077). You could open Apache Spark web UI in **http://localhost:8080/** or in the host displayed in the terminal:

	20/01/28 22:27:33 INFO Utils: Successfully started service 'MasterUI' on port 8080.
	20/01/28 22:27:33 INFO MasterWebUI: Bound MasterWebUI to 0.0.0.0, and started at http://192.xxx.xxx.xxx:8080

Finally, start an Apache Spark slave:

	make start-slave

## Running Apache Spark for high availability with ZooKeeper

ZooKeeper can provide [high availability](http://spark.apache.org/docs/latest/spark-standalone.html#high-availability) dealing with the single point of failure of Apache Spark. ZooKeeper is installed with ```make setup``` command of the ```Makefile``` (```/usr/share/zookeeper/bin``` path in Ubuntu). **highavailability.conf** file specified in ```make start-spark-ha``` command of ```Makefile``` file, needs a configuration with the below structure:

	spark.deploy.recoveryMode=ZOOKEEPER
	spark.deploy.zookeeper.url=localhost:2181
	spark.deploy.zookeeper.dir=<path_of_your_virtualenv>/lib/python3.<your_python_version>/site-packages/pyspark

By default, port for ZooKeeper service to listen is 2181. Create that file and save it in ```pyspark``` folder, installed inside of your virtualenv. If you didn't install spark with pip, save the file in ```spark/conf``` path or edit default properties in ```conf/spark-defaults.conf```. 

Run ZooKeeper:

	make start-zookeeper

This will start a ZooKeeper master. Also you can manage it with:

	service zookeeper # {start|stop|status|restart|force-reload}

Or just as below:

	cd /usr/share/zookeeper/bin/
	./zkServer.sh start
	./zkServer.sh status

Displaying the following information:

	ZooKeeper JMX enabled by default
	Using config: /etc/zookeeper/conf/zoo.cfg
	Mode: standalone

You can check the master ZooKeeper running in zooinspector:

	cd /usr/bin
	./zooinspector

Finally, you can run Spark with ZooKeeper as below (instead of using ```make start-spark```):

	make WEBUIPORT=<webui_spark_worker_PORT_> start-spark-ha

Where ```WEBUIPORT``` is an optional parameter (8080 by default) to see the Spark Web UI of that worker.

It will display a message similar as below:

	20/01/28 22:25:54 INFO ZooKeeperLeaderElectionAgent: We have gained leadership
	20/01/28 22:25:54 INFO Master: I have been elected leader! New state: ALIVE

## Launch multiple Masters in your cluster connected to the same ZooKeeper instance

In a terminal (or a node), run:

	make start-spark-ha

In your browser, open [http://localhost:8080/](http://localhost:8080/) and the status of that worker shoul be:

	Status: ALIVE

In another terminal (or a node), run:

	make WEBUIPORT=8081 start-spark-ha

In your browser, open [http://localhost:8081/](http://localhost:8081/) and the status of that worker shoul be:

	Status: STANDBY

In your python code, you can start a slave worker as below:

	from pyspark import SparkContext
	from pyspark import SparkConf
	conf = SparkConf()
	conf.setAppName('task1')
	conf.setMaster('spark://192.xxx.xxx.xxx:7077,192.xxx.xxx.xxx:7078')
	sc = SparkContext.getOrCreate(conf)

Now in the first master worker terminal, you should see:

	20/01/30 23:14:15 INFO Master: Registering app task1
	20/01/30 23:14:15 INFO Master: Registered app task1 with ID app-20200130231415-0000

You could see your slave worker running in the web UI in **Running Applications**. Now, kill your first master worker terminal. In the second terminal, now you should see:

	20/01/30 23:18:40 INFO ZooKeeperLeaderElectionAgent: We have gained leadership
	20/01/30 23:18:40 INFO Master: I have been elected leader! New state: RECOVERING
	20/01/30 23:18:40 INFO Master: Trying to recover app: app-20200130231415-0000
	20/01/30 23:18:40 INFO TransportClientFactory: Successfully created connection to /192.xxx.xxx.xxx:39917 after 18 ms (0 ms spent in bootstraps)
	20/01/30 23:18:40 INFO Master: Application has been re-registered: app-20200130231415-0000
	20/01/30 23:18:40 INFO Master: Recovery complete - resuming operations!

In second master worker web UI, the status should be changged:

	Status: ALIVE

Finally, stop existing context:

	sc.stop()

In the second master worker web UI your slave worker should be in **Completed Applications**

See full documentation of this flow [here](https://spark.apache.org/docs/latest/spark-standalone.html#standby-masters-with-zookeeper)

## Models

* Topic: is about people are talking in a specific moment in a social network.
* Word root: is a word or word part that can form the basis of new words through the addition of prefixes and suffixes.
* Dictionary: is a set of word that contains positive and negative words.
* CustomDictionary: is a customizable set of words per user, with positive and negative words
* Search: is a tracking table where you could find you recently search.
* SocialNetworkAccounts: is a set of social networks accounts used to sentiment analysis.

## About Spanish Sentiment Analysis Solutions

Nowadays exists many solutions of sentiment Analysis in English but is not the same history that in Spanish, since closer solutions provide a translate that allows you to receive Spanish content and translate to English to do the process. Sentiment Analysis is in fact a complex task in NLP, because there are great challenges, like context, irony, jokes or mostly sarcasm, that aren't aspects that even for humans results easy to detect, so currently exists differents studies (in some cases related with neuronal networks), that try to solve this problem from differents points of views, based on the person who wrote the content, the reputation or the kind of previously content published by that person (account), etc, also if the analysis detect if exists sarcasm in the content, the polarity is changed to the opossited.

In this project, on one hand, we bring another possible way of how to handle with this problem (of course including the possibility of to do this analysis oriented to Big Data with Spark) that is by creating a custom dictionary by user of positive and negative words, that the user can define to contribute to the resulting analysis according of the polarity assigned to custom words, i.e:

	"Hoy es un maravilloso e impresionante día de mierda"

This is a typically ironic tweet but the model based on the dictionary used on this project, will categorize it  as "Positive" by majority of positive words. However, some words that aren't in ```positive_dictionary.json``` or ```negative_dictionary.json``` files could be added by the user and selected as "Positive" or "Negative", so in consequence, a sarcasm tweet could be categorized correctly, but only by mayority of positive and negative words, so it's important to emphasize that this isn't an advance solution (also it express another problem, how to build a Spanish Lexicon?), but it's an idea of how this problem could be attacked. In the other hand, we also offer the possibility of doing sentiment analysis by training a Voting Classifier system, consisting on Naives Bayes provided by NLTK and other machine learning models from Scikit Learn. So when the user is authenticated, the system will use the custom user dictionary model (**Rule-based Approach**, system naive since it don't take into account how words are combined in a sequence, i.e the context) and if the user isn't authenticated, the system will use Voting Classifier (**Automatic Approach**).

## About TASS dataset

The [Spain Society of Natural Language Proccessing (SEPLN)](http://www.sepln.org/), offers the [TASS Dataset](http://tass.sepln.org/) that "is a corpus of texts (mainly tweets) in Spanish tagged for Sentiment Analysis related tasks. It is divided into several subsets created for the various tasks proposed in the different editions through the years." **You need to sign the License Agreement to download the dataset** in the following [link](http://www.sepln.org/workshops/tass/tass_data/download.php).

This project specify a ```tassConf``` section in the ```settings.ini``` file, to provide a list of the TASS Dataset XML files (using the 2019 edition), to train the Naive Bayes model.  

## Swagger Documentation

[Swagger UI](https://swagger.io/tools/swagger-ui/) is a tool for API documentation. "Swagger UI allows anyone — be it your development team or your end consumers — to visualize and interact with the API’s resources without having any of the implementation logic in place. It’s automatically generated from your OpenAPI (formerly known as Swagger) Specification, with the visual documentation making it easy for back end implementation and client side consumption."

This project uses [drf-yasg - Yet another Swagger generator](https://github.com/axnsan12/drf-yasg)

## Endpoints Structure

In a RESTful API, endpoints (URLs) define the structure of the API and how end users access data from our application using the HTTP methods (GET, POST, PUT, DELETE), making all posssible CRUD (create, retrieve, update, delete) operations.

You can see the endpoints structure in the Swagger UI documentation:
	
	http://127.0.0.1:8000/swagger/

Basically the structure is as below for all the main instances (User, Dictionaries, Custom Dictionaries, Topics and Word roots)

Endpoint Path |HTTP Method | CRUD Method | Used for
-- | -- |-- |--
`api/<instance>` | GET | READ | Get all the <instance> records
`api/<instance>/id/` | GET | READ | Get a single <instance>
`api/<instance>`| POST | CREATE | Create a new <instance> record
`api/<instance>/id/` | PUT | UPDATE | Update a <instance> record
`api/<instance>/id/` | DELETE | DELETE | Delete a <instance> record

## Endpoints without Models

* Word_cloud: `api/word_cloud/`

Endpoint |HTTP Method | CRUD Method | Used for
-- | -- |-- |--
`create` | POST | CREATE | To generate Twitter word cloud images.

Endpoint Path:
	```api/word_cloud/comments/<string:comments>/user_id/<int:user_id>```

Parameters:
- Mandatory: comments
- Optionals: user

If user is given (authenticated=True), it will generate a random word cloud with one of the mask located in:

	/static/images/word_cloud_masks

In other case, word cloud will be with square form. The image will be generated in the follow path:

	/static/images/word_clouds/<user>

Endpoint |HTTP Method | CRUD Method | Used for
-- | -- |-- |--
`list` | GET | READ | To list Twitter word cloud images by users.

Endpoint Path:
	```api/word_cloud/list```

* Twitter_analytics: `api/twitter_analytics/`

Endpoint |HTTP Method | CRUD Method | Used for
-- | -- |-- |--
`tweets_get` | POST | CREATE | To get a list with trending tweets

Endpoint Path:
	```api/twitter_analytics/tweets_get```

Parameters:
- Mandatory: social network account id (1 = twitter)

* Machine Learning Layer: `api/ml_layer/`

Endpoint |HTTP Method | CRUD Method | Used for
-- | -- |-- |--
`tweet_topic_classification` | POST | CREATE | To determine the topic of the tweet

Endpoint Path:
	```api/ml_layer/tweet_topic_classification```

Parameters:
- Mandatory: text (a tweet)

* Big Data Layer: `api/big_data_layer/`

Endpoint |HTTP Method | CRUD Method | Used for
-- | -- |-- |--
`process_tweets` | POST | CREATE | To get current tweets, to process them with different goals: to determine the topic and sentiment analysys of all the tweets and also, returns cleaned tweets that you can use to generate a word cloud, for example.

Endpoint Path:
	```api/big_data_layer/process_tweets/social_network/<int:social_network_id>```

Parameters:
- Mandatory: social network account id (1 = twitter)

Endpoint |HTTP Method | CRUD Method | Used for
-- | -- |-- |--
`twitter_search` | POST | CREATE | To apply sentiment analysis againts the text found in the Twitter search, also will show differents indicators related, so the user could know if people is talking positive or negative about the text searched.

Endpoint Path:
	```api/big_data_layer/twitter_search/text/<string:text>```

Parameters:
- Mandatory: text to search, language
- Optionals: user

## Updating System Dictionary
------------------------

If you want to add a new word in the system dictionary, you can use the following endpoint:

	http://127.0.0.1:8000/api/dictionary/

Then, in your terminal, run in the root of the project the below command to update the ```word_root``` field of the related new word and also update the fixtures:

	python manage.py update_dictionary_word_roots 1

Where "1" is Spanish language.

## Contributions
------------------------

All work to improve performance is good

Enjoy it!
