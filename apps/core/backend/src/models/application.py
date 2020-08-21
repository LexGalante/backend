import re

from datetime import datetime
from textwrap import shorten

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship

from .base import Base
from .user import User
from .environment import Environment


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
    features = relationship("ApplicationFeature", lazy="select", back_populates="application")

    def generate_name(self):
        name = self.real_name.lower().replace(" ", "_")
        name = re.sub(r"[^a-zA-Z0-9]", "", name)
        name = shorten(name, width=30, placeholder="_")
        self.name = name

    def add_user(self, user_id: int):
        user = ApplicationUser(application_id=self.id, user_id=user_id)
        self.users.append(user)

    def add_feature(self, environment_id: int, name: str, enable: bool, user: User):
        application_feature = ApplicationFeature()
        application_feature.application_id = self.id
        application_feature.environment_id = environment_id
        application_feature.name = name
        application_feature.enable = enable
        application_feature.created_at = datetime.now()
        application_feature.created_by = user.id
        application_feature.updated_at = datetime.now()
        application_feature.updated_by = user.id
        self.features.append(application_feature)

    @staticmethod
    def get_fields_can_be_updated():
        return ("real_name", "model", "description", "details")


class ApplicationUser(Base):
    __tablename__ = "application_users"

    application_id = Column(Integer, ForeignKey(Application.id), primary_key=True)
    user_id = Column(Integer, ForeignKey(User.id), primary_key=True)
    # relations
    application = relationship("Application", lazy="select", back_populates="users")
    user = relationship("User", lazy="select")


class ApplicationFeature(Base):
    __tablename__ = "application_features"

    application_id = Column(Integer, ForeignKey(Application.id))
    environment_id = Column(Integer, ForeignKey(Environment.id))
    name = Column(String(250), nullable=False)
    enable = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime(timezone=True), nullable=False, default=datetime.now())
    created_by = Column(Integer, ForeignKey(User.id))
    updated_at = Column(DateTime(timezone=True), nullable=False, default=datetime.now())
    updated_by = Column(Integer, ForeignKey(User.id))
    # relations
    application = relationship("Application", lazy="select", back_populates="features")
    environment = relationship("Environment", lazy="select")
