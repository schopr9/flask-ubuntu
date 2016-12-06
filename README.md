# flask-api
rest api using sqlalchemy

### Steps to Install

     git clone 
     cd venv/scripts
     activate
     #workspace venv    
     pip install -r requirements.txt

     python migrate.py db init
     python migrate.py db migrate
     python migrate.py db upgrade
     python run.py
     
     https://www.getpostman.com/collections/0392d95a122034ad2ba2
     
         GET /users
    GET /user/:id
    GET /user/:id/groups
    PATCH /user/:id  {}
    DELETE /user/:id 
    POST /user/new {}
    DELETE /user/:id/groups {}


    GET /groups
    GET /group/:id
    GET /group/:id/users
    PATCH /group/:id {}
    POST /group/new  {}




POST /group/new

      {
      "data": 
        {
          "attributes": {
           "name": "postbeyond1"
        },
           "type": "groups"
       }
      
    }

POST /user/new
    
    {
      "data": 
        {
          "attributes": {
            "email": "mohit.chopra@gmail.com", 
            "username": "mohit007"
         },
        "type": "users"
      }
    }

POST /user/:id/groups

    {

    "groups" : [1,3,5]
    }

DELETE /user/:id/groups

    {

    "groups" : [1,3,5]
    }


