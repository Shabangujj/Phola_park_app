def log_action(action, description, user_id):
    from phola_park_app import db
    from phola_park_app.model import AuditLog

    log = AuditLog(
        action=action,
        description=description,
        user_id=user_id
    )

    db.session.add(log)
    db.session.commit()