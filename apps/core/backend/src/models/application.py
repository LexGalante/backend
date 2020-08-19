from datetime import datetime

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship

from .base import Base


class Application(Base):
    __tablename__ = "applications"

    name = Column(String(30), nullable=False, unique=True)
    real_name = Column(String(250), nullable=False)
    model = Column(Integer, nullable=False, default=1)
    description = Column(String(250), nullable=False)
    details = Column(String(5000), nullable=True)
    active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime(timezone=True), nullable=False, default=datetime.now())
    created_by = Column(Integer, ForeignKey("user.id"))
    updated_at = Column(DateTime(timezone=True), nullable=False, default=datetime.now())
    updated_by = Column(Integer, ForeignKey("user.id"))
    # relations
    users = relationship("ApplicationUser", lazy="select", back_populates="application")
    enviroments = relationship("ApplicationEnviroment", lazy="select", back_populates="application")
    features = relationship("ApplicationFeature", lazy="select", back_populates="application")


class ApplicationUser(Base):
    __tablename__ = "application_users"

    application_id = Column(Integer, ForeignKey(Application.id), primary_key=True)
    user_id = Column(Integer, nullable=False, primary_key=True)
    # relations
    application = relationship("Application", lazy="select", back_populates="users")


class ApplicationEnviroment(Base):
    __tablename__ = "application_environments"

    application_id = Column(Integer, ForeignKey(Application.id))
    name = Column(String(30), nullable=False)
    real_name = Column(String(250), nullable=False)
    description = Column(String(250), nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False, default=datetime.now())
    created_by = Column(Integer, ForeignKey("user.id"))
    updated_at = Column(DateTime(timezone=True), nullable=False, default=datetime.now())
    updated_by = Column(Integer, ForeignKey("user.id"))
    # relations
    application = relationship("Application", lazy="select", back_populates="enviroments")


class ApplicationFeature(Base):
    __tablename__ = "application_features"

    application_id = Column(Integer, ForeignKey(Application.id))
    enviroment_id = Column(Integer, ForeignKey(ApplicationEnviroment.id))
    name = Column(String(250), nullable=False)
    enable = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime(timezone=True), nullable=False, default=datetime.now())
    created_by = Column(Integer, ForeignKey("user.id"))
    updated_at = Column(DateTime(timezone=True), nullable=False, default=datetime.now())
    updated_by = Column(Integer, ForeignKey("user.id"))
    # relations
    application = relationship("Application", lazy="select", back_populates="features")




