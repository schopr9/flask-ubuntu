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
    groups : [1,3,5]
}