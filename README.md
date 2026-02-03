# Authentication vs Authorization 🔐

Understanding the difference between authentication and authorization is fundamental to building secure applications. Although the terms are often used together, they solve two very different problems in security.

### AUTHENTICATION - Who are you?

Authentication is the process of verifying "Identity". Think of it like:
- Logging in with email and password
- Using face ID to unlock your phone
- Entering an OTP

In a typical application:

![Screenshot 2026-02-03 at 2 16 07 PM](https://github.com/user-attachments/assets/948c65d0-a897-4a98-94d9-e686887c0c43)


### AUTHORIZATION - What are you allowed to do?

Authorization happens after Authentication. It simply answers one question - **"What can this user access?"**

Examples:
- Can this user access the admin dashboard?
- Can they modify system settings?

#### SIMPLE ANALOGY

Imagine entering a building:
**Authentication** = Showing your ID at the door

They confirm you are XXXXXX.

**Authorization** = Deciding which rooms you can enter.
Maybe you can enter the lobby but not the server room.


-----


### Building a simple Auth System


📌 Install Dependencies

```python
pip install fastapi uvicorn pymongo bcrypt python-dotenv
```

🎯 Clone the repo from `main` branch

```
app/
│── main.py
│── database.py
│── models.py
│── routers/
│     ├── auth.py
│── utils/
│     ├── jwt_handler.py
│     ├── hashing.py
```

🚀 Run the server
```
uvicorn main:app --reload --port 8000
```

---

### HOW THE FLOW WORKS:

#### STEP 1 | SIGN UP FLOW

Create a simple sign up flow where the user can enter their name, email, gender and a password.

#### STEP 2 | HASH THE PASSWORD

Hashing is a one‑way transformation. You cannot get the original password back. This is why hashing is used for passwords.

Common password safe hashing algorithms are `bcrypt`, `argon2`, `scrypt`

These are called password hashing functions because they are:
- Salted (to prevent rainbow table attacks)
- Resistant to brute force

Use hashing for passwords. Never encryption, because encryption is reversible. You can decrypt the data back to the original. This is why encryption is NOT used for passwords. If someone steals your key, they can decrypt every password.

> A SALT is random data added to the password before hashing. `bcrypt`, `argon2`, `scrypt` all automatically salt passwords.
> Salting prevents
> Rainbow table attacks and 
> Identical passwords having identical hashes

#### STEP 3 | STORE THE USERS IN A DB

Have a proper users database or a collection (if mongo db)

This collection will contain the users
1. Name 
2. Email address
3. Password
4. And other demographic data 

For each user the document can be in this format:
```
{
  _id: ObjectId(...),
  name: “Mogan N”,
  email: “mk@example.com",
  gender: "male",
  password: <hashed_password>,
  created_at: <timestamp>
}
```

#### STEP 4 | USER LOGS IN

Once the user is all signed up and ready to login, client sends:

```
{
  "email": “mk@example.com",
  "password": "mypassword123"
}
```

Once the payload is sent to the backend, the following flow happens:
```
User enters Email + Password
            │
            ▼
Lookup User by Email in Database
            │
     ┌──────┴─────────┐
     │                │
User NOT found     User found
     │                │
     ▼                ▼
Return:           Hash entered password
"Sign up          (bcrypt / argon2)
to access"              │
                         ▼
              Compare with stored hash
                         │
                 ┌───────┴────────┐
                 │                │
             No match          Match
                 │                │
                 ▼                ▼
        "Invalid Credentials"  Login Success
                                (issue JWT / session)
```

---

### HOW A JWT (JSON Web Token) IS ISSUED


#### STEP 1 | CREATE A JWT PAYLOAD

For each user, from the users DB, include the necessary fields as a json entry:

```
{
  "user_id": "65a1f37hf2n8293n822",
  "name": "Mogan N",
  "email": "mk@example.com",
  "exp": <2 hours from now>
}
```

#### STEP 2 | SIGN THE PAYLOAD

Use one of the following signing algorithms to sign the json payload (most common): 

1. **HMAC** - Uses one shared secret key for both signing and verifying. It is fast, simple and best suited for single server apps.
2. **RSA** - Uses private key to sign and public key to verify. Ideal for distributed systems.

```
jwt.encode(payload, JWT_SECRET, algorithm="HS256")
```

This signed payload will be of a long strin of alphanumeric characters. Once this is created, return it to client.

#### STEP 3 | PROTECT ROUTES

Client sends this token with each request in the header

```
Authorization: Bearer <jwt_token>
```

The backend then verifies the token:
1. Extract token from header
2. Decode using the secret key (JWT_SECRET)
3. Check expiration
4. Load user from DB
5. Attach user info to each request

If token is invalid or expired → return `401`.

If all the above steps are completed, then USER GAINS ACCESS.






