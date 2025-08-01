# Django Blog Application

A modern blog application built with Django, featuring user authentication, real-time chat, and recommendation systems.

## Features

- User authentication and registration
- Blog post creation and management
- Real-time chat functionality
- Dark mode toggle
- Search functionality
- Responsive design with Bootstrap
- Recommendation system

## Local Development

### Prerequisites

- Python 3.10+
- Redis server
- Virtual environment

### Setup

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables (create a `.env` file):
   ```
   SECRET_KEY=your-secret-key-here
   DEBUG=True
   REDIS_URL=redis://localhost:6379
   ```

5. Run migrations:
   ```bash
   python manage.py migrate
   ```

6. Start Redis server:
   ```bash
   redis-server
   ```

7. Run the development server:
   ```bash
   python manage.py runserver
   ```

8. Visit http://localhost:8000

## Deployment on Render

### Prerequisites

- Render account
- GitHub repository with your code

### Deployment Steps

1. **Connect your GitHub repository to Render**

2. **Create a new Web Service**
   - Choose your repository
   - Set the following configuration:
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `gunicorn blog_project.wsgi:application`

3. **Set Environment Variables**
   - `SECRET_KEY`: Generate a secure secret key
   - `DEBUG`: Set to `false`
   - `DATABASE_URL`: Will be automatically set by Render
   - `REDIS_URL`: Will be automatically set by Render

4. **Add PostgreSQL Database**
   - Create a new PostgreSQL database in Render
   - The `DATABASE_URL` will be automatically linked

5. **Add Redis Service**
   - Create a new Redis service in Render
   - The `REDIS_URL` will be automatically linked

6. **Deploy**
   - Render will automatically deploy your application
   - Your app will be available at `https://your-app-name.onrender.com`

### Environment Variables for Production

```
SECRET_KEY=your-secure-secret-key
DEBUG=false
DATABASE_URL=postgresql://user:password@host:port/database
REDIS_URL=redis://host:port
RENDER_EXTERNAL_HOSTNAME=your-app-name.onrender.com
```

## File Structure

```
├── blog_project/          # Django project settings
├── blog/                  # Blog app
├── users/                 # User authentication app
├── api/                   # API app
├── templates/             # HTML templates
├── media/                 # User uploaded files
├── staticfiles/           # Collected static files
├── requirements.txt       # Python dependencies
├── render.yaml           # Render deployment config
└── build.sh              # Build script for Render
```

## Technologies Used

- **Backend**: Django 5.2
- **Database**: PostgreSQL (production), SQLite (development)
- **Cache/Channels**: Redis
- **Frontend**: Bootstrap 5, HTML, CSS, JavaScript
- **Deployment**: Render
- **WSGI Server**: Gunicorn
- **Static Files**: WhiteNoise

## License

This project is open source and available under the MIT License. 