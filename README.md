# Toasty 🍞

A GitHub App that responds to `/plan` commands on issues and provides a structured code implementation plan.

## Features

- 🤖 Responds to `/plan` commands in issue comments
- 📋 Generates structured implementation plans
- 🚀 Built with Probot framework for reliability

## How to Use

Once installed on a repository, simply comment `/plan` on any issue, and Toasty will respond with a structured code plan based on the issue title and description.

### Example

1. Create or open an issue
2. Add a comment: `/plan`
3. Toasty will respond with a detailed implementation plan

## Setup

### Prerequisites

- Node.js 18 or higher
- A GitHub account

### Local Development

1. Clone this repository:
   ```bash
   git clone https://github.com/OWASP-BLT/Toasty.git
   cd Toasty
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Create a GitHub App:
   - Go to [GitHub Apps settings](https://github.com/settings/apps/new)
   - Set the following:
     - **GitHub App name**: Choose a unique name
     - **Homepage URL**: Your repository URL
     - **Webhook URL**: Your webhook URL (use [Smee.io](https://smee.io) for local testing)
     - **Webhook secret**: Generate a random string
     - **Permissions**: 
       - Issues: Read & Write
       - Contents: Read-only
     - **Subscribe to events**: Issue comment
   - Click "Create GitHub App"
   - Generate and download a private key

4. Configure environment variables:
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` and add your values:
   ```
   APP_ID=your-app-id
   WEBHOOK_SECRET=your-webhook-secret
   PRIVATE_KEY_PATH=path-to-your-private-key.pem
   ```

5. Install the app on a repository:
   - Go to your app's settings page
   - Click "Install App"
   - Choose repositories to install on

6. Start the development server:
   ```bash
   npm start
   ```

   For development with auto-reload:
   ```bash
   npm run dev
   ```

## Deployment

### Deploy to Heroku

1. Create a new Heroku app:
   ```bash
   heroku create
   ```

2. Set environment variables:
   ```bash
   heroku config:set APP_ID=your-app-id
   heroku config:set WEBHOOK_SECRET=your-webhook-secret
   heroku config:set PRIVATE_KEY="$(cat your-private-key.pem)"
   ```

3. Deploy:
   ```bash
   git push heroku main
   ```

### Deploy to Glitch

1. Go to [Glitch](https://glitch.com)
2. Click "New Project" → "Import from GitHub"
3. Enter `OWASP-BLT/Toasty`
4. Add your environment variables in the `.env` file

## Configuration

The app can be configured using environment variables:

- `APP_ID`: Your GitHub App ID
- `WEBHOOK_SECRET`: Your webhook secret
- `PRIVATE_KEY_PATH`: Path to your private key file
- `PRIVATE_KEY`: Or paste your private key directly
- `PORT`: Port to run the app on (default: 3000)
- `LOG_LEVEL`: Logging level (default: info)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT

## Support

For issues and questions, please open an issue on the [GitHub repository](https://github.com/OWASP-BLT/Toasty/issues).
