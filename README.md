# Ranker API

Ranker is a Django API that allows users to create challenges to gain XP. XP helps users achieve levels, and at specific levels, they gain titles like Beginner, Challenger (customizable) etc. Daily ranks are calculated based on total XP.

## Features
Here are some core features:
- **Authentication:** All nesssary authentication and authorization features (including 2FA and social login) provided by [All-Auth](https://docs.allauth.org/en/latest/).
- **Challenge Creation:** Users can create challenges with specific goals, difficulty and due date (optional).
- **Challenge Steps:** Users can break challenge into several steps to complete it faster.
- **Challenge and Step Reordering:** Users can reorder challenges and its steps based on their personal preference and priority.
- **Difficulty:** Admin and staffs can create custom difficulty levels with associated colors and XP.
- **XP Tracking:** Users earn XP for completing challenges.
- **Leveling Up:** Users achieve higher levels based on their total XP.
- **Title Achievement:** Users gain titles from Beginner to Titan at specific levels (customizable by admin and staffs).
- **Ranking:** Daily ranks are calculated based on total XP.

### AI Features
- **Challenge Steps Generation:** Users can generate steps for completing a challenge.

### Comming Soon
- **QR Code Login:** Users can login instantly by scaning QR code securely
- **Notifications:** Users receive notifications for weekly progress, level title achievements, and more.
- **Repeated Challenges:** Users can create repeated challenges (e.g. daily, weekly, monthly).

## Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/HasanAshab/ranker-api.git
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run migrations:**
   ```bash
   python manage.py migrate
   ```

4. **Create a superuser:**
   ```bash
   python manage.py createsuperuser
   ```

5. **Run the development server:**
   ```bash
   python manage.py runserver
   ```

6. **Access the API:**
   - Admin Panel: `http://localhost:8000/admin/`
   - API Root: `http://localhost:8000/api/`
   - API Documentation: `http://localhost:8000/api/docs/ui/swagger/`

7. **Test the API:**
   ```bash
   python manage.py test
   ```

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your changes.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
