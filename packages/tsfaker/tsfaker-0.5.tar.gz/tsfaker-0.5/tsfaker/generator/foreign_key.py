import os
from collections import defaultdict
from typing import List, Union

import numpy as np
from tableschema import Table, Schema

from tsfaker.exceptions import ResourceMissing


class ForeignKeyCatalog:
    def __init__(self, resource_name_to_path_or_schema=None, low_memory=False, limit_fk=False):
        self.resource_name_to_path_or_schema = resource_name_to_path_or_schema or dict()
        self.catalog_remaining_uses = self.set_catalog_remaining_uses()
        self.catalog = dict()
        self.low_memory = low_memory
        self.limit_fk = limit_fk or 10 ** 10

    def set_catalog_remaining_uses(self) -> dict:
        catalog_remaining_uses = defaultdict(int)
        for resource_name, schema in self.resource_name_to_path_or_schema.items():
            if not isinstance(schema, Schema):
                continue
            for foreign_key in schema.foreign_keys:
                resource_key = self._get_resource_key(resource_name=foreign_key['reference']['resource'],
                                                      resource_fields=foreign_key['reference']['fields'])
                catalog_remaining_uses[resource_key] += 1
        return catalog_remaining_uses

    def get_foreign_key_values(self, resource_name, resource_fields) -> np.ndarray:

        resource_path = self.resource_name_to_path_or_schema[resource_name]
        if not os.path.exists(resource_path):
            raise ResourceMissing("Resource csv file is missing '{}'. This should not happen. "
                                  "This file either existed when tsfaker was started, "
                                  "or it should have been generated before.".format(resource_path))

        resource_key = self._get_resource_key(resource_fields, resource_name)
        self.catalog_remaining_uses[resource_key] -= 1
        if resource_path in self.catalog:
            if self.catalog_remaining_uses == 0:
                return self.catalog.pop(resource_key)
            return self.catalog[resource_key]

        table = Table(resource_path)
        foreign_key_values = []
        for i, keyed_row in enumerate(table.iter(keyed=True)):
            if i > self.limit_fk:
                break
            foreign_key_values.append([keyed_row[key] for key in resource_fields])

        foreign_key_values = np.array(foreign_key_values)

        if self.catalog_remaining_uses and not self.low_memory:
            self.catalog[resource_key] = foreign_key_values

        return foreign_key_values

    @staticmethod
    def _get_resource_key(resource_fields, resource_name):
        return resource_name + '__' + '+'.join(resource_fields)


class ForeignKeyGenerator:
    @staticmethod
    def to_list(str_or_list: Union[str, List[str]]) -> List[str]:
        return (str_or_list,) if isinstance(str_or_list, str) else str_or_list

    def __init__(self, nrows: int,
                 fields: Union[str, List[str]],
                 resource_name: str,
                 resource_fields: Union[str, List[str]],
                 foreign_key_catalog: ForeignKeyCatalog = None
                 ):
        self.nrows = nrows
        self.fields = self.to_list(fields)

        self.resource_fields = self.to_list(resource_fields)

        self.foreign_key_catalog = foreign_key_catalog or ForeignKeyCatalog()
        self.foreign_key_values = self.foreign_key_catalog.get_foreign_key_values(resource_name, self.resource_fields)
        self.array_2d = self.random_choice_2d(self.foreign_key_values, self.nrows)

    @staticmethod
    def random_choice_2d(array: np.ndarray, size: int) -> np.ndarray:
        random_indices = np.random.randint(array.shape[0], size=size)
        return array[random_indices, :]

    def get_column(self, field) -> np.ndarray:
        field_index = self.fields.index(field)
        return self.array_2d[:, field_index]
