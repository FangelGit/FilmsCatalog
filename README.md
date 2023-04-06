# Films catalog
A small project representing REST API using DRF
# Models
## User
    django.contrib.auth.models.AbstractUser subclass with 'user_type' field, 
    which can take one of ('user', 'superuser', 'owner') value
## Director
    django.db.models.Model subclass with 'first_name', 'second_name', 'birth_date' fields
## Country
    django.db.models.Model subclass with unique 'name' field.
## Film
    django.db.models.Model subclass with 'title', 'description', 'director' (Many to One relation with Director),
    'country' (Many to Many relation with Country) fields
# Public endpoints
## "/login/" 
    Returns account type for authorized user
## "/api/film/"
    Returns films list with nested data
    Everyone can GET
    Superuser and Owner can POST, PUT, DELETE
# Private endpoints
## "/api/country/" 
    Returns countries list
    Only Superuser and Owner can GET, POST, PUT, DELETE
## "/api/director/"
    Returns derictors list
    Only Superuser and Owner can GET, POST, PUT, DELETE
## "/api/user/"
    Returns users list
    Only Superuser can GET, POST, PUT, DELETE

