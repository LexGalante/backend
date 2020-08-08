from typing import List

from ..resources.list_helpers import prevent_duplicate_items
from ..resources.text_helpers import replace_all
from .model import Model


class Application(Model):
    real_name: str
    name: str
    type: str
    description: str
    detail: str
    roled_by: str = "default"
    owners: List[str] = []
    maintainers: List[str] = []
    tags: List[str] = []
    features: List[str] = []
    enable_features: List[str] = []

    def set_name(self):
        charsToRemove = [" ", "@", "#", "!", "&", "*", "$", ",", "+", "=", "-"]
        self.name = replace_all(self.name, "_", charsToRemove)

    def add_owner(self, owner: str | List[str]):
        self.owner = prevent_duplicate_items(owner)

    def add_maintaner(self, maintaner: str | List[str]):
        self.maintaners = prevent_duplicate_items(maintaner)

    def add_tag(self, tag: str | List[str]):
        self.tags = prevent_duplicate_items(tag)

    def add_feature(self, feature: str | List[str]):
        self.features = prevent_duplicate_items(feature)

    def add_enable_feature(self, enable_feature: str | List[str]):
        self.enable_features = prevent_duplicate_items(enable_feature)
