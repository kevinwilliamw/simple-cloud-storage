# Simple Cloud Storage
A simple cloud file storage service that contains :

### User Access Service
  1. Register API
     - `127.0.0.1;8000/register`
     - Parameters : *(username, password)*
  2. Log In API
     - `127.0.0.1;8000/login`
     - Parameters : *(username, password)*
  3. Log Out API
     - `127.0.0.1;8000/logout` 
     - Parameters : *none*
      
### File Access Service [Log In Required]
  1. Upload File 
     - `127.0.0.1:8000/upload` 
     - Parameters : *(content)*
  2. Get All File 
     - `127.0.0.1/getall`
     - Parameters : *none*
  3. Download File by ID 
     - `127.0.0.1;8000/download`
     - Parameters : *(file-id)*

## Requirements for running the service
  This service uses *python*, *nameko*, *redis*, and *mySQL*.
  
## Steps
  1. Clone this repository
  2. Import the *.sql* inside `sql` folder into your local mySQL database.
  3. Open 2 CMDs
  4. On the first CMD, type `nameko run service` to run the gateway.
  5. On the second CMD, type `nameko run storage_service` to run the file service.
  6. To test the API using *Postman*, import the *.postman_collection* file inside `postman` folder into your *Postman*.
