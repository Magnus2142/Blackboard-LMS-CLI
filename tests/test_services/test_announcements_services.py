import json
from re import M
from typing import List
from click import Abort, BadParameter
import requests

import pytest

from unittest.mock import Mock, patch
from bbcli.entities.content_builder_entitites import DateInterval

from bbcli.services.announcements_services import create_announcement, delete_announcement, list_announcement, list_announcements, list_course_announcements, update_announcement
from bbcli.utils.utils import format_date


TEST_ANNOUNCEMENT = {"id":"_388961_1","title":"TEST annonucement","body":"This is a test announcement","creator":"_140040_1","draft":False,"availability":{"duration":{"type":"Restricted","start":"2022-04-12T08:06:33.422Z","end":None}},"created":"2022-04-12T08:06:33.423Z","modified":"2022-04-12T08:06:33.452Z","position":2}
UPDATED_TEST_ANNOUNCEMENT = {"id":"_388961_1","title":"TEST TITLE","body":"TEST BODY","creator":"_140040_1","draft":False,"availability":{"duration":{"type":"Restricted","start":"2022-04-12T08:06:33.422Z","end":None}},"created":"2022-04-12T08:06:33.423Z","modified":"2022-04-12T08:06:33.452Z","position":2}


TEST_COURSE_ANNOUNCEMENTS_LIST = [{'id': '_389054_1', 'title': 'Test announcement', 'body': 'This is a test announcement', 'creator': '_140040_1', 'draft': False, 'availability': {'duration': {'type': 'Restricted', 'start': '2022-04-15T22:04:00.000Z', 'end': None}}, 'created': '2022-04-15T13:50:15.623Z', 'modified': '2022-04-15T14:38:43.049Z', 'position': 2}, {'id': '_389055_1', 'title': 'Test announcement', 'creator': '_140040_1', 'draft': False, 'availability': {'duration': {'type': 'Restricted', 'start': '2022-04-15T22:04:00.000Z', 'end': None}}, 'created': '2022-04-15T13:55:57.898Z', 'modified': '2022-04-15T13:55:57.926Z', 'position': 1}, {'id': '_389026_1', 'title': 'Testing announcement', 'body': 'Here is a new announcement. Here is a \n<a href="https://ntnu.no">link</a>.', 'creator': '_36000_1', 'draft': False, 'availability': {'duration': {'type': 'Restricted', 'start': '2022-04-13T16:33:01.758Z', 'end': None}}, 'created': '2022-04-13T16:33:01.759Z', 'modified': '2022-04-13T16:33:01.811Z', 'position': 3}]
TEST_COURSES_LIST = [{'id': '_33050_1', 'name': 'Donn Alexander Morrison testrom'}, {'id': '_32909_1', 'name': 'Sammensl??tt - Ingeni??rfaglig systemtenkning INGA2300 INGG2300 INGT2300 (2022 V??R)'}, {'id': '_31606_1', 'name': 'INGT2300 Ingeni??rfaglig systemtenkning (2022 V??R)'}, {'id': '_32736_1', 'name': 'Sammensl??tt - Matematiske metoder 3 for dataingeni??rer IMAX2150 (2021 H??ST)'}, {'id': '_28936_1', 'name': 'IMAT2150 Matematiske metoder 3 for dataingeni??rer (2021 H??ST)'}, {'id': '_27251_1', 'name': 'IDATT2900 Bacheloroppgave  (start 2021 H??ST)'}]

TEST_CREATED_ANNOUNCEMENT = {"id":"_389054_1","title":"Test announcement","body":"This is a test announcement","creator":"_140040_1","draft":False,"availability":{"duration":{"type":"Restricted","start":"2022-04-15T22:04:00.000Z","end":None}},"created":"2022-04-15T13:50:15.623Z","modified":"2022-04-15T13:50:15.623Z","participants":5,"position":1}

TEST_ANNOUNCEMENTS_LIST = [{
    'course_name': 'Donn Alexander Morrison testrom',
    'course_announcements': {
        'results' :TEST_COURSE_ANNOUNCEMENTS_LIST
    }
}, {
    'course_name': 'Sammensl??tt - Ingeni??rfaglig systemtenkning INGA2300 INGG2300 INGT2300 (2022 V??R)',
    'course_announcements': {
        'results' :TEST_COURSE_ANNOUNCEMENTS_LIST
    }
}, {
    'course_name': 'INGT2300 Ingeni??rfaglig systemtenkning (2022 V??R)',
    'course_announcements': {
        'results' :TEST_COURSE_ANNOUNCEMENTS_LIST
    }
}, {
    'course_name': 'Sammensl??tt - Matematiske metoder 3 for dataingeni??rer IMAX2150 (2021 H??ST)',
    'course_announcements': {
        'results' :TEST_COURSE_ANNOUNCEMENTS_LIST
    }
}, {
    'course_name': 'IMAT2150 Matematiske metoder 3 for dataingeni??rer (2021 H??ST)',
    'course_announcements': {
        'results' :TEST_COURSE_ANNOUNCEMENTS_LIST
    }
}, {
    'course_name': 'IDATT2900 Bacheloroppgave  (start 2021 H??ST)',
    'course_announcements': {
        'results' :TEST_COURSE_ANNOUNCEMENTS_LIST
    }
}]

