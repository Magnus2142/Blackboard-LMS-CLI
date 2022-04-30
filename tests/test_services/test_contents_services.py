import json
from re import M
from typing import List
from click import Abort, BadParameter
import requests

from unittest.mock import Mock, patch
from nose.tools import assert_list_equal, assert_equal, raises
from bbcli.entities.content_builder_entitites import DateInterval, FileOptions, GradingOptions, StandardOptions, WeblinkOptions
from bbcli.services.contents_services import create_assignment, create_document, create_externallink, create_file, create_folder, delete_content, update_content

TEST_CREATED_DOCUMENT = {"id":"_1699922_1","parentId":"_1699223_1","title":"Test document","body":"This is a test document","created":"2022-04-18T08:02:18.316Z","modified":"2022-04-18T08:02:18.410Z","position":0,"launchInNewWindow":False,"reviewable":False,"availability":{"available":"Yes","allowGuests":True,"allowObservers":True,"adaptiveRelease":{}},"contentHandler":{"id":"resource/x-bb-document"},"links":[{"href":"/ultra/courses/_33050_1/cl/outline?legacyUrl=%2Fwebapps%2Fblackboard%2Fexecute%2FdisplayIndividualContent%3Fcourse_id%3D_33050_1%26content_id%3D_1699922_1","rel":"alternate","title":"User Interface View","type":"text/html"}]}
TEST_CREATED_FILE = {"id":"_1699925_1","parentId":"_1645559_1","title":"Test file","created":"2022-04-18T08:27:32.497Z","modified":"2022-04-18T08:27:32.497Z","position":16,"launchInNewWindow":False,"reviewable":False,"availability":{"available":"Yes","allowGuests":True,"allowObservers":True,"adaptiveRelease":{}},"contentHandler":{"id":"resource/x-bb-file","file":{"fileName":"pdf-test.pdf"}},"links":[{"href":"/ultra/courses/_33050_1/cl/outline?legacyUrl=%2Fwebapps%2Fblackboard%2Fexecute%2FdisplayIndividualContent%3Fcourse_id%3D_33050_1%26content_id%3D_1699925_1","rel":"alternate","title":"User Interface View","type":"text/html"}]}
TEST_CREATED_EXTERNALLINK = {"id":"_1699927_1","parentId":"_1645559_1","title":"Test web-link","created":"2022-04-18T08:48:07.119Z","modified":"2022-04-18T08:48:07.148Z","position":17,"launchInNewWindow":False,"reviewable":False,"availability":{"available":"Yes","allowGuests":True,"allowObservers":True,"adaptiveRelease":{}},"contentHandler":{"id":"resource/x-bb-externallink","url":"https://vg.no/"},"links":[{"href":"/ultra/courses/_33050_1/cl/outline?legacyUrl=%2Fwebapps%2Fblackboard%2Fexecute%2FdisplayIndividualContent%3Fcourse_id%3D_33050_1%26content_id%3D_1699927_1","rel":"alternate","title":"User Interface View","type":"text/html"}]}
TEST_CREATED_FOLDER = {"id":"_1699929_1","parentId":"_1645559_1","title":"Test folder","body":"This is a test folder","created":"2022-04-18T08:51:37.878Z","modified":"2022-04-18T08:51:37.897Z","position":18,"hasChildren":True,"launchInNewWindow":False,"reviewable":False,"availability":{"available":"Yes","allowGuests":True,"allowObservers":True,"adaptiveRelease":{}},"contentHandler":{"id":"resource/x-bb-folder"},"links":[{"href":"/ultra/courses/_33050_1/cl/outline?legacyUrl=%2Fwebapps%2Fblackboard%2Fexecute%2FdisplayIndividualContent%3Fcourse_id%3D_33050_1%26content_id%3D_1699929_1","rel":"alternate","title":"User Interface View","type":"text/html"}]}
TEST_CREATED_ASSIGNMENT = {"contentId":"_1699934_1","gradeColumnId":"_281045_1","attachmentIds":["_4322478_1","_4322479_1"]}

