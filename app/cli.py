import click
from app.database import UserSeeder, PartSeeder


def register_cli_commands(app):
    """Register CLI commands with the Flask app."""
    
    @app.cli.command()
    def seed():
        """Seed the database with sample data."""
        user_result = UserSeeder.seed_all()
        click.echo(f"✓ Added: {user_result['added']} users")
        click.echo(f"✗ Skipped: {user_result['skipped']} users")

        part_result = PartSeeder.seed_all()
        click.echo(f"✓ Added: {part_result['added']} parts")
        click.echo(f"✗ Skipped: {part_result['skipped']} parts")

        click.echo("✓ Seeding complete!")
    
    @app.cli.command()
    def clearSeed():
        """Clear all users and parts from the database."""
        if click.confirm("Are you sure you want to delete all users and parts?"):
            user_count = UserSeeder.clear_all()
            part_count = PartSeeder.clear_all()
            click.echo(f"✓ Deleted {user_count} users!")
            click.echo(f"✓ Deleted {part_count} parts!")
        else:
            click.echo("✗ Cancelled.")
