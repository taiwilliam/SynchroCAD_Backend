import click
from app.database import UserSeeder


def register_cli_commands(app):
    """Register CLI commands with the Flask app."""
    
    @app.cli.command()
    def seed():
        """Seed the database with sample data."""
        result = UserSeeder.seed_all()
        click.echo(f"✓ Added: {result['added']} users")
        click.echo(f"✗ Skipped: {result['skipped']} users")
        click.echo("✓ Seeding complete!")
    
    @app.cli.command()
    def clear_users():
        """Clear all users from the database."""
        if click.confirm("Are you sure you want to delete all users?"):
            count = UserSeeder.clear_all()
            click.echo(f"✓ Deleted {count} users!")
        else:
            click.echo("✗ Cancelled.")
