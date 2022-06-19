**STAR NAVI API**
***Quick Start***

 - Copy this git repository.
 - Install required packages:
 - `pip install -r requirements.txt`
 - Write down following commands:
 - `flask db init`
 - `flask db migrate`
 - `flask db upgrade`
 - Run `inserts.py` to create some test records in database
 - Now you can start Flask application (`app.py`)
 
 ***URLs***
 - `/` - GET. Smoke request. Just returns message "OK" to check that API is started
 - `/swagger`- Opens Swagger interface for testing API.
 - `/signup`- POST. Creates user. Request Body:
`
    {
      "username": "string",
      "email": "mail@example.com",
      "password": "string"
    }`

 - `/login` - GET. Log In User if not logged in. Returns JWT token. Authorization goes through header (Basic Auth)
 - `/logout` - GET. Log Out User.
 - `/user-activity` - GET. JWT required. Returns timestamp on user last login and last request
 - `/posts` - GET. JWT required. Returns list of all posts created.
 POST. JWT required. Creates post. Request body: 
 ``
 {
 "title" : "string",
 "text": "string"
 }``
 - `/posts/<uuid>` - GET.  JWT required. Returns post (selection by passing post UUID in URL)
 - `/posts/<uuid>/like` - POST. JWT required. Creates Like connected to selected post and user, who provided JWT.
 DELETE. JWT required. Post unlike (deletes like).
 - `/analytics` - GET. JWT required. Returns amount of likes made aggregated by date.

 **JWT AUTH**
 
To authenticate via JWT you should add 'x-api-key' header to your request with passing you token as value.