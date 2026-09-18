"""
JJCORETECH
Committee Model
"""

from datetime import datetime

from phola_park_app.extensions import db


# ============================================================
# COMMITTEE MEMBERS
# ============================================================

committee_members = db.Table(
    "committee_members",

    db.Column(
        "committee_id",
        db.Integer,
        db.ForeignKey("committees.id"),
        primary_key=True
    ),

    db.Column(
        "user_id",
        db.Integer,
        db.ForeignKey("users.id"),
        primary_key=True
    ),

    db.Column(
        "joined_at",
        db.DateTime,
        default=datetime.utcnow,
        nullable=False
    )
)


# ============================================================
# COMMITTEE
# ============================================================

class Committee(db.Model):

    __tablename__ = "committees"

    # --------------------------------------------------------
    # ID
    # --------------------------------------------------------

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    # --------------------------------------------------------
    # INFORMATION
    # --------------------------------------------------------

    name = db.Column(
        db.String(150),
        nullable=False
    )

    description = db.Column(
        db.Text,
        nullable=True
    )

    # --------------------------------------------------------
    # PORTFOLIO
    # --------------------------------------------------------

    portfolio = db.Column(
        db.String(100),
        nullable=False,
        index=True
    )

    # --------------------------------------------------------
    # CREATED BY SUPERVISOR
    # --------------------------------------------------------

    created_by = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    # --------------------------------------------------------
    # CREATED DATE
    # --------------------------------------------------------

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    # --------------------------------------------------------
    # MEMBERS
    # --------------------------------------------------------

    members = db.relationship(
        "User",
        secondary=committee_members,
        backref=db.backref(
            "committees",
            lazy="dynamic"
        ),
        lazy="dynamic"
    )

    # --------------------------------------------------------
    # CREATOR
    # --------------------------------------------------------

    creator = db.relationship(
        "User",
        foreign_keys=[created_by],
        back_populates="committees_created"
    )

    # --------------------------------------------------------
    # MEMBER COUNT
    # --------------------------------------------------------

    @property
    def member_count(self):

        return self.members.count()

    # --------------------------------------------------------
    # MINIMUM MEMBER CHECK
    # --------------------------------------------------------

    @property
    def has_minimum_members(self):

        return self.member_count >= 10

    # --------------------------------------------------------
    # REPRESENTATION
    # --------------------------------------------------------

    def __repr__(self):

        return (
            f"<Committee "
            f"id={self.id} "
            f"name='{self.name}' "
            f"portfolio='{self.portfolio}'>"
        )