# Dynamic Form Builder with Analytics

This project is a backend implementation of a **Dynamic Form Builder** using Django. It allows an admin to create forms, add questions, view user responses, and analyze form submissions. All superusers are considered admins and can access the admin panel for managing the forms and analytics.

## Features
- **Dynamic Form Creation**: Admins can create forms and add questions of various types.
- **User Responses**: Users can submit responses to the forms.
- **Analytics**: Admins can analyze user responses, including top words and option selections.
- **Admin Panel**: Superusers can manage forms, questions, and responses via Django's admin interface.
- **Swagger UI**: API documentation is available at the root URL (`/`).

---

## Steps to Run the Project

### Prerequisites
- Python (>= 3.8)
- SQLite (default) or any supported database
- `pip` for installing Python dependencies

### Installation
1. **Clone the Repository**  
   ```bash
   git clone git@github.com:aarya-dev003/morpheus-rbc.git
   cd morpheus-rbc

2. **Create a Virtual Environment**

    ```bash
    python -m venv .venv
    source .venv/bin/activate  

3. **Install Dependencies**

    ```bash
    pip install -r requirements.txt
    cd form_builder

4. **Run Migrations**

    ```bash
    python manage.py makemigrations
    python manage.py migrate

5. **Create a Superuser**

    ```bash
    python manage.py createsuperuser

6. **Run the Development Server**
    
    ```bash
    python manage.py runserver

## Authenticate as Admin
1. Access the token endpoint to sign in using the superuser's credentials:
   - Visit: `{{URL}}/auth/token/`
   - Use the superuser's **username** and **password** to obtain an access token.
   
2. This token can be used to access protected API endpoints for creating forms and adding questions.

3. Alternatively, you can use the **admin panel** at `{{URL}}/admin/` to manage forms directly.

---

## Admin Panel Access
- Superusers can access the admin panel at `/admin/`.
- All superusers are considered admins by default.


## API Documentation

- You can explore the API endpoints and make requests using the following Postman documentation:
   - [Postman API Documentation](https://documenter.getpostman.com/view/32664548/2sAYJ9AJJq)

- Additionally The Swagger UI documentation is available at the root URL: '/'.