TEST_GET_CONTENT = {'id': '_1698141_1', 'parentId': '_1697863_1', 'title': 'testing assignment', 'body': '<p>asdfasdf</p>', 'created': '2022-04-06T12:52:02.900Z', 'modified': '2022-04-11T09:42:33.594Z', 'position': 4, 'hasGradebookColumns': True, 'launchInNewWindow': False, 'reviewable': False, 'availability': {'available': 'Yes', 'allowGuests': True, 'allowObservers': True, 'adaptiveRelease': {}}, 'contentHandler': {'id': 'resource/x-bb-assignment', 'gradeColumnId': '_280808_1', 'groupContent': False}, 'links': [{'href': '/ultra/courses/_33050_1/cl/outline?legacyUrl=%2Fwebapps%2Fblackboard%2Fexecute%2FdisplayIndividualContent%3Fcourse_id%3D_33050_1%26content_id%3D_1698141_1', 'rel': 'alternate', 'title': 'User Interface View', 'type': 'text/html'}]}
TEST_GET_CONTENT_UPDATED = {'id': '_1698141_1', 'parentId': '_1697863_1', 'title': 'TEST TITLE', 'body': 'TEST BODY', 'created': '2022-04-06T12:52:02.900Z', 'modified': '2022-04-11T09:42:33.594Z', 'position': 4, 'hasGradebookColumns': True, 'launchInNewWindow': False, 'reviewable': False, 'availability': {'available': 'Yes', 'allowGuests': True, 'allowObservers': True, 'adaptiveRelease': {}}, 'contentHandler': {'id': 'resource/x-bb-assignment', 'gradeColumnId': '_280808_1', 'groupContent': False}, 'links': [{'href': '/ultra/courses/_33050_1/cl/outline?legacyUrl=%2Fwebapps%2Fblackboard%2Fexecute%2FdisplayIndividualContent%3Fcourse_id%3D_33050_1%26content_id%3D_1698141_1', 'rel': 'alternate', 'title': 'User Interface View', 'type': 'text/html'}]}

TEST_UPLOADED_FILE = {'id': '53-5321C30FA434825104FDC83B173BF720-abcdf665d3294daf8addddc56a670674'}


