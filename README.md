## Android server side services

* Backend python scripts automated on Linux server with cron jobs supplying observable endpoints to [MCC Android App](https://github.com/phillipsk/MissionChurch) 

* Scrapy crawls & OAuth key rotation to centralize Church's social network content and pipe to Android ViewModels
* Extensive API debugging
    * Postman collections 
    * Facebook GraphQL
    * REST APIs with Constant Contact, retrieving email campaign data
    * Youtube Data API, Video to audio conversion with _ffmpeg_ library 
* Current infrastructure relies on self managed Linux server with cron jobs and minimal security
* Refactoring to GCP service accounts, AWS lambda
