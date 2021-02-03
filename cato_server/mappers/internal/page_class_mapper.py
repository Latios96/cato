from typing import Dict

from cato_server.mappers.abstract_class_mapper import AbstractClassMapper
from cato_server.mappers.mapper_registry import MapperRegistry
from cato_server.storage.abstract.page import Page


class PageClassMapper(AbstractClassMapper[Page]):
    def __init__(self, mapper_registry: MapperRegistry):
        self._mapper_registry = mapper_registry

    def map_from_dict(self, json_data: Dict) -> Page:
        return Page(
            page_number=json_data["page_number"],
            page_size=json_data["page_size"],
            total_pages=json_data["total_pages"],
            entities=self.map_many_from_dict(json_data["entities"]),
        )

    def map_to_dict(self, page: Page) -> Dict:
        return {
            "page_number": page.page_number,
            "page_size": page.page_size,
            "total_pages": page.total_pages,
            "entities": self._map_entities(page),
        }

    def _map_entities(self, page: Page):
        if not page.entities:
            return []
        return self._mapper_registry.class_mapper_for_cls(
            page.entities[0].__class__
        ).map_many_to_dict(page.entities)
