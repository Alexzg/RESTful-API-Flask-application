# RESTful-API-Flask-application
Small-scale application using Flask framework and Python.
## Testing Scenarios
For the evaluation of the application, a number of scenarios have been manually tested using "Postman" app.
### Sign up
- [x] The user is trying to submit an email address that already exists in the database
  - In this case, a message is displayed for the user to import a new email address
### Activation (of the account)
- [x] The user is trying to manually send a wrong activation key
  - In this case, a message is displayed that the key is not correct
- [x] The user is trying to manually send a correct key, but the the key does not contain details of an existed user
  - In this case, messages are displayed accordingly that the email or the password is not correct
### Log in
- [x] The user attempts to log in, without prior completion of the activation procedure 
  - In this case, a message is displayed for the user to activate the account
- [x] The user attempts to log in using wrong email or password
  - In its case, a message is displayed informing the user of what is wrong
### Authorization (resource only for members)
- [x] The user attempts to see the hidden resource, without previously log in or sign up
  - In this case, a message is displayed for the user to log in or sign up
### Correct procedure
- [x] The user successfully executes sign up, activation, log in
  - In this case, a secret message is displayed
