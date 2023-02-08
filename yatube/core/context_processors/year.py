from datetime import datetime


def year(request):
    """Добавляет переменную с текущим годом."""
    year_now = datetime.now()
    return {
        'year': year_now.year,
    }
