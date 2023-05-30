# dvm2
# E-Commerce Web Application

> A basic online marketplace. 

> A web app on which vendors can register themselves and add items they want to sell.

> Users can add money  and order these items.


## Features

#### Basic Features:
- Registeration: Users need to register first. There are different registerations for vendors and customers.

![Screenshot (8)](https://github.com/raggg377/docker/assets/93575844/6700906d-07f2-4951-8bf6-8dd11bc091f0)

- Authentication: Vendors and customers need to re-login by verifying. This was done using Django's in-built authentication system.

![Screenshot (9)](https://github.com/raggg377/docker/assets/93575844/aa1ca685-d2c5-4e84-bbf4-f30e6cc46dd2)

#### Vendor-side Features:

The web-app has a page for each vendor where his items are listed, sort of like a 'vendor profile'.

![Screenshot (12)](https://github.com/raggg377/docker/assets/93575844/76590e7b-8511-4870-8a65-5a81a8e49096)


Vendors can:
- Add *multiple items* 
- Items can have *many units* (specified by the vendor)
- Each item can have a image, a title, a price and a description.
- Vendors can *add or delete items* to sell
- View all orders that were placed for items that they're selling 
- *get an email* whenever someone buys from him
- generate a CSV/Excel report of all his sales till now
- show discounts on items

#### Customer-side Features:

The web-app has a page for each customer where all the items are listed kinda like a 'home-page'

![Screenshot (15)](https://github.com/raggg377/docker/assets/93575844/2e5d37af-0871-4495-b294-7ffb8ebe9d2c)


Customers can:

- order from *multiple vendors* at a time 
- order *multiple items*
- order upto 10 units of the same item
- add money (virtual) to their account  
- View all *previous orders* 
- order only if he has sufficient funds for the items he's buying
- edit shipping address
- *add items to their wishlists*
- view all details of a previous order on clicking it in the previous orders section
- directly *move an item from the wishlist to the cart*

## Images of special features

1. Mail

![Screenshot (25)](https://github.com/raggg377/docker/assets/93575844/f0944aab-bb3f-443d-920e-bddb6de8c28f)


2. CSV Files

![Screenshot (23)](https://github.com/raggg377/docker/assets/93575844/85913467-12a6-4e43-b85d-377b04f7ed6b)


3. Database

![Screenshot (24)](https://github.com/raggg377/docker/assets/93575844/d0653248-6ce1-4da2-8082-3096e6dc0de5)


## Implementation Video

>These 2 videos show the implementation of all the features written above:

>https://drive.google.com/file/d/1rBffHnjcj8cOjaruZFVgyKWXLI6kDZ77/view?usp=sharing

>https://drive.google.com/file/d/1rA6YQnBbrIUFSd6MtYm1OSUqLe_iPf-R/view?usp=sharing
## Tech

I used a number of tech-stacks to make this project successful

- [Django](https://www.djangoproject.com/) - The framework used to create this project 
- [Django Allauth](https://www.section.io/engineering-education/django-google-oauth/) - for  authentication 
- [Mailjet](https://www.mailjet.com/) - to send mails to vendors
- [Postgresql](https://www.postgresql.org/) - to create a database for the web application


## Building and Docker
>Deployment of the project by creating the docker file, with entry point , env variable and ngnix config is done . 

>The server in production is successfully running on local server

>Credits: https://testdriven.io/blog/dockerizing-django-with-postgres-gunicorn-and-nginx/

## License

MIT
