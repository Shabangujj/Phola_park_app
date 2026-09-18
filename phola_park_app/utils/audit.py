from datetime import datetime

from phola_park_app.extensions import db
from phola_park_app.models import AuditLog


def log_action(
    user_id,
    action,
    module,
    description,
    ip_address=None,
    user_agent=None
):
    log = AuditLog(
        user_id=user_id,
        action=action,
        module=module,
        description=description,
        ip_address=ip_address,
        user_agent=user_agent,
        created_at=datetime.utcnow()
    )

    db.session.add(log)
    db.session.commit()

    return log