class TestAnnouncementsServices(object):
    @classmethod
    def setup_class(cls):
        cls.test_session = requests.Session()

        cls.mock_get_patcher = patch('bbcli.services.announcements_services.requests.Session.get')
        cls.mock_auth_patcher = patch('bbcli.cli.authenticate_user')

        cls.mock_get = cls.mock_get_patcher.start()
        cls.mock_auth = cls.mock_auth_patcher.start()

    @classmethod
    def teardown_class(cls):
        cls.mock_get_patcher.stop()
        cls.mock_auth_patcher.stop()
        cls.test_session.close

    def test_list_announcement(self):
        self.mock_auth.return_value.ok = True
        self.mock_get.return_value.ok = True
        self.mock_get.return_value.text = json.dumps(TEST_ANNOUNCEMENT)

        # Id is irrelavant here because the API call is mocked anyways
        response = list_announcement(self.test_session, 'test_course_id', 'test_announcement_id')

        assert response == TEST_ANNOUNCEMENT


    def test_list_course_announcements(self):
        self.mock_auth.return_value.ok = True
        self.mock_get.return_value.ok = True
        self.mock_get.return_value.text = json.dumps({
                'results':TEST_COURSE_ANNOUNCEMENTS_LIST
            })

        # Id is irrelavant here because the API call is mocked anyways
        response = list_course_announcements(self.test_session, 'test_course_id')

        assert response == {
            'results': TEST_COURSE_ANNOUNCEMENTS_LIST
        }

    def test_list_announcements(self):
        self.mock_auth.return_value.ok = True
        self.mock_get.return_value.ok = True
        self.mock_get.return_value.text = json.dumps({
                'results': TEST_COURSE_ANNOUNCEMENTS_LIST
            })
        
        mock_get_courses_patcher = patch('bbcli.services.announcements_services.list_all_courses')
        mock_get_courses = mock_get_courses_patcher.start()

        mock_get_course_announcements_patcher = patch('bbcli.services.announcements_services.list_course_announcements')
        mock_get_course_announcements = mock_get_course_announcements_patcher.start()

        mock_get_courses.return_value = TEST_COURSES_LIST
        mock_get_course_announcements.return_value = {
            'results': TEST_COURSE_ANNOUNCEMENTS_LIST
        }

        response = list_announcements(self.test_session, 'test_user_name')

        mock_get_course_announcements_patcher.stop()
        mock_get_courses_patcher.stop()

        assert response == TEST_ANNOUNCEMENTS_LIST

    def test_create_annonucement(self):
        self.mock_auth.return_value.ok = True
        mock_input_body_patcher = patch('bbcli.services.announcements_services.input_body')
        mock_post_patcher = patch('bbcli.services.announcements_services.requests.Session.post')
        mock_input_body = mock_input_body_patcher.start()
        mock_post = mock_post_patcher.start()
        
        
        mock_input_body.return_value = 'This is a test announcement'
        mock_post.return_value.ok = True
        mock_post.return_value.text = json.dumps(TEST_CREATED_ANNOUNCEMENT)

        test_date_interval = DateInterval(start_date=format_date('15/04/22 22:00:00'))
        response = create_announcement(self.test_session, '_33050_1', 'Test announcement', test_date_interval, False)

        mock_input_body_patcher.stop()
        mock_post_patcher.stop()

        assert response == TEST_CREATED_ANNOUNCEMENT

    def test_create_announcement_with_empty_title(self):
        self.mock_auth.return_value.ok = True
        with pytest.raises(BadParameter):
            create_announcement(self.test_session, '_33050_1', '', DateInterval(), False)

    def test_create_annonucement_with_wrong_date_format(self):
        self.mock_auth.return_value.ok = True
        with pytest.raises(Abort):
            create_announcement(self.test_session, '_33050_1', 'Test annonucement', DateInterval(start=format_date('16-04-22 12:00')), False)


    def test_delete_announcement(self):
        self.mock_auth.return_value.ok = True

        mock_delete_patcher = patch('bbcli.services.announcements_services.requests.Session.delete')
        mock_delete = mock_delete_patcher.start()
        mock_delete.return_value.ok = True
        mock_delete.return_value.status_code = 204
        mock_delete.return_value.text = ''

        response = delete_announcement(self.test_session, 'test_course_id', 'test_announcement_id')

        assert response == ''

    def test_delete_announcement_with_wrong_announcement_id(self):
        self.mock_auth.return_value.ok = True

        mock_delete_patcher = patch('bbcli.services.announcements_services.requests.Session.delete')
        mock_delete = mock_delete_patcher.start()
        mock_delete.return_value.ok = False
        mock_delete.return_value = requests.models.Response()
        mock_delete.return_value.status_code = 404

        with pytest.raises(requests.exceptions.HTTPError):
            delete_announcement(self.test_session, 'test_course_id', 'test_announcement_id')

    def test_update_announcement(self):
        self.mock_auth.return_value.ok = True
        mock_update_patcher = patch('bbcli.cli.requests.Session.patch')
        mock_update = mock_update_patcher.start()
        mock_list_annonucement_patcher = patch('bbcli.services.announcements_services.list_announcement')
        mock_list_announcement = mock_list_annonucement_patcher.start()
        mock_list_announcement.return_value.ok = True
        mock_list_announcement.return_value = TEST_ANNOUNCEMENT
        mock_edit_title_patcher = patch('bbcli.services.announcements_services.edit_title')
        mock_edit_title = mock_edit_title_patcher.start()
        mock_edit_body_patcher = patch('bbcli.services.announcements_services.edit_body')
        mock_edit_body = mock_edit_body_patcher.start()


        mock_edit_title.return_value = 'TEST TITLE'
        mock_edit_body.return_value = 'TEST BODY'

        mock_update.return_value.ok = True
        mock_update.return_value.text = json.dumps(UPDATED_TEST_ANNOUNCEMENT)

        response = update_announcement(self.test_session, 'test_course_id', 'test_announcement_id', False)
        
        mock_update_patcher.stop()
        mock_list_annonucement_patcher.stop()
        mock_edit_title_patcher.stop()
        mock_edit_body_patcher.stop()

        assert response == UPDATED_TEST_ANNOUNCEMENT