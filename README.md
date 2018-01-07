# CP317 MLS Project
Web application to extend a [Brightspace learning enviroment](https://www.d2l.com/products/learning-environment/) using the [Brightspace API](http://docs.valence.desire2learn.com/reference.html) to bulk upload student grades and feedback. A writeup with more background can be found [here](https://cocalc.com/share/0f65cb8b-6f11-42b9-87d4-2e2ec6e0bf63/final_report/CP317_Final_Report.pdf?viewer=share)

## Getting Started
### Prerequisites
#### Python
##### Development
- [PIP](https://pypi.python.org/pypi/pip)
- [Python 3.x](https://www.python.org/download/releases/3.0/)
##### Deployment
- [Apache](https://www.apache.org/)
- [Docker](https://www.docker.com/)
#### PHP
- to be filled in

### Installing
### Python
1. Install PIP and Python3.x if not already installed
2. Clone the repository to your computer 
```git clone https://github.com/Sjohnston3700/CP317_MLS_Project.git ezmarker```
3. Install virtualenv if not already installed
```pip install virtualenv```
4. Inside git_project_folder checkout the Python branch
~~~~
git fetch origin
git checkout -b python origin/python
~~~~
5. Create a copy of 'template_conf_basic.py' named conf_basic.py
7. Update the values for API key/ID trusted_url and lms host in conf_basic.py
7. Create a new python3 virtual environment (anywhere is fine)
```virtualenv -p python3 name-of-your-env-here```
8. Activate your virtual enviroment (need to do this anytime you want to run code)
~~~
source name-of-your-env-here/bin/activate (Linux/MAC)
virtualenv_name\Scripts\activate (Windows)
~~~
9. Install necessary libraries (only need to do once)
```pip install -r requirements.txt```
10. Inside git_project_folder run ```python ezmarker.py```
11. In any browser goto ```localhost:8080``` and you should see the home page for web app

### PHP
- To be filled in

## Running the tests
There are no tests

## Deployment
### Python
1. Clone repository to server you want to run it on.
```git clone https://github.com/Sjohnston3700/CP317_MLS_Project.git ezmarker```
2. Checkout Python branch
~~~~
git fetch origin
git checkout -b python origin/python
~~~~
3. Update API KEY/ID, trusted url, and LMS values in the deploy_python file. 
4. Run deploy_python
5. If you later want to run the latest version of the code just run deploy_python again.

### PHP
1. Clone repository to server you want to run it on.
```git clone https://github.com/Sjohnston3700/CP317_MLS_Project.git ezmarker```
2. Checkout PHP branch
~~~~
git fetch origin
git checkout -b php origin/php
~~~~
3. Update API KEY/ID, trusted url, and LMS values in the deploy_php file. 
4. Run deploy_php
5. If you later want to run the latest version of the code just run deploy_php again.

## Built With
### Python
- [Python3.x](https://www.python.org/download/releases/3.0/)
- [Flask](http://flask.pocoo.org/)
- [Brightspace API](http://docs.valence.desire2learn.com/reference.html)
- [Docker](https://www.docker.com/)

### PHP
- [PHP]

## Contributing
If you are interested in contributing to this project please send us an email.

## Versioning
The code as is should be considered v1.0.0 It is functional, feature complete, and safe to use. 

## Authors
* **Harold Hodgins** - *Initial work* - [CP493 - Winter 2017](https://cocalc.com/share/9501f241-b52e-43f8-9034-7292e8ee54ce/final_report/MLS_API_Report.pdf?viewer=share) See also the list of [contributors](https://github.com/Sjohnston3700/CP317_MLS_Project/contributors) who participated in this project.
## License
This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
## Acknowledgments
* This Readme is based on the [Purple Booth ReadMe template](https://gist.github.com/PurpleBooth/109311bb0361f32d87a2)
* A big thank you to everyone who contributed to this project
