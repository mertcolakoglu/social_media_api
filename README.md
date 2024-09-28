# Social Media App

## Table of Contents
- [Social Media App](#social-media-app)
  - [Table of Contents](#table-of-contents)
  - [Introduction](#introduction)
  - [Features](#features)
  - [Project Structure](#project-structure)
  - [Installation](#installation)
  - [Configuration](#configuration)
  - [API Endpoints](#api-endpoints)
    - [Users](#users)
    - [Posts](#posts)
    - [Comments](#comments)
    - [Relationships](#relationships)
    - [Notifications](#notifications)
    - [Moderation](#moderation)
  - [Models](#models)
    - [User](#user)
    - [Profile](#profile)
    - [Post](#post)
    - [Like](#like)
    - [Hashtag](#hashtag)
    - [PostHashtag](#posthashtag)
    - [Comment](#comment)
    - [Relationship](#relationship)
    - [Notification](#notification)
    - [Report](#report)
  - [Authentication](#authentication)
  - [Permissions](#permissions)
  - [Notifications](#notifications-1)
  - [Moderation](#moderation-1)
  - [License](#license)

## Introduction

This Social Media App is a Django-based backend application that provides a robust API for a social networking platform. It includes features such as user authentication, post creation and interaction, commenting, user relationships, notifications, and content moderation.

## Features

- User registration and authentication
- User profile management
- Post creation, retrieval, update, and deletion
- Like/unlike functionality for posts
- Commenting system with nested replies
- Hashtag support for posts
- User relationships (follow/unfollow)
- Real-time notifications
- Content moderation with reporting system
- Admin dashboard for moderation

## Project Structure

The project is organized into several Django apps, each responsible for specific functionality:

- `core`: Main project settings and configurations
- `users`: User management and profiles
- `posts`: Post creation, retrieval, and interaction
- `comments`: Commenting system
- `relationships`: User follow/unfollow functionality
- `notifications`: Real-time notification system
- `moderation`: Content reporting and moderation

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/mertcolakoglu/social_media_api.git
   cd social_media_api
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Apply migrations:
   ```
   python manage.py makemigrations
   python manage.py migrate
   ```

5. Create a superuser:
   ```
   python manage.py createsuperuser
   ```

6. Run the development server:
   ```
   python manage.py runserver
   ```

## Configuration

1. Create a `.env` file in the project root and add the following variables:
   ```
   SECRET_KEY=your_secret_key_here
   DEBUG=True
   ```

2. Update `ALLOWED_HOSTS` in `core/settings.py` if deploying to a specific domain.

## API Endpoints

### Users
- `POST /auth/users/`: Register a new user
- `POST /auth/jwt/create/`: Obtain JWT token
- `POST /auth/jwt/refresh/`: Refresh JWT token
- `GET /api/me/`: Retrieve current user's profile
- `PUT /api/me/`: Update current user's profile

### Posts
- `GET /api/posts/`: List all posts
- `POST /api/posts/`: Create a new post
- `GET /api/posts/<int:pk>/`: Retrieve a specific post
- `PUT /api/posts/<int:pk>/`: Update a specific post
- `DELETE /api/posts/<int:pk>/`: Delete a specific post
- `GET /api/my-posts/`: List current user's posts
- `POST /api/likes/toggle/`: Toggle like on a post
- `GET /api/posts-by-hashtag/?hashtag=<hashtag_name>`: List posts with a specific hashtag

### Comments
- `GET /api/posts/<int:post_id>/comments/`: List comments for a post
- `POST /api/posts/<int:post_id>/comments/`: Create a comment on a post
- `GET /api/comments/<int:pk>/`: Retrieve a specific comment
- `PUT /api/comments/<int:pk>/`: Update a specific comment
- `DELETE /api/comments/<int:pk>/`: Delete a specific comment
- `GET /api/comments/<int:comment_id>/replies/`: List replies to a comment
- `POST /api/comments/<int:comment_id>/replies/`: Create a reply to a comment

### Relationships
- `GET /api/relationships/`: List current user's relationships
- `POST /api/relationships/`: Create a new relationship (follow/block)
- `GET /api/relationships/<int:pk>/`: Retrieve a specific relationship
- `PUT /api/relationships/<int:pk>/`: Update a specific relationship
- `DELETE /api/relationships/<int:pk>/`: Delete a specific relationship
- `GET /api/followers/`: List current user's followers
- `GET /api/following/`: List users the current user is following

### Notifications
- `GET /api/notifications/`: List current user's notifications
- `GET /api/notifications/<int:pk>/`: Retrieve a specific notification
- `PUT /api/notifications/<int:pk>/`: Mark a notification as read
- `POST /api/notifications/mark-all-read/`: Mark all notifications as read

### Moderation
- `POST /api/reports/`: Create a new report
- `GET /api/reports/`: List reports (admin only)
- `GET /api/reports/<int:pk>/`: Retrieve a specific report
- `PUT /api/reports/<int:pk>/`: Update report status (admin only)

## Models

### User
- Custom user model extending Django's AbstractUser
- Fields: username, email, password, first_name, last_name, date_joined, is_active, is_staff

### Profile
- OneToOne relationship with User
- Fields: user, bio, profile_picture, location, birth_date, website, privacy_settings

### Post
- Fields: author, content, image, created_at, updated_at, is_public

### Like
- Fields: user, post, created_at

### Hashtag
- Fields: name, created_at

### PostHashtag
- Fields: post, hashtag

### Comment
- Fields: user, post, parent_comment, content, created_at, updated_at

### Relationship
- Fields: from_user, to_user, status, created_at

### Notification
- Fields: user, content, notification_type, related_object, is_read, created_at

### Report
- Fields: reporter, reported_object, reason, description, status, created_at, updated_at

## Authentication

The project uses JWT (JSON Web Tokens) for authentication. To authenticate:

1. Obtain a token by sending a POST request to `/auth/jwt/create/` with your username and password.
2. Include the token in the Authorization header of your requests: `Authorization: JWT <your_token>`.

## Permissions

- `IsAuthenticatedOrReadOnly`: Allows read access to anyone, but requires authentication for write operations.
- `IsAuthorOrReadOnly`: Allows the author of an object to modify or delete it.
- `IsPublicOrAuthor`: Allows access to public posts or to the author of private posts.
- `IsCommentAuthorOrPostAuthorOrReadOnly`: Allows comment authors or post authors to modify comments.
- `IsOwnerOrReadOnly`: Allows the owner of a relationship to modify it.
- `IsAdminOrReporter`: Allows admins or the original reporter to view and update reports.

## Notifications

The app includes a real-time notification system. Notifications are created for:
- Likes on posts
- Comments on posts
- New followers
- Content reports (for admins)
- Report status updates

## Moderation

The moderation system allows users to report inappropriate content. Admins can review and take action on reports through the admin interface or API.

## License

This project is licensed under the MIT License.
