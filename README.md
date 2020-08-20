# cars_api

## About
Project was created as a recruitment task and follows requirements given. 

## Technologies used
Project was built using Django & Django Rest Framework. 

## Docker
Application is contenerized using Docker together with PostgreSQL database.
To run applicaiton run following commands:
    * `docker-compose run web python manage.py migrate` to run migraitons for db
    *  `docker-compose up` or `docker-compose up -d`

To stop application use:
    * `ctr + c` or `docker-compose down`

## Testing
Unittests are prepared and can be started with
    `docker-compose run web python manage.py test`

## App description
Following app is a simple simple REST API; a basic cars makes and models database interacting with external API.
We have following endpoints:

POST /cars
* Request body should contain car make and model name
* Based on this data, its existence is checked here https://vpic.nhtsa.dot.gov/api/
* If the car doesn't exist - returns an error
* If the car exists - it is saved in the database

POST /rate
* Add a rate for a car from 1 to 5

GET /cars
* Fetch list of all cars already present in application database with their current average rate

GET /popular
* Return top cars already present in the database ranking based on number of rates

## Live view
App is deployed on heroku: `https://netguru-cars-api.herokuapp.com/cars/`
