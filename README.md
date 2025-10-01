# UID Management Server

A Flask-based UID management system with expiration tracking and external API integration.

## Features

- ✅ Add UIDs with custom expiration
- ✅ Permanent UIDs support
- ✅ Automatic cleanup of expired UIDs
- ✅ External server integration
- ✅ RESTful API endpoints

## API Endpoints

- `GET/POST /add_uid` - Add a new UID
- `GET /get_time/<uid>` - Check remaining time
- `DELETE /delete_uid/<uid>` - Delete a UID
- `GET /list_uids` - List all UIDs
- `GET /health` - Health check
- `POST /force_cleanup` - Force cleanup

## Deployment

### Vercel Deployment
1. Fork this repository
2. Connect to Vercel
3. Deploy automatically

### Local Development
```bash
pip install -r requirements.txt
python app.py