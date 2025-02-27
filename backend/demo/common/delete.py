import os
import django
django.setup()

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fridgeserver.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        print(exc)
        return

    from demo.models import Food

    # Query to get the record where name='xx'
    Food.objects.all().delete()



if __name__ == '__main__':
    main()


