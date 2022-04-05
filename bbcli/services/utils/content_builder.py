from __future__ import annotations
from datetime import date, datetime
from typing import Any, Dict
from abc import ABC, abstractmethod

from bbcli.entities.content_builder_entitites import FileContent, FileOptions, GradingOptions, StandardOptions, WeblinkOptions


class Builder(ABC):

    @property
    @abstractmethod
    def product(self) -> None:
        pass

    @abstractmethod
    def add_parent_id(self, title: str) -> Builder:
        pass

    @abstractmethod
    def add_title(self, title: str) -> Builder:
        pass

    @abstractmethod
    def add_body(self, body: str) -> Builder:
        pass

    @abstractmethod
    def add_standard_options(self, standard_options: StandardOptions) -> Builder:
        pass

    # Alignment option is available in creation in the web interface, but not in the actual content objects that is created
    @abstractmethod
    def add_file_options(self, file_options: FileOptions) -> Builder:
        pass

    @abstractmethod
    def add_weblink_options(self, web_link_options: WeblinkOptions) -> Builder:
        pass

    @abstractmethod
    def add_grading_options(self, grading_options: GradingOptions) -> Builder:
        pass

    @abstractmethod
    def add_content_handler_document(self) -> Builder:
        pass

    @abstractmethod
    def add_content_handler_file(self, file_content: FileContent) -> Builder:
        pass

    @abstractmethod
    def add_content_handler_externallink(self, url: str) -> Builder:
        pass

    @abstractmethod
    def add_content_handler_folder(self, is_bb_page: bool) -> Builder:
        pass

    # Possible target types:
    # Unset
    # CourseAssessment
    # CourseTOC
    # Forum
    # Tool
    # CollabSession (deprecated since 3000.1.0)
    # Group
    # BlogJournal
    # StaffInfo
    # ModulePage

    @abstractmethod
    def add_content_handler_courselink(self, target_id: str, target_type: str = 'Unset') -> Builder:
        pass


class ContentBuilder(Builder):

    def __init__(self) -> None:
        self.reset()

    def reset(self) -> None:
        self._product = Content()

    @property
    def product(self) -> Content:
        product = self._product
        self.reset()
        return product

    def add_parent_id(self, parent_id: str) -> Builder:
        self._product.add({
            'parentId': parent_id
        })
        return self

    def add_title(self, title: str) -> Builder:
        self._product.add({
            'title': title
        })
        return self

    def add_name(self, name: str) -> Builder:
        self._product.add({
            'name': name
        })
        return self

    def add_body(self, body: str) -> Builder:
        self._product.add({
            'body': body
        })
        return self

    def add_standard_options(self, standard_options: StandardOptions) -> Builder:
        start_date_str = datetime.strftime(standard_options.date_interval.start_date,
                                           '%Y-%m-%dT%H:%m:%S.%fZ') if standard_options.date_interval.start_date else None
        end_date_str = datetime.strftime(standard_options.date_interval.end_date,
                                         '%Y-%m-%dT%H:%m:%S.%fZ') if standard_options.date_interval.end_date else None
        self._product.add({
            'availability': {
                'available': 'No' if standard_options.hide_content else 'Yes',
                'allowGuests': True,
                'allowObservers': True,
                'adaptiveRelease': {
                    'start': start_date_str,
                    'end': end_date_str
                }
            }
        })
        if standard_options.reviewable:
            self._product.add({
                'reviewable': standard_options.reviewable,
            })
        return self

    # Missing an extra option, but don't know what it is called
    def add_file_options(self, file_options: FileOptions) -> Builder:
        self._product.add({
            'launchInNewWindow': file_options.launch_in_new_window
        })
        return self

    def add_weblink_options(self, web_link_options: WeblinkOptions) -> Builder:
        self._product.add({
            'launchInNewWindow': web_link_options.launch_in_new_window
        })
        return self

    def add_grading_options(self, grading_options: GradingOptions) -> Builder:
        due_date_str = datetime.strftime(
            grading_options.due, '%Y-%m-%dT%H:%m:%S.%fZ') if grading_options.due else None
        self._product.add({
            'grading': {
                'due': due_date_str,
                'attemptsAllowed': grading_options.attempts_allowed,
                'isUnlimitedAttemptsAllowed': grading_options.is_unlimited_attemps_allowed
            },
            'score': {
                'possible': grading_options.score_possible
            }
        })
        return self

    def add_content_handler_document(self) -> Builder:
        self._product.add({
            'contentHandler': {
                'id': 'resource/x-bb-document'
            }
        })
        return self

    def add_content_handler_file(self, file_content: FileContent) -> Builder:
        self._product.add({
            'contentHandler': {
                'id': 'resource/x-bb-file',
                'file': {
                    'uploadId': file_content.upload_id,
                    'fileName': file_content.file_name,
                    'mimeType': file_content.mime_type,
                    'duplicateFileHandling': file_content.duplicate_file_handling
                }

            }
        })
        return self

    def add_content_handler_externallink(self, url: str) -> Builder:
        self._product.add({
            'contentHandler': {
                'id': 'resource/x-bb-externallink',
                'url': url
            }
        })
        return self

    def add_content_handler_folder(self, is_bb_page: bool) -> Builder:
        self._product.add({
            'contentHandler': {
                'id': 'resource/x-bb-folder',
                'isBbPage': is_bb_page
            }
        })
        return self

    def add_content_handler_courselink(self, target_id: str, target_type: str = 'Unset') -> Builder:
        self._product.add({
            'contentHandler': {
                'id': 'resource/x-bb-courselink',
                'targetId': target_id,
                'targetType': target_type
            }
        })
        return self

    def create(self) -> Dict:
        content = self._product.get_content()
        self._product = Content()
        return content


class Content():

    def __init__(self) -> None:
        self.content = {}

    def add(self, content_part: str) -> None:
        self.content.update(content_part)

    def get_content(self) -> None:
        return self.content
