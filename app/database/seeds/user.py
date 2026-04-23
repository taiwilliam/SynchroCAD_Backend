"""Database seed logic for users."""
from app.repositories import UserRepository


class UserSeeder:
    """Handle user seed operations."""

    SAMPLE_USERS = [
        {
            "name": "Alice Chen",
            "email": "alice@example.com",
            "password": "hashed_password_123"
        },
        {
            "name": "Bob Wang",
            "email": "bob@example.com",
            "password": "hashed_password_456"
        },
        {
            "name": "Carol Liu",
            "email": "carol@example.com",
            "password": "hashed_password_789"
        },
        {
            "name": "David Wu",
            "email": "david@example.com",
            "password": "hashed_password_012"
        },
        {
            "name": "Eve Huang",
            "email": "eve@example.com",
            "password": "hashed_password_345"
        }
    ]

    @staticmethod
    def seed_all():
        """Seed all sample data and return result."""
        added_count = 0
        skipped_count = 0

        for user_data in UserSeeder.SAMPLE_USERS:
            existing = UserRepository.get_by_email(user_data["email"])
            if not existing:
                UserRepository.create(**user_data)
                added_count += 1
            else:
                skipped_count += 1

        return {"added": added_count, "skipped": skipped_count}

    @staticmethod
    def clear_all():
        """Clear all users and return count."""
        count = UserRepository.count()
        users = UserRepository.list()
        for user in users:
            UserRepository.delete(user.id)
        return count
