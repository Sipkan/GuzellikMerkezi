# 🚀 Deployment Guide — Pınar Seda Sayan Güzellik Dünyası

## 📖 Glossary — What Do These Terms Mean?

| Term | Ne Demek? (What It Means) |
|------|---------------------------|
| **Domain** | Your website address (e.g., `pinarsedasayan.com`). Like a phone number for your website. |
| **DNS** | Domain Name System — translates your domain name to your server's IP address. Like a phone book. |
| **Cloudflare** | A company that sells domains and provides free CDN + SSL. Acts as a shield in front of your server. |
| **CDN** | Content Delivery Network — caches your site across the world so it loads faster for visitors. |
| **SSL / HTTPS** | The 🔒 padlock in the browser. Encrypts data between visitors and your site. Cloudflare gives this for free. |
| **DigitalOcean** | A cloud hosting company where you rent a virtual server (called a "Droplet"). |
| **Droplet** | DigitalOcean's name for a virtual server — a computer in the cloud running 24/7. |
| **Ubuntu** | A Linux operating system. Your server runs on this (not Windows). |
| **SSH** | Secure Shell — how you remotely connect to your server from your PC. Like remote desktop, but text-based. |
| **SSH Key** | A pair of files (public + private) used to login to your server securely without a password. |
| **Nginx** | A web server that sits in front of your app. It receives requests from the internet and forwards them to your FastAPI app. |
| **Reverse Proxy** | What Nginx does — it takes incoming traffic and "proxies" it to your app running on port 8001. |
| **Uvicorn** | The Python server that actually runs your FastAPI app. |
| **Systemd** | Ubuntu's service manager — keeps your app running 24/7, restarts it if it crashes. |
| **PostgreSQL** | The database where customer contact form submissions are stored. |
| **Firewall (UFW)** | Controls which ports are open on your server. Only allows web traffic (80, 443) and SSH (22). |
| **Git Branch** | A separate version of your code. You'll deploy from a `production` branch to keep it clean. |
| **`.env` file** | A secret file on your server with passwords (database URL). Never push this to GitHub! |

---

## 🌿 Branch Strategy

```
main ←── development & new features
  │
  └── production ←── what runs on the live server
```

- You work on **`main`** locally
- When ready to deploy, merge into **`production`**
- The server pulls from **`production`** only

---

## Step-by-Step Summary

### 1️⃣ Buy Domain (~5 min)
- Go to [Cloudflare](https://dash.cloudflare.com) → Domain Registration → Search `pinarsedasayan.com` → Buy (~$10/year)

### 2️⃣ Create Server (~5 min)
- Go to [DigitalOcean](https://cloud.digitalocean.com) → Create Droplet
- Pick: **Ubuntu 22.04**, **Frankfurt**, **$6/month plan**
- Add your SSH key (or use password)
- Note the **IP address** after creation

### 3️⃣ Connect to Server
```bash
ssh root@YOUR_SERVER_IP
```

### 4️⃣ Install Everything on Server (~10 min)
```bash
# Update system
apt update && apt upgrade -y

# Install PostgreSQL
apt install postgresql postgresql-contrib -y

# Install Python & Git
apt install python3 python3-pip python3-venv git -y

# Install Nginx
apt install nginx -y
```

### 5️⃣ Setup Database (~5 min)
```bash
sudo -u postgres psql
```
```sql
CREATE USER merkez_user WITH PASSWORD 'YOUR_SECURE_PASSWORD';
CREATE DATABASE merkez OWNER merkez_user;
GRANT ALL PRIVILEGES ON DATABASE merkez TO merkez_user;
\q
```

Then allow password login:
```bash
# Edit: change 'peer' to 'md5' on the "local all all" line
nano /etc/postgresql/14/main/pg_hba.conf
systemctl restart postgresql
```

### 6️⃣ Create App User
```bash
adduser --disabled-password --gecos "" appuser
```

### 7️⃣ Create Production Branch & Push (on your Windows PC)
```powershell
cd C:\Users\busin\PycharmProjects\Merkez

# Create and switch to production branch
git checkout -b production

# Push to GitHub
git push -u origin production
```

### 8️⃣ Clone Code on Server
```bash
su - appuser
git clone -b production https://github.com/YOUR_USERNAME/Merkez.git /home/appuser/app
cd /home/appuser/app

# Setup Python
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 9️⃣ Create .env on Server
```bash
nano /home/appuser/app/.env
```
```
DATABASE_URL=postgresql+asyncpg://merkez_user:YOUR_SECURE_PASSWORD@localhost:5432/merkez
```

### 🔟 Configure Nginx
```bash
# As root
nano /etc/nginx/sites-available/merkez
```
```nginx
server {
    listen 80;
    server_name pinarsedasayan.com www.pinarsedasayan.com;

    location / {
        proxy_pass http://127.0.0.1:8001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static/ {
        alias /home/appuser/app/app/static/;
        expires 30d;
    }
}
```
```bash
ln -s /etc/nginx/sites-available/merkez /etc/nginx/sites-enabled/
rm /etc/nginx/sites-enabled/default
nginx -t && systemctl restart nginx
```

### 1️⃣1️⃣ Create Systemd Service (App runs forever)
```bash
nano /etc/systemd/system/merkez.service
```
```ini
[Unit]
Description=Merkez Beauty Center
After=network.target postgresql.service

[Service]
User=appuser
WorkingDirectory=/home/appuser/app
Environment="PATH=/home/appuser/app/venv/bin"
EnvironmentFile=/home/appuser/app/.env
ExecStart=/home/appuser/app/venv/bin/uvicorn app.main:app --host 127.0.0.1 --port 8001 --workers 2
Restart=always

[Install]
WantedBy=multi-user.target
```
```bash
systemctl daemon-reload
systemctl enable merkez
systemctl start merkez
```

### 1️⃣2️⃣ Setup Firewall
```bash
ufw allow OpenSSH
ufw allow 'Nginx Full'
ufw enable
```

### 1️⃣3️⃣ Cloudflare DNS
In Cloudflare Dashboard → DNS → Add records:

| Type | Name | Value |
|------|------|-------|
| A | `@` | YOUR_SERVER_IP |
| A | `www` | YOUR_SERVER_IP |

Then: SSL/TLS → Set to **"Full"**

### 1️⃣4️⃣ Submit to Google
- [Google Search Console](https://search.google.com/search-console) → Add `pinarsedasayan.com` → Submit sitemap
- [Google Business](https://business.google.com) → Create listing for your beauty center

---

## 🔄 How to Deploy Updates

On your **Windows PC**:
```powershell
# 1. Commit your changes on main
git add .
git commit -m "Yeni değişiklikler"

# 2. Merge into production
git checkout production
git merge main
git push origin production

# 3. Go back to main for future work  
git checkout main
```

On the **server** (via SSH):
```bash
ssh root@YOUR_SERVER_IP
su - appuser
cd /home/appuser/app
git pull origin production
exit
systemctl restart merkez
```

---

## 🗄️ Database Quick Commands

```bash
# Connect to database
sudo -u postgres psql -d merkez

# See all contact requests
SELECT * FROM callback_requests ORDER BY created_at DESC;

# Backup
pg_dump -U merkez_user -h localhost merkez > backup.sql

# Restore
psql -U merkez_user -h localhost merkez < backup.sql
```

---

## 💰 Total Cost: ~$7/month

| Item | Cost |
|------|------|
| DigitalOcean | $6/month |
| Cloudflare Domain | ~$10/year |
| SSL, CDN, DNS | Free |
| PostgreSQL | Free (self-hosted) |
