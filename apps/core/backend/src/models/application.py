import re

from datetime import datetime
from textwrap import shorten

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship

from .base import Base
from .user import User


class Application(Base):
    __tablename__ = "applications"

    WEB = "web"
    MOBILE = "mob"
    DESKTOP = "des"

    name = Column(String(30), nullable=False, unique=True)
    real_name = Column(String(250), nullable=False)
    model = Column(Integer, nullable=False, default=1)
    description = Column(String(250), nullable=False)
    details = Column(String(5000), nullable=True)
    active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime(timezone=True), nullable=False, default=datetime.now())
    created_by = Column(Integer, ForeignKey(User.id))
    updated_at = Column(DateTime(timezone=True), nullable=False, default=datetime.now())
    updated_by = Column(Integer, ForeignKey(User.id))
    # relations
    users = relationship("ApplicationUser", lazy="select", back_populates="application")
    enviroments = relationship("ApplicationEnviroment", lazy="select", back_populates="application")
    features = relationship("ApplicationFeature", lazy="select", back_populates="application")

    def generate_name(self):
        name = self.real_name.lower().replace(" ", "_")
        name = re.sub(r"[^a-zA-Z0-9]", "", name)
        name = shorten(name, width=30, placeholder="_")
        self.name = name

    def add_user(self, user: User):
        applicationUser = ApplicationUser(application_id=self.id, user_id=user.id)
        self.users.append(applicationUser)

    @staticmethod
    def get_fields_can_be_updated():
        return ("real_name", "model", "description", "details")


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
    created_by = Column(Integer, ForeignKey(User.id))
    updated_at = Column(DateTime(timezone=True), nullable=False, default=datetime.now())
    updated_by = Column(Integer, ForeignKey(User.id))
    # relations
    application = relationship("Application", lazy="select", back_populates="enviroments")


class ApplicationFeature(Base):
    __tablename__ = "application_features"

    application_id = Column(Integer, ForeignKey(Application.id))
    enviroment_id = Column(Integer, ForeignKey(ApplicationEnviroment.id))
    name = Column(String(250), nullable=False)
    enable = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime(timezone=True), nullable=False, default=datetime.now())
    created_by = Column(Integer, ForeignKey(User.id))
    updated_at = Column(DateTime(timezone=True), nullable=False, default=datetime.now())
    updated_by = Column(Integer, ForeignKey(User.id))
    # relations
    application = relationship("Application", lazy="select", back_populates="features")




