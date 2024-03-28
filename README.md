# Web Scraping and Data Analysis with Selenium and MySQL

## Introduction
This Python script demonstrates web scraping with Selenium from the Dealabs website. It extracts offer information, such as title, price, and company name, and stores it in a MySQL database. Additionally, it performs basic data analysis on offer prices.

## Requirements
- Python
- Selenium
- Docker
- Docker Compose
# How To run
- Run `docker-compose -up`
- Check `localhost:8081` to enter into the phpMyAdmin interface
- log in with the username 'root', without password
- Check if there is a database called 'dealabs'
- If it is not there, run this: `docker exec -it container_name bash`
- While you are inside the container run `mysql -u root -p < /docker-entrypoint-initdb.d/init.sql`
- Finally run the python script
