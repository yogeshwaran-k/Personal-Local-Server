from flask import Flask, request, session, redirect, render_template_string, send_file
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.secret_key = "super_secret_key"

# Configuration
USERNAME = "admin"
PASSWORD_HASH = generate_password_hash("admin123")
BASE_DIR = os.path.expanduser("~")
UPLOAD_DIR = os.path.join(BASE_DIR, "MobileUploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

# ------------ HTML Templates ------------

LOGIN_PAGE = '''
<!DOCTYPE html>
<html>
<head>
  <title>Login</title>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <style>
    body {
      font-family: sans-serif;
      background: #121212;
      color: #fff;
      display: flex;
      align-items: center;
      justify-content: center;
      height: 100vh;
      margin: 0;
      overflow-x: hidden;
    }
    .login-box {
      background: #1e1e1e;
      padding: 30px;
      border-radius: 12px;
      width: 90%;
      max-width: 400px;
      box-shadow: 0 0 10px rgba(0,0,0,0.5);
      text-align: center;
    }
    .input-btn {
      width: 100%;
      padding: 12px;
      margin-top: 15px;
      border-radius: 8px;
      border: none;
      font-size: 16px;
      box-sizing: border-box;
    }
    input { background: #333; color: white; }
    button { background: #007bff; color: white; cursor: pointer; }
    h2 { margin-bottom: 20px; }
    .card { margin-top: 20px; font-size: 14px; }
    a { text-decoration: none; color: rgb(0, 136, 255); }

    #popup-img {
      position: fixed;
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%);
      z-index: 999;
      display: none;
      max-width: 300px;
      border-radius: 12px;
      box-shadow: 0 0 20px rgba(0,0,0,0.6);
    }
  </style>
</head>
<body>
  <div class="login-box">
    <h2>🔐 YK Local Server</h2>
    <form onsubmit="return login(event)">
      <input type="text" id="username" class="input-btn" placeholder="Username" required>
      <input type="password" id="password" class="input-btn" placeholder="Password" required>
      <button type="submit" class="input-btn">Login</button>
    </form>
    <div class="card">
      <a href="https://yogeshwaran-k.orgfree.com">Made with ❤️ by Yogeshwaran Kumaran</a>
    </div>
  </div>

  <img id="popup-img" src="" alt="Popup Image">

  <script>
    function showImagePopup(imgUrl) {
      const popup = document.getElementById("popup-img");
      popup.src = imgUrl;
      popup.style.display = "block";
      setTimeout(() => {
        popup.style.display = "none";
      }, 3000);
    }

    async function login(event) {
      event.preventDefault();
      const username = document.getElementById("username").value;
      const password = document.getElementById("password").value;

      const formData = new FormData();
      formData.append("username", username);
      formData.append("password", password);

      const response = await fetch("/login", { method: "POST", body: formData });
      const result = await response.text();

      if (response.status === 200) {
        showImagePopup("https://media.giphy.com/media/111ebonMs90YLu/giphy.gif");
        setTimeout(() => {
          alert("🎉 Welcome Yoyo! Login successful.");
          window.location.href = "/browse";
        }, 1000);
      } else {
        showImagePopup("https://media.giphy.com/media/3o6ZtaO9BZHcOjmErm/giphy.gif");
        setTimeout(() => {
          alert("❌ You Illegal Entry.");
        }, 1000);
      }
    }
  </script>
</body>
</html>
'''

BROWSER_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
  <title>📁 File Browser</title>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <style>
    :root {
      color-scheme: dark;
    }
    body {
      margin: 0;
      font-family: 'Segoe UI', sans-serif;
      background: #121212;
      color: #ffffff;
      padding: 16px;
    }

    .container {
      max-width: 600px;
      margin: auto;
    }

    h2 {
      font-size: 18px;
      margin: 16px 0;
      word-break: break-all;
    }

    .item {
      display: flex;
      align-items: center;
      padding: 12px;
      background: #1e1e1e;
      border-radius: 10px;
      margin: 6px 0;
      text-decoration: none;
      color: #90caf9;
      transition: background 0.2s;
    }

    .item:hover {
      background: #292929;
    }

    .item span {
      margin-left: 10px;
      font-size: 16px;
    }

    .folder-icon {
      color: #ffcc00;
    }

    .file-icon {
      color: #90caf9;
    }

    .back-link {
      color: #f44336;
      font-weight: bold;
      display: inline-block;
      margin-bottom: 12px;
    }

    .logout {
      position: fixed;
      top: 15px;
      right: 20px;
      background: #e53935;
      color: white;
      padding: 8px 14px;
      border-radius: 8px;
      text-decoration: none;
      font-size: 14px;
    }

    form {
      margin-top: 30px;
      background: #1e1e1e;
      padding: 16px;
      border-radius: 12px;
      box-shadow: 0 0 8px rgba(0,0,0,0.3);
    }

    input[type="file"] {
      width: 100%;
      background: #2e2e2e;
      border: none;
      color: white;
      padding: 10px;
      margin-bottom: 14px;
      border-radius: 8px;
      font-size: 14px;
    }

    button {
      width: 100%;
      padding: 12px;
      font-size: 16px;
      background: #007bff;
      border: none;
      border-radius: 8px;
      color: white;
      font-weight: bold;
      cursor: pointer;
    }

    button:hover {
      background: #0056b3;
    }

    .footer {
      margin-top: 30px;
      text-align: center;
      font-size: 14px;
      color: #aaa;
    }

    .footer a {
      color: #90caf9;
      text-decoration: none;
    }

    .toggle-mode {
      text-align: center;
      margin-top: 20px;
      font-size: 13px;
      color: #ccc;
    }

    @media (hover: none) {
      .logout { font-size: 12px; padding: 6px 10px; }
    }
  </style>
</head>
<body>

<a class="logout" href="/logout">Logout</a>

<div class="container">

  {% if parent %}
    <a class="back-link" href="/browse?path={{ parent }}">⬅ Back</a>
  {% endif %}

  <h2>📂 {{ path }}</h2>

  {% for name, full, is_dir in contents %}
    {% if is_dir %}
      <a class="item" href="/browse?path={{ full }}">
        <span class="folder-icon">📁</span>
        <span>{{ name }}</span>
      </a>
    {% else %}
      <a class="item" href="/download?file={{ full }}">
        <span class="file-icon">📄</span>
        <span>{{ name }}</span>
      </a>
    {% endif %}
  {% endfor %}

  <form action="/upload?path={{ path }}" method="POST" enctype="multipart/form-data">
    <h3>📤 Upload a File</h3>
    <input type="file" name="file" required>
    <button type="submit">Upload</button>
  </form>

  <div class="toggle-mode">🌙 Dark mode is on</div>

  <div class="footer">
    Personal Local Server. Made with ❤️ by <a href="https://yogeshwaran-k.orgfree.com" target="_blank">Yogeshwaran Kumaran</a>
  </div>

</div>
</body>
</html>
'''


# ------------ Routes ------------

@app.route('/')
def index():
    if session.get("logged_in"):
        return redirect('/browse')
    return LOGIN_PAGE

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get("username")
    password = request.form.get("password")
    if username == USERNAME and check_password_hash(PASSWORD_HASH, password):
        session["logged_in"] = True
        return "OK", 200
    return "Invalid credentials", 403

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/browse')
def browse():
    if not session.get("logged_in"):
        return redirect('/')
    path = request.args.get("path", BASE_DIR)
    path = os.path.abspath(path)

    if not path.startswith(BASE_DIR):
        return "Access denied", 403

    parent = os.path.dirname(path) if path != BASE_DIR else ''
    try:
        entries = sorted(os.listdir(path))
    except:
        return "Cannot access folder"

    contents = []
    for entry in entries:
        full = os.path.join(path, entry)
        contents.append((entry, full, os.path.isdir(full)))
    return render_template_string(BROWSER_TEMPLATE, path=path, parent=parent, contents=contents)

@app.route('/upload', methods=['POST'])
def upload_file():
    if not session.get("logged_in"):
        return redirect('/')

    # Get the path from query parameters
    path = request.args.get("path", BASE_DIR)
    path = os.path.abspath(path)

    # Prevent directory traversal
    if not path.startswith(BASE_DIR):
        return "Access denied", 403

    if 'file' not in request.files:
        return "No file part", 400

    f = request.files['file']
    if f.filename == '':
        return "No file selected", 400

    filename = secure_filename(f.filename)
    save_path = os.path.join(path, filename)

    try:
        f.save(save_path)
        return redirect('/browse?path=' + path)
    except Exception as e:
        return f"Upload failed: {e}", 500


@app.route('/download')
def download():
    if not session.get("logged_in"):
        return redirect('/')
    file = request.args.get("file")
    if not file or not os.path.isfile(file):
        return "File not found", 404
    if not os.path.abspath(file).startswith(BASE_DIR):
        return "Access denied", 403
    return send_file(file, as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
