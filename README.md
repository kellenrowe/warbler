Welcome to Warbler! A Twitter clone with a spin!

This was a 2-3 day exercise to extend a somewhat-functioning Twitter clone.

To view Warbler please complete the following steps:

    - download the code by using git clone
    - cd into the folder and type python3 -m venv venv
    - activate the venv with source venv/bin/activate
    - install all the necessary requirements with pip3 install -r requirements.txt
    - in your terminal type createdb warbler
    - then seed the db with data using python3 seed.py
    - LASTLY type flask run to start your local server on port 5000
    
visit localhost:5000/users to follow a few users and see their recent messages appear in your profile.