from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship

from .base import Base


class ApplicationBase(Base):
    created_at = Column(DateTime(timezone=True), nullable=False)
    created_by = Column(Integer, ForeignKey("users.id"))
    updated_at = Column(DateTime(timezone=True), nullable=False)
    updated_by = Column(Integer, ForeignKey("users.id"))


class Application(ApplicationBase):
    __tablename__ = "applications"

    name = Column(String(30), nullable=False, unique=True)
    real_name = Column(String(250), nullable=False)
    model = Column(Integer(min=1, max=3), nullable=False, default=1)
    description = Column(String(250), nullable=False)
    details = Column(String(5000), nullable=True)
    active = Column(Boolean, nullable=False, default=True)
    enviroments = relationship("ApplicationEnviroment", lazy="select", back_populates="application")
    features = relationship("ApplicationFeature", lazy="select", back_populates="application")


class ApplicationEnviroment(ApplicationBase):
    __tablename__ = "application_environments"

    application_id = Column(Integer, ForeignKey("applications.id"))
    name = Column(String(30), nullable=False)
    real_name = Column(String(250), nullable=False)
    description = Column(String(250), nullable=False)
    application = relationship("Application", lazy="select", back_populates="enviroments")
    created_at = Column(DateTime(timezone=True), nullable=False)
    created_by = Column(Integer, ForeignKey("users.id"))
    updated_at = Column(DateTime(timezone=True), nullable=False)
    updated_by = Column(Integer, ForeignKey("users.id"))


class ApplicationFeature(ApplicationBase):
    __tablename__ = "application_features"

    application_id = Column(Integer, ForeignKey("applications.id"))
    enviroment_id = Column(Integer, ForeignKey("application_enviroments.id"))
    name = Column(String(250), nullable=False)
    enable = Column(Boolean, nullable=False, default=False)
    application = relationship("Application", lazy="select", back_populates="features")
    created_at = Column(DateTime(timezone=True), nullable=False)
    created_by = Column(Integer, ForeignKey("users.id"))
    updated_at = Column(DateTime(timezone=True), nullable=False)
    updated_by = Column(Integer, ForeignKey("users.id"))
