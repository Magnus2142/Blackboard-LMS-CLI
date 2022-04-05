from __future__ import annotations
from typing import Any
from abc import ABC, abstractmethod

DOMAIN = 'https://ntnu.blackboard.com'
API_BASE = '/learn/api/public'


class Builder(ABC):

    @property
    @abstractmethod
    def product(self) -> None:
        pass

    """
    Returns the base URL which includes the domain and first part of all the endpoints: domain/learn/api/public/vX,
    where X is the version from 1 to 3.
    """

    @abstractmethod
    def base_v1(self) -> Builder:
        pass

    @abstractmethod
    def base_v2(self) -> Builder:
        pass

    @abstractmethod
    def base_v3(self) -> Builder:
        pass

    @abstractmethod
    def add_courses(self) -> Builder:
        pass

    @abstractmethod
    def add_users(self) -> Builder:
        pass

    @abstractmethod
    def add_announcements(self) -> Builder:
        pass

    @abstractmethod
    def add_contents(self) -> Builder:
        pass

    @abstractmethod
    def add_terms(self) -> Builder:
        pass

    @abstractmethod
    def add_children(self) -> Builder:
        pass

    @abstractmethod
    def add_attachments(self) -> Builder:
        pass

    @abstractmethod
    def add_uploads(self) -> Builder:
        pass

    @abstractmethod
    def add_create_assignment(self) -> Builder:
        pass

    @abstractmethod
    def add_id(self, id: str, id_type: str = None) -> Builder:
        pass

    @abstractmethod
    def add_download(self) -> Builder:
        pass

    @abstractmethod
    def add_gradebook(self) -> Builder:
        pass

    @abstractmethod
    def add_columns(self) -> Builder:
        pass


class URL_builder(Builder):

    def __init__(self) -> None:
        self.reset()

    def reset(self) -> None:
        self._product = URL()

    @property
    def product(self) -> URL:
        product = self._product
        self.reset()
        return product

    def base_v1(self) -> URL_builder:
        self._product.add(f'{DOMAIN}{API_BASE}/v1')
        return self

    def base_v2(self) -> URL_builder:
        self._product.add(f'{DOMAIN}{API_BASE}/v2')
        return self

    def base_v3(self) -> URL_builder:
        self._product.add(f'{DOMAIN}{API_BASE}/v3')
        return self

    def add_courses(self) -> URL_builder:
        self._product.add('/courses')
        return self

    def add_users(self) -> URL_builder:
        self._product.add('/users')
        return self

    def add_announcements(self) -> URL_builder:
        self._product.add('/announcements')
        return self

    def add_contents(self) -> URL_builder:
        self._product.add('/contents')
        return self

    def add_terms(self) -> URL_builder:
        self._product.add('/terms')
        return self

    def add_children(self) -> Builder:
        self._product.add('/children')
        return self

    def add_attachments(self) -> Builder:
        self._product.add('/attachments')
        return self

    def add_uploads(self) -> Builder:
        self._product.add('/uploads')
        return self

    def add_create_assignment(self) -> Builder:
        self._product.add('/createAssignment')
        return self

    def add_download(self) -> Builder:
        self._product.add('/download')
        return self

    def add_id(self, id: str, id_type: str = None) -> URL_builder:
        if id_type:
            self._product.add(f'/{id_type}:{id}')
        else:
            self._product.add(f'/{id}')
        return self

    def add_gradebook(self) -> Builder:
        self._product.add('/gradebook')
        return self

    def add_columns(self) -> Builder:
        self._product.add('/columns')
        return self

    def create(self) -> str:
        url = self._product.get_url()
        self._product = URL()
        return url


class URL():

    def __init__(self) -> None:
        self.URL = ''

    def add(self, url_part: str) -> None:
        self.URL += url_part

    def get_url(self) -> None:
        return self.URL
