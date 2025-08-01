# Deployment Guide for Render

## Quick Deployment Steps

### 1. Prepare Your Repository

Make sure your code is pushed to GitHub with all the necessary files:
- `requirements.txt`
- `render.yaml`
- `build.sh`
- `blog_project/settings.py` (updated for production)
- `blog_project/urls.py` (updated for production)

### 2. Deploy on Render

1. **Go to [Render Dashboard](https://dashboard.render.com/)**
2. **Click "New +" and select "Blueprint"**
3. **Connect your GitHub repository**
4. **Render will automatically detect the `render.yaml` file**
5. **Click "Apply" to deploy**

### 3. Manual Deployment (Alternative)

If you prefer manual deployment:

1. **Create a new Web Service**
   - Connect your GitHub repository
   - Set **Build Command**: `pip install -r requirements.txt`
   - Set **Start Command**: `gunicorn blog_project.wsgi:application`

2. **Add Environment Variables**
   - `SECRET_KEY`: Generate a secure key (use Django's `get_random_secret_key()`)
   - `DEBUG`: `false`
   - `RENDER_EXTERNAL_HOSTNAME`: Your app's URL (e.g., `your-app.onrender.com`)

3. **Add PostgreSQL Database**
   - Create a new PostgreSQL database
   - Link it to your web service

4. **Add Redis Service**
   - Create a new Redis service
   - Link it to your web service

### 4. Environment Variables

Set these in your Render dashboard:

```
SECRET_KEY=your-secure-secret-key-here
DEBUG=false
RENDER_EXTERNAL_HOSTNAME=your-app-name.onrender.com
```

The following will be automatically set by Render:
- `DATABASE_URL` (from PostgreSQL)
- `REDIS_URL` (from Redis)

### 5. Generate a Secure Secret Key

Run this in your local Django shell:
```python
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

### 6. Post-Deployment

After deployment:
1. **Run migrations**: Render will do this automatically via `build.sh`
2. **Create a superuser**: Use Django admin or Render shell
3. **Test your application**: Visit your Render URL

## Troubleshooting

### Common Issues

1. **Build Fails**
   - Check `requirements.txt` for correct package versions
   - Ensure all dependencies are listed

2. **Database Connection Issues**
   - Verify `DATABASE_URL` is set correctly
   - Check if PostgreSQL service is running

3. **Static Files Not Loading**
   - Ensure `collectstatic` runs during build
   - Check WhiteNoise configuration

4. **Redis Connection Issues**
   - Verify `REDIS_URL` is set correctly
   - Check if Redis service is running

### Debug Commands

Run these in Render's shell:
```bash
python manage.py check --deploy
python manage.py collectstatic --noinput
python manage.py migrate
```

### Performance Tips

1. **Enable caching** for better performance
2. **Use CDN** for static files in production
3. **Monitor your app** using Render's dashboard

## Support

If you encounter issues:
1. Check Render's logs in the dashboard
2. Verify all environment variables are set
3. Test locally with production settings
4. Check Django's deployment checklist: `python manage.py check --deploy` 