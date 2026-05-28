"""Base service class for business logic."""


class BaseService:
    """Base service class for common CRUD operations."""
    
    def __init__(self, model, db):
        """Initialize service with model and database session."""
        self.model = model
        self.db = db
    
    def create(self, **kwargs):
        """Create a new record."""
        obj = self.model(**kwargs)
        self.db.session.add(obj)
        self.db.session.commit()
        return obj
    
    def get_by_id(self, id):
        """Get record by ID."""
        return self.model.query.get(id)
    
    def get_all(self):
        """Get all records."""
        return self.model.query.all()
    
    def update(self, id, **kwargs):
        """Update a record."""
        obj = self.get_by_id(id)
        if obj:
            for key, value in kwargs.items():
                setattr(obj, key, value)
            self.db.session.commit()
        return obj
    
    def delete(self, id):
        """Delete a record."""
        obj = self.get_by_id(id)
        if obj:
            self.db.session.delete(obj)
            self.db.session.commit()
        return True
