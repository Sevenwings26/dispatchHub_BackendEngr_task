# Star Wars Films API

A Django REST API for managing Star Wars films and comments, with data automatically fetched from SWAPI (Star Wars API). This project includes automated deployment to cloud platforms.

## 🚀 Features

- **Films Management**: Retrieve Star Wars films with comment counts
- **Comments System**: Add and view comments for films (500 character limit)
- **Auto Data Population**: Automatically fetches films from SWAPI on first run
- **RESTful API**: Clean, well-documented REST endpoints
- **Automated Deployment**: CI/CD pipeline with GitHub Actions
- **API Documentation**: Interactive Swagger/OpenAPI documentation

## 📋 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/healthz/` | RESTAPI Health Check |
| `GET` | `/` | Get all films with comment counts, sorted by release date |
| `GET` | `/films/{id}/comments/` | Get all comments for a specific film |
| `POST` | `/films/{id}/comments/add/` | Add a comment to a specific film |

## 🛠️ Installation & Local Development

### Prerequisites
- Python 3.9+
- PostgreSQL (for production) or SQLite (for development)

### 1. Clone the Repository
```bash
git clone https://github.com/Sevenwings26/dispatchHub_BackendEngr_task.git
cd dispatchHub
```

### 2. Set Up Environment
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your settings
```

### 3. Database Setup
```bash
# Run migrations
python manage.py migrate

# Create superuser (optional)
python manage.py createsuperuser
```

### 4. Run Development Server
```bash
python manage.py runserver
```

The API will be available at `http://localhost:8000/`

## 📚 API Usage

### Get All Films
```bash
curl -X GET http://localhost:8000/films/
```

Response:
```json
[
  {
    "id": 1,
    "title": "A New Hope",
    "release_date": "1977-05-25",
    "comment_count": 3
  }
]
```

### Get Film Comments
```bash
curl -X GET http://localhost:8000/films/1/comments/
```

### Add a Comment
```bash
curl -X POST http://localhost:8000/films/1/comments/add/ \
  -H "Content-Type: application/json" \
  -d '{"text": "This is a great film!"}'
```

## 🚀 Deployment

### Automated Deployment (CI/CD)

This project is configured for automatic deployment to Heroku when pushing to the main branch:

1. **Push to main branch** → GitHub Actions automatically runs tests and deploys
2. **Migrations** are automatically applied
3. **Static files** are collected automatically

### Manual Deployment

#### Heroku
```bash
# Login to Heroku
heroku login

# Create app
heroku create your-app-name

# Set environment variables
heroku config:set DEBUG=False
heroku config:set SECRET_KEY=your-secure-secret-key

# Deploy
git push heroku main

# Run migrations
heroku run python manage.py migrate
```

#### Render.com
1. Connect your GitHub repository to Render
2. Use the provided `render.yaml` for automatic configuration
3. Environment variables are automatically set

## 🏗️ Project Structure

```
dispatchHub/
├── films/                 # Main app
│   ├── models.py         # Film and Comment models
│   ├── views.py          # API views
│   ├── serializers.py    # DRF serializers
│   └── urls.py           # App URL routes
├── dispatchHub/          # Project settings
│   ├── settings.py       # Django settings
│   ├── urls.py          # Project URL routes
│   └── wsgi.py          # WSGI configuration
├── .github/workflows/    # CI/CD configuration
│   └── ci-cd.yml        # GitHub Actions workflow
├── requirements.txt      # Python dependencies

```

## 🔧 Configuration

### Environment Variables

Create a `.env` file with:

```env
DEBUG=True
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///db.sqlite3
```

### Production Settings

- Debug mode is disabled
- PostgreSQL database
- WhiteNoise for static files
- Gunicorn as WSGI server
- Secure HTTPS configuration

## 📊 API Documentation

Interactive API documentation is available at:
- Swagger UI: `/api/docs/`
- OpenAPI Schema: `/api/schema/`

## 🧪 Testing

```bash
# Run tests
python manage.py test

# Run with coverage
coverage run manage.py test
coverage report
```

## 🔄 Data Source

Films are automatically populated from [SWAPI](https://swapi.dev/) (Star Wars API) when the database is empty. The first API call to `/films/` will trigger this population.

## 📦 Dependencies

### Main Dependencies
- Django 4.2.7
- Django REST Framework 3.14.0
- drf-spectacular 0.28.0 (API documentation)
- Gunicorn (Production WSGI server)
- WhiteNoise (Static file serving)
- PostgreSQL (Production database)

### Development Dependencies
- python-dotenv (Environment management)
- requests (HTTP client for SWAPI integration)

## 🐛 Troubleshooting

### Common Issues

1. **Import Errors**: Ensure all dependencies are installed with `pip install -r requirements.txt`
2. **Database Issues**: Run `python manage.py migrate` to apply migrations
3. **Static Files**: Run `python manage.py collectstatic` before deployment
4. **SWAPI Connection**: Check internet connection for initial data population

### Logs

- **Heroku**: `heroku logs --tail`
- **Render**: Check dashboard logs
- **Local**: Check console output or Django debug page

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- [SWAPI](https://swapi.dev/api) for Star Wars data
- [Django REST Framework](https://www.django-rest-framework.org/) for the API framework
- [drf-spectacular](https://drf-spectacula  r.readthedocs.io/) for API documentation
- [Heroku](https://www.heroku.com/) and [Render](https://render.com/) for deployment platforms
