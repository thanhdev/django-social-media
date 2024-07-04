# Django Social Media Project

This project is a simple social media application built with Django. It allows users to create an account, post content, and view posts from other users.

## Features

- User authentication (sign up, log in, log out)
- Posting content with text and images
- Viewing a feed of posts from all users

## Technologies Used

- Python
- Django
- HTML/CSS
- Tailwind CSS for styling
- PostgreSQL for the database
- Docker for containerization

## Getting Started

To get this project running on your local machine, follow these steps:

### Prerequisites

- Python 3.8 or higher
- pip
- Docker and Docker Compose

### Installation

1. Clone the repository to your local machine:
   ```
   git clone https://github.com/<your-username>/django-social-media.git
   ```
2. Navigate to the project directory:
   ```
   cd django-social-media
   ```
3. Create a `.env` file in the project root directory with the following contents:
   ```
   DEBUG=0
   SECRET_KEY=your_secret_key
   DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1 [::1]
   SQL_ENGINE=django.db.backends.postgresql
   SQL_DATABASE=social_media
   SQL_USER=social_media_user
   SQL_PASSWORD=social_media_password
   SQL_HOST=db
   SQL_PORT=5432
   DATABASE=postgres
   ```
4. Create a `.env.db` file in the project root directory with the following contents:
   ```
   POSTGRES_DB=your_db_name
   POSTGRES_USER=your_db_user
   POSTGRES_PASSWORD=your_db_password
   POSTGRES_HOST=db
   POSTGRES_PORT=5432
   ```
5. Build and access the Docker container:
   ```
   sh run.sh
   ```
6. Create a superuser for Django admin (optional):
   ```
   python manage.py createsuperuser
   ```
7. Run the server:
   ```
   sh server.sh
   ```
8. Visit `http://localhost:8000` in your web browser to view the application.

## Configuration

- The database settings can be configured in the `.env.db` file.
- Additional Django settings can be configured in the `.env` file.

## Deployment
1. Manual Deployment
   ```
   docker compose -f docker-compose.production.yml up --build
   ```
2. Continuous Deployment
   ```
   nohup ./cd.py &
   ```

## Contributing

Contributions are welcome! Please feel free to submit a pull request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
