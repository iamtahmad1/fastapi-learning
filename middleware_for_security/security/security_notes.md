2️⃣ Security Headers in FastAPI
What Are Security Headers?

Security headers are extra HTTP response headers that protect web applications from common attacks. They help prevent:
✅ Cross-site scripting (XSS) – Injecting malicious scripts into web pages.
✅ Clickjacking attacks – Embedding your site inside an attacker’s site using <iframe>.
✅ Data leaks – Restricting what browsers can load from your site.

Common Security Headers
X-Frame-Options	Prevents clickjacking by blocking <iframe> embedding.
Content-Security-Policy (CSP)	Blocks XSS by restricting allowed scripts, styles, and sources.
X-XSS-Protection	Enables browser-based XSS protection.
Strict-Transport-Security (HSTS)	Enforces HTTPS to prevent man-in-the-middle attacks.
X-Content-Type-Options	Stops MIME-type sniffing to prevent malicious file execution.
Referrer-Policy	Controls what referrer information is sent when navigating between sites.