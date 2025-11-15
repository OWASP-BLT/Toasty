# Quick Start Guide

Get Toasty up and running in minutes!

## For Users (Installing the App)

Once Toasty is deployed and available as a GitHub App:

1. Go to the GitHub App installation page
2. Click "Install"
3. Choose which repositories to install it on
4. That's it! Now you can use `/plan` on any issue in those repositories

## For Developers (Running Locally)

### Prerequisites
- Node.js 18+ installed
- A GitHub account

### Steps

1. **Clone and Install**
   ```bash
   git clone https://github.com/OWASP-BLT/Toasty.git
   cd Toasty
   npm install
   ```

2. **Create a GitHub App**
   - Visit https://github.com/settings/apps/new
   - Fill in:
     - App name: `Toasty-Dev` (or your choice)
     - Homepage URL: `https://github.com/OWASP-BLT/Toasty`
     - Webhook URL: `https://smee.io/new` (get a new channel)
   - Set permissions:
     - Issues: Read & write
     - Contents: Read-only
   - Subscribe to events:
     - Issue comment
   - Click "Create GitHub App"
   - Generate and download a private key

3. **Configure Environment**
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env`:
   ```
   APP_ID=12345                                    # From app settings
   WEBHOOK_SECRET=your-secret                       # You created this
   PRIVATE_KEY_PATH=./path-to-private-key.pem      # Downloaded file
   ```

4. **Install the App**
   - Go to your app's page (in GitHub settings)
   - Click "Install App"
   - Choose a test repository

5. **Start the Server**
   ```bash
   npm start
   ```

6. **Test It**
   - Go to your test repository
   - Create or open an issue
   - Comment: `/plan`
   - Toasty should respond with a plan! 🍞

## Troubleshooting

### App not responding?
- Check that webhook events are being received (check Smee.io channel)
- Verify your `.env` file has correct values
- Check server logs for errors

### Permission errors?
- Ensure the app has "Issues: Write" permission
- Re-install the app on the repository

### Need help?
Open an issue at https://github.com/OWASP-BLT/Toasty/issues
