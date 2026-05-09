from datetime import datetime
from app import db
from app.models import AuditLog

def log_action(user_id, action, description):
    log = AuditLog(
        user_id=user_id,
        action=action,
        description=description,
        timestamp=datetime.utcnow()
    )
    db.session.add(log)
    db.session.commit()