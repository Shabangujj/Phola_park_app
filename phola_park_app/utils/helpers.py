"""Utility helper functions."""


def format_datetime(dt, format='%Y-%m-%d %H:%M:%S'):
    """Format datetime object to string."""
    if dt:
        return dt.strftime(format)
    return None


def get_pagination_info(page, per_page, total):
    """Calculate pagination information."""
    total_pages = (total + per_page - 1) // per_page
    return {
        'current_page': page,
        'per_page': per_page,
        'total': total,
        'total_pages': total_pages,
        'has_prev': page > 1,
        'has_next': page < total_pages
    }


def truncate_string(text, length=100):
    """Truncate string to specified length."""
    if len(text) > length:
        return text[:length] + '...'
    return text


def get_time_ago(dt):
    """Get human-readable time difference."""
    from datetime import datetime
    if not dt:
        return None
    
    diff = datetime.utcnow() - dt
    seconds = diff.total_seconds()
    
    if seconds < 60:
        return 'just now'
    elif seconds < 3600:
        return f'{int(seconds/60)} minutes ago'
    elif seconds < 86400:
        return f'{int(seconds/3600)} hours ago'
    else:
        return f'{int(seconds/86400)} days ago'
