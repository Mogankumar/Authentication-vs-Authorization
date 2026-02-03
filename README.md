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


---


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
