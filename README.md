# 📁 Mobile-Friendly Flask File Server by Yogeshwaran Kumaran

A secure, mobile-optimized local file server built using Flask — allowing you to browse, upload, and download files from your PC using just your phone. Includes QR code and Ngrok-based remote access.

## 🌟 Features

- 🔐 Secure login with hashed credentials
- 📂 Browse your PC’s files and folders from mobile
- 📤 Upload files from phone directly to your PC
- 📄 Download files from PC to phone
- 📱 Fully responsive dark-themed UI for mobile devices
- 🌐 Remote access enabled via Ngrok tunnel
- 📷 Auto QR Code generation to open on mobile quickly
- 🚫 Basic protection against directory traversal

---

## 🛠️ Installation

1. **Clone this repo**
   git clone https://github.com/yogeshwaran-k/Personal-Local-Server.git
   cd Personal-Local-Server
   
3. **Install the Dependencies**
    pip install -r requirements.txt

4. **Install and Configure Ngrok**
    - Download Ngrok
    - Go to https://ngrok.com/download
    - Download and extract it for your OS (Windows/Mac/Linux)
   
    **Sign Up and Get Your Auth Token**
    - Sign up at https://dashboard.ngrok.com/signup
    - After signing in, you'll get an auth token from the Auth Token page

    **Add Auth Token to Ngrok**
    - Run this in terminal/command prompt (replace YOUR_AUTHTOKEN with your token):
    - ngrok config add-authtoken YOUR_AUTHTOKEN

5. **Run the Server**
    python start.py

    This will:
      - Start your Flask app locally on port 5000
      - Open a public HTTPS tunnel via Ngrok
      - Generate a QR code you can scan from your mobile
      - Automatically open the QR code image on your PC

6. **Open the Server on Your Mobile**
    - Scan the QR code displayed after launch OR copy-paste the printed Ngrok URL into your mobile browser

## 🔐 Default Login

Username: admin
Password: admin123

You can change them in server.py:
USERNAME = "admin"
PASSWORD_HASH = generate_password_hash("admin123")


---

## Preview

**Login Page in PC(Local Network)**

<img width="1919" height="1072" alt="image" src="https://github.com/user-attachments/assets/3d5a92e0-0d31-4ba4-bc3b-f333c5720865" />



**File Manager Page in PC(Local Network)**

<img width="1919" height="1023" alt="image" src="https://github.com/user-attachments/assets/0627b416-b3da-4420-91f6-d2e4334352bf" />



**Login Page in Mobile(Different Network by scanning the QR of Ngrok Tunnel)**

![1](https://github.com/user-attachments/assets/5e725f29-9d5b-4604-97f7-f0efaaf24237)



**File Manager Page in Mobile(Different Network by scanning the QR of Ngrok Tunnel)**

![2](https://github.com/user-attachments/assets/10ce1e94-9451-4fbb-9cb6-47edf6171d90)



**CLI Output**

<img width="717" height="358" alt="image" src="https://github.com/user-attachments/assets/51d6fca8-7242-47f6-9b60-6bba6c986806" />



## 🛑 Security Notice

- This project is intended for personal/local use only.
- Avoid deploying this to the public internet without TLS/HTTPS.
- Do not expose sensitive files or use this on untrusted networks.
- If you plan to extend this:
  - Add user roles
  - Enable HTTPS (e.g., via reverse proxy or Flask extension)
  - Use authentication tokens for upload/download APIs

## ✨ Future Improvements (Optional Ideas)

  - ✅ Create folders, rename/delete files
  - ✅ Upload progress bar
  - ✅ Drag-and-drop upload
  - ✅ Public links for shared files
  - ✅ Light/dark mode toggle

## ❤️ Credits

**Made with ❤️ by Yogeshwaran Kumaran**
- Portfolio : https://yogeshwaran-kumaran.netlify.app/
- Connect with me on LinkedIn : https://www.linkedin.com/in/yogeshwarankumaran/