class TestContentsServices(object):
    @classmethod
    def setup_class(cls):
        cls.test_session = requests.Session()
        cls.mock_post_patcher = patch('bbcli.cli.requests.Session.post')
        cls.mock_get_patcher = patch('bbcli.services.announcements_services.requests.Session.get')
        cls.mock_auth_patcher = patch('bbcli.cli.authenticate_user')

        cls.mock_post = cls.mock_post_patcher.start()
        cls.mock_get = cls.mock_get_patcher.start()
        cls.mock_auth = cls.mock_auth_patcher.start()

    @classmethod
    def teardown_class(cls):
        cls.mock_post_patcher.stop()
        cls.mock_get_patcher.stop()
        cls.mock_auth_patcher.stop()
        cls.test_session.close


    def test_create_document(self):
        self.mock_auth.return_value.ok = True
        mock_input_body_patcher = patch('bbcli.services.contents_services.input_body')
        mock_input_body = mock_input_body_patcher.start()
        mock_input_body.return_value = 'This is a test document'
        
        standard_options = StandardOptions(date_interval=DateInterval())
        self.mock_post.return_value.ok = True
        self.mock_post.return_value.text = json.dumps(TEST_CREATED_DOCUMENT)

        response = create_document(self.test_session, 'test_course_id', 'test_parent_id', 'Test document', standard_options, None, False)

        mock_input_body_patcher.stop()

        assert_equal(response, TEST_CREATED_DOCUMENT)

    def test_create_file(self):
        self.mock_auth.return_value.ok = True
        mock_upload_file_patcher = patch('bbcli.services.contents_services.upload_file')
        mock_upload_file = mock_upload_file_patcher.start()

        mock_upload_file.return_value = TEST_UPLOADED_FILE

        standard_options = StandardOptions(date_interval=DateInterval())
        self.mock_post.return_value.ok = True
        self.mock_post.return_value.text = json.dumps(TEST_CREATED_FILE)

        response = create_file(self.test_session, 'test_course_id', 'test_parent_id', 'Test file', 'tests/test_resources/pdf-test.pdf', FileOptions(), standard_options)

        mock_upload_file_patcher.stop()

        assert_equal(response, TEST_CREATED_FILE)

    
    def test_create_externallink(self):
        self.mock_auth.return_value.ok = True
        
        standard_options = StandardOptions(date_interval=DateInterval())
        self.mock_post.return_value.ok = True
        self.mock_post.return_value.text = json.dumps(TEST_CREATED_EXTERNALLINK)

        response = create_externallink(self.test_session, 'test_course_id', 'test_parent_id', 'Test web-link', 'https://vg.no/', WeblinkOptions(), standard_options)

        assert_equal(response, TEST_CREATED_EXTERNALLINK)

    def test_create_folder(self):
        self.mock_auth.return_value.ok = True
        mock_input_body_patcher = patch('bbcli.services.contents_services.input_body')
        mock_input_body = mock_input_body_patcher.start()
        mock_input_body.return_value = 'This is a test folder'
        


        standard_options = StandardOptions(date_interval=DateInterval())
        self.mock_post.return_value.ok = True
        self.mock_post.return_value.text = json.dumps(TEST_CREATED_FOLDER)

        response = create_folder(self.test_session, 'test_course_id', 'test_parent_id', 'Test folder', False, standard_options, False)

        mock_input_body_patcher.stop()

        assert_equal(response, TEST_CREATED_FOLDER)

    def test_create_assignment(self):
        self.mock_auth.return_value.ok = True
        mock_input_body_patcher = patch('bbcli.services.contents_services.input_body')
        mock_input_body = mock_input_body_patcher.start()
        mock_input_body.return_value = 'This is a test assignment'
        mock_upload_file_patcher = patch('bbcli.services.contents_services.upload_file')
        mock_upload_file = mock_upload_file_patcher.start()
        mock_upload_file.return_value = TEST_UPLOADED_FILE

        standard_options = StandardOptions(date_interval=DateInterval())
        self.mock_post.return_value.ok = True
        self.mock_post.return_value.text = json.dumps(TEST_CREATED_ASSIGNMENT)

        response = create_assignment(self.test_session, 'test_course_id', 'test_parent_id', 'Test assignment', standard_options, GradingOptions(), ('tests/test_resources/pdf-test.pdf', 'tests/test_resources/pdf-test.pdf'), False)

        mock_input_body_patcher.stop()
        mock_upload_file_patcher.stop()

        assert_equal(response, TEST_CREATED_ASSIGNMENT)


    def test_delete_content(self):
        self.mock_auth.return_value.ok = True
        mock_delete_patcher = patch('bbcli.cli.requests.Session.delete')
        mock_delete = mock_delete_patcher.start()
        mock_delete.return_value = requests.models.Response()
        mock_delete.return_value.status_code = 204 

        response = delete_content(self.test_session, 'test_course_id', 'test_parent_id', True)

        mock_delete_patcher.stop()

        assert_equal(response.status_code, 204)

    def test_update_content(self):
        self.mock_auth.return_value.ok = True
        mock_update_patcher = patch('bbcli.cli.requests.Session.patch')
        mock_update = mock_update_patcher.start()
        mock_edit_title_patcher = patch('bbcli.services.contents_services.edit_title')
        mock_edit_title = mock_edit_title_patcher.start()
        mock_edit_body_patcher = patch('bbcli.services.contents_services.update_content_data')
        mock_edit_body = mock_edit_body_patcher.start()
        self.mock_get.return_value.text = json.dumps(TEST_GET_CONTENT)

        mock_edit_title.return_value = 'TEST TITLE'
        mock_edit_body.return_value = {'body' : 'TEST BODY'}

        mock_update.return_value.ok = True
        mock_update.return_value.text = json.dumps(TEST_GET_CONTENT_UPDATED)

        response = update_content(self.test_session, 'test_course_id', 'test_content_id', False)
        
        mock_update_patcher.stop()
        mock_edit_title_patcher.stop()
        mock_edit_body_patcher.stop()

        assert_equal(response, TEST_GET_CONTENT_UPDATED)