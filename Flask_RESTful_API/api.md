## This is the main script
### The script is organized in two groups:
#### 1. Initialization
#### 2. Resources:
- Signup (#1)
  1. Read email & password
  2. Add email and password to database file
  3. If email exists in database abort
  4. Create token (activation key)
  5. Send email with an URL for activation
- Activation (#2)
  1. Read token (activation key) from URL
  2. Decode token
  3. If it is wrong abort
  4. If the email does not exist in database abort
  5. Change user's status to active
- Login (#3)
  1. Read email & password
  2. If the email does not exist in database abort
  3. If the password is wrong abort
  4. If the user's status is not active abort
  5. Return a token with a variable "check=1"
- Main (#4)
  1. Re-route to function "login_required"
      1. Read header
      2. Decode token with the variable "check"
      3. If email does not exist in database abort
      4. If check=0 abort
  2. Print the hidden message
