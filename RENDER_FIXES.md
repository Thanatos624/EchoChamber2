# Render Deployment Fixes

## Issues Fixed

### 1. **Media Directory Error**
**Problem**: `UserWarning: No directory at: /opt/render/project/src/media/`
**Solution**: 
- Updated `wsgi.py` to check if media directory exists before serving files
- Updated `build.sh` to create media directory during deployment
- Updated `urls.py` to handle media serving more robustly

### 2. **ALLOWED_HOSTS Configuration**
**Problem**: Application not trusting Render's domain
**Solution**: 
- Improved `settings.py` to properly handle `RENDER_EXTERNAL_HOSTNAME`
- Added explicit environment variable in `render.yaml`

### 3. **Error Handling**
**Problem**: No way to debug deployment issues
**Solution**: 
- Added health check endpoint at `/health/`
- Better error handling in media file serving

## Files Modified

### 1. `blog_project/wsgi.py`
```python
# Before: Always tried to serve media files
application = WhiteNoise(application, root=os.path.join(...))

# After: Check if directory exists first
media_root = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'media')
if os.path.isdir(media_root):
    application = WhiteNoise(application, root=media_root)
```

### 2. `blog_project/settings.py`
```python
# Before: Basic ALLOWED_HOSTS setup
ALLOWED_HOSTS = ['127.0.0.1', 'localhost']
RENDER_EXTERNAL_HOSTNAME = config('RENDER_EXTERNAL_HOSTNAME', default=None)
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)

# After: More explicit configuration
RENDER_EXTERNAL_HOSTNAME = config('RENDER_EXTERNAL_HOSTNAME', default=None)
ALLOWED_HOSTS = ['127.0.0.1', 'localhost']
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)
```

### 3. `build.sh`
```bash
# Added: Create media directory
mkdir -p media
```

### 4. `blog_project/urls.py`
```python
# Before: Always serve media files in production
urlpatterns += [re_path(r'^media/(?P<path>.*)$', serve, ...)]

# After: Check if directory exists first
if os.path.exists(settings.MEDIA_ROOT):
    urlpatterns += [re_path(r'^media/(?P<path>.*)$', serve, ...)]
```

### 5. `render.yaml`
```yaml
# Added: Explicit RENDER_EXTERNAL_HOSTNAME
- key: RENDER_EXTERNAL_HOSTNAME
  value: "django-blog-app.onrender.com"
```

### 6. `blog/views.py` & `blog/urls.py`
```python
# Added: Health check endpoint
def health_check(request):
    # Returns JSON with deployment status
    return JsonResponse({...})

# URL: /health/
```

## Testing the Fixes

### 1. **Local Testing**
```bash
# Test configuration
python manage.py check --deploy

# Test health endpoint (after starting server)
curl http://localhost:8001/health/
```

### 2. **Render Deployment**
1. Push changes to GitHub
2. Render will automatically redeploy
3. Check logs for any errors
4. Visit `/health/` endpoint to verify deployment

### 3. **Health Check Endpoint**
Visit `https://your-app.onrender.com/health/` to see:
- Database connection status
- Media directory status
- Static files status
- Debug mode status
- Allowed hosts configuration

## Expected Results

After deployment, you should see:
- ✅ No more 500 errors
- ✅ Application loads successfully
- ✅ Media files work (when uploaded)
- ✅ Health check returns `{"status": "healthy"}`

## Troubleshooting

### If you still get 500 errors:

1. **Check Render logs** in the dashboard
2. **Visit `/health/` endpoint** to see detailed status
3. **Verify environment variables** are set correctly
4. **Check database connection** in Render dashboard

### Common issues:

1. **Database not connected**: Check `DATABASE_URL` in environment variables
2. **Redis not connected**: Check `REDIS_URL` in environment variables
3. **Static files not loading**: Check if `collectstatic` ran successfully
4. **Media files not loading**: Check if media directory was created

## Next Steps

1. **Deploy the updated code** to Render
2. **Monitor the logs** for any remaining issues
3. **Test the application** thoroughly
4. **Create a superuser** if needed for admin access
5. **Upload some test images** to verify media functionality 