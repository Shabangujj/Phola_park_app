"""
JJCORETECH
System Settings Model
"""

from datetime import datetime

from phola_park_app.extensions import db


# =====================================================
# SYSTEM SETTINGS
# =====================================================

class SystemSettings(db.Model):
    __tablename__ = "system_settings"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    # -------------------------
    # General
    # -------------------------

    site_name = db.Column(
        db.String(150),
        default="Phola Park App",
        nullable=False
    )

    company_name = db.Column(
        db.String(150),
        default="JJCORETECH",
        nullable=False
    )

    site_description = db.Column(
        db.Text,
        nullable=True
    )

    # -------------------------
    # Contact
    # -------------------------

    contact_email = db.Column(
        db.String(150)
    )

    contact_phone = db.Column(
        db.String(50)
    )

    address = db.Column(
        db.Text
    )

    # -------------------------
    # Appearance
    # -------------------------

    theme = db.Column(
        db.String(50),
        default="default"
    )

    logo = db.Column(
        db.String(255)
    )

    favicon = db.Column(
        db.String(255)
    )

    # -------------------------
    # Security
    # -------------------------

    allow_registration = db.Column(
        db.Boolean,
        default=True
    )

    maintenance_mode = db.Column(
        db.Boolean,
        default=False
    )

    require_email_verification = db.Column(
        db.Boolean,
        default=False
    )

    password_min_length = db.Column(
        db.Integer,
        default=8
    )

    # -------------------------
    # Notifications
    # -------------------------

    enable_email_notifications = db.Column(
        db.Boolean,
        default=True
    )

    enable_system_notifications = db.Column(
        db.Boolean,
        default=True
    )

    # -------------------------
    # Dates
    # -------------------------

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )

    # -------------------------
    # Helper Methods
    # -------------------------

    def enable_maintenance(self):
        self.maintenance_mode = True

    def disable_maintenance(self):
        self.maintenance_mode = False

    def enable_registration(self):
        self.allow_registration = True

    def disable_registration(self):
        self.allow_registration = False

    def to_dict(self):
        return {
            "site_name": self.site_name,
            "company_name": self.company_name,
            "contact_email": self.contact_email,
            "contact_phone": self.contact_phone,
            "theme": self.theme,
            "allow_registration": self.allow_registration,
            "maintenance_mode": self.maintenance_mode,
            "require_email_verification": self.require_email_verification,
            "password_min_length": self.password_min_length,
            "enable_email_notifications": self.enable_email_notifications,
            "enable_system_notifications": self.enable_system_notifications,
        }

    def __repr__(self):
        return f"<SystemSettings {self.site_name}>"