# Meeting website

This project is a dating site with the following functionality:
 - search for people by your search parameter or city;
 - private chats;
 - set/delete like;
 - add or remove a user from favorites;
 - with mutual likes, both of you receive a notification about this
 - sending notifications when mutual likes or adding you to favorites;
 - user authorization/registration;
 - registration via google;
 - confirmation of registration by mail;
 - etc.

### Launch of the project

#### 1) Clone the repository
```
https://github.com/Lanterman/meeting_website.git
```
#### 2) Create and run docker-compose
```
docker-compose up --build
```
#### 3) Follow the link in the browser
```
http://127.0.0.1:8000/
```
or
```
http://0.0.0.0:8000/
```

### Running tests

#### 1) Set the TESTING variable to True
```
config.db.TESTING = True
```
#### 2) Run tests
```
python -m pytest test
```
