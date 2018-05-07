# RESTful-API-Flask-application
Small-scale application using Flask framework and Python.
## The application has three main goals:
### Sign Up
- [x] The user can create a new account with a given email address and password
  - All the data is stored into an external file
  - Its email address in the database is unique
- [x] The user receives an confirmation email
- [x] In order to activate the account, the user has to click an activation link provided in the email 
### Log In - (Authentication)
- [x] The user can log in to the system with the chosen email address and password
### Authorization
- [x] Users can access a protected resource only if they have been previously authenticated
- [x] Anonymous access to these resources is not possible

##### I was unable to split the main script ('api.py') to more pieces, in order to follow best practices. The problem is that some common variables are needed throughout the scripts, which leads to the creation of loops between scripts. I did not had the necessary time to find a solution as to how the loop could be broken.
##### This might be a future work, together with a front-end extension.
