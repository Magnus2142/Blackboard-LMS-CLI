import json
from re import M
from typing import List
from click import Abort, BadParameter
import requests

from unittest.mock import Mock, patch
from nose.tools import assert_list_equal, assert_equal, raises
from bbcli.entities.content_builder_entitites import DateInterval, FileOptions, GradingOptions, StandardOptions, WeblinkOptions
from bbcli.services.assignment_service import create_column_attempt, get_assignments, get_column_attempt, get_column_attempts, update_column_attempt
from bbcli.services.contents_service import create_assignment, create_document, create_externallink, create_file, create_folder, delete_content, update_content
from tests.test_services.test_announcements_services import UPDATED_TEST_ANNOUNCEMENT


TEST_ASSIGNMENTS_LIST = {"results":[{"id":"_275617_1","name":"Totalt","description":"<p>Den uvektede totalen av alle vurderinger for en bruker.</p>","externalGrade":True,"score":{"possible":3757.00000},"availability":{"available":"No"},"grading":{"type":"Calculated","schemaId":"_328072_1"},"gradebookCategoryId":"_654726_1","formula":{"formula":"{ \"running\":\"True\", \"all\":{\"average\":\"False\"}}"},"includeInCalculations":True,"showStatisticsToStudents":False},{"id":"_277393_1","name":"posted from CLI test","created":"2022-02-23T12:15:42.847Z","contentId":"_1666340_1","score":{"possible":100.00000},"availability":{"available":"Yes"},"grading":{"type":"Attempts","attemptsAllowed":1,"scoringModel":"Last","schemaId":"_328072_1","anonymousGrading":{"type":"None"}},"gradebookCategoryId":"_654732_1","includeInCalculations":True,"showStatisticsToStudents":False,"scoreProviderHandle":"resource/x-bb-assignment"},{"id":"_277394_1","name":"posted from CLI test","created":"2022-02-23T12:18:11.087Z","contentId":"_1666343_1","score":{"possible":100.00000},"availability":{"available":"Yes"},"grading":{"type":"Attempts","attemptsAllowed":1,"scoringModel":"Last","schemaId":"_328072_1","anonymousGrading":{"type":"None"}},"gradebookCategoryId":"_654732_1","includeInCalculations":True,"showStatisticsToStudents":False,"scoreProviderHandle":"resource/x-bb-assignment"},{"id":"_280663_1","name":"Test_04042022_1538","created":"2022-04-04T13:49:32.442Z","contentId":"_1696651_1","score":{"possible":100.00000},"availability":{"available":"Yes"},"grading":{"type":"Attempts","due":"2022-04-05T10:04:00.000Z","attemptsAllowed":1,"scoringModel":"Last","schemaId":"_328072_1","anonymousGrading":{"type":"None"}},"gradebookCategoryId":"_654732_1","includeInCalculations":True,"showStatisticsToStudents":False,"scoreProviderHandle":"resource/x-bb-assignment"},{"id":"_280808_1","name":"testing assignment","created":"2022-04-06T12:52:02.909Z","contentId":"_1698141_1","score":{"possible":69.00000},"availability":{"available":"Yes"},"grading":{"type":"Attempts","attemptsAllowed":1,"scoringModel":"Last","schemaId":"_328072_1","anonymousGrading":{"type":"None"}},"gradebookCategoryId":"_654732_1","includeInCalculations":True,"showStatisticsToStudents":False,"scoreProviderHandle":"resource/x-bb-assignment"},{"id":"_280809_1","name":"testing assignment 2","created":"2022-04-06T12:52:26.148Z","contentId":"_1698143_1","score":{"possible":123.00000},"availability":{"available":"Yes"},"grading":{"type":"Attempts","attemptsAllowed":1,"scoringModel":"Last","schemaId":"_328072_1","anonymousGrading":{"type":"None"}},"gradebookCategoryId":"_654732_1","includeInCalculations":True,"showStatisticsToStudents":False,"scoreProviderHandle":"resource/x-bb-assignment"},{"id":"_280839_1","name":"Mattias har klamma, True or False?","created":"2022-04-07T10:44:18.700Z","contentId":"_1698594_1","score":{"possible":69.00000},"availability":{"available":"Yes"},"grading":{"type":"Attempts","attemptsAllowed":0,"scoringModel":"Last","schemaId":"_328072_1","anonymousGrading":{"type":"None"}},"gradebookCategoryId":"_654732_1","includeInCalculations":True,"showStatisticsToStudents":False,"scoreProviderHandle":"resource/x-bb-assignment"},{"id":"_280850_1","name":"Kommer mattias på DT ikveld mon tro?","created":"2022-04-07T11:58:42.794Z","contentId":"_1698666_1","score":{"possible":96.00000},"availability":{"available":"Yes"},"grading":{"type":"Attempts","attemptsAllowed":1,"scoringModel":"Last","schemaId":"_328072_1","anonymousGrading":{"type":"None"}},"gradebookCategoryId":"_654732_1","includeInCalculations":True,"showStatisticsToStudents":False,"scoreProviderHandle":"resource/x-bb-assignment"},{"id":"_280968_1","name":"Ttest assignment hehehe","created":"2022-04-11T09:08:40.603Z","contentId":"_1699529_1","score":{"possible":100.00000},"availability":{"available":"No"},"grading":{"type":"Attempts","attemptsAllowed":1,"scoringModel":"Last","schemaId":"_328072_1","anonymousGrading":{"type":"None"}},"gradebookCategoryId":"_654732_1","includeInCalculations":True,"showStatisticsToStudents":False,"scoreProviderHandle":"resource/x-bb-assignment"},{"id":"_281043_1","name":"Test assignment","created":"2022-04-18T08:59:50.312Z","contentId":"_1699931_1","score":{"possible":1000.00000},"availability":{"available":"Yes"},"grading":{"type":"Attempts","attemptsAllowed":1,"scoringModel":"Last","schemaId":"_328072_1","anonymousGrading":{"type":"None"}},"gradebookCategoryId":"_654732_1","includeInCalculations":True,"showStatisticsToStudents":False,"scoreProviderHandle":"resource/x-bb-assignment"},{"id":"_281044_1","name":"Test assignment","created":"2022-04-18T09:02:48.606Z","contentId":"_1699933_1","score":{"possible":1000.00000},"availability":{"available":"Yes"},"grading":{"type":"Attempts","attemptsAllowed":1,"scoringModel":"Last","schemaId":"_328072_1","anonymousGrading":{"type":"None"}},"gradebookCategoryId":"_654732_1","includeInCalculations":True,"showStatisticsToStudents":False,"scoreProviderHandle":"resource/x-bb-assignment"},{"id":"_281045_1","name":"Test assignment","created":"2022-04-18T09:03:43.900Z","contentId":"_1699934_1","score":{"possible":1000.00000},"availability":{"available":"Yes"},"grading":{"type":"Attempts","attemptsAllowed":1,"scoringModel":"Last","schemaId":"_328072_1","anonymousGrading":{"type":"None"}},"gradebookCategoryId":"_654732_1","includeInCalculations":True,"showStatisticsToStudents":False,"scoreProviderHandle":"resource/x-bb-assignment"}]}
TEST_ASSIGNMENT_ATTEMPTS_LIST = {"results":[{"id":"_5330107_1","userId":"_111522_1","status":"Completed","displayGrade":{"scaleType":"Score","score":70.00000},"text":"70.00000","score":70.000000000000000,"feedback":"Jaja ca greit nok","studentComments":"Test comment.","studentSubmission":"<p>Test submission.</p>","exempt":False,"created":"2022-04-05T08:36:18.225Z","attemptDate":"2022-04-05T08:36:18.242Z","modified":"2022-04-06T13:38:15.169Z","attemptReceipt":{"receiptId":"e4473469b3674366a7837b0debb4d93e","submissionDate":"2022-04-05T08:36:18.229Z"}},{"id":"_5334307_1","userId":"_140040_1","status":"Completed","displayGrade":{"scaleType":"Score","score":100.00000},"text":"100.00000","score":100.000000000000000,"notes":"Helt UsERR","feedback":"Gratulerer","studentSubmission":"<p>Hva faen, Mattias ga klamma til Chloe \uD83D\uDE2F</p>","exempt":False,"created":"2022-04-06T07:25:46.278Z","attemptDate":"2022-04-06T07:25:46.313Z","modified":"2022-04-06T11:28:51.489Z","attemptReceipt":{"receiptId":"669bea9237164cd2b3dae5feee41f47c","submissionDate":"2022-04-06T07:25:46.283Z"}},{"id":"_5330216_1","userId":"_140955_1","status":"Completed","displayGrade":{"scaleType":"Score","score":100.00000},"text":"100.00000","score":100.000000000000000,"feedback":"Maggie er IKKE taperbb assignments grade --helpbb assignments grade --help","studentComments":"hva skjer","studentSubmission":"<p>adsfadsfadsf</p>","exempt":False,"created":"2022-04-05T08:54:56.286Z","attemptDate":"2022-04-05T08:54:56.302Z","modified":"2022-04-08T16:17:40.022Z","attemptReceipt":{"receiptId":"095f247c4e91492186b4416e94e20c22","submissionDate":"2022-04-05T08:54:56.290Z"}}]}
TEST_ATTEMPT = {
  "id": "_5330107_1",
  "userId": "_111522_1",
  "status": "Completed",
  "displayGrade": {
    "scaleType": "Score",
    "score": 70.0
  },
  "text": "70.00000",
  "score": 70.0,
  "feedback": "Jaja ca greit nok",
  "studentComments": "Test comment.",
  "studentSubmission": "<p>Test submission.</p>",
  "exempt": False,
  "created": "2022-04-05T08:36:18.225Z",
  "attemptDate": "2022-04-05T08:36:18.242Z",
  "modified": "2022-04-06T13:38:15.169Z",
  "attemptReceipt": {
    "receiptId": "e4473469b3674366a7837b0debb4d93e",
    "submissionDate": "2022-04-05T08:36:18.229Z"
  }
}
TEST_SUBMITTED_ATTEMPT = {'id': '_5361991_1', 'userId': '_140040_1', 'status': 'NeedsGrading', 'studentComments': 'I think yes', 'studentSubmission': 'TRUE, Mattias har klamma!', 'exempt': False, 'created': '2022-04-20T11:15:08.978Z'}
TEST_GRADE_ATTEMPT = {'id': '_5340506_1', 'userId': '_111522_1', 'status': 'Completed', 'feedback': 'Great work man!', 'studentComments': 'hallaballa', 'exempt': False, 'created': '2022-04-07T12:01:20.708Z', 'attemptDate': '2022-04-07T12:01:20.708Z', 'modified': '2022-04-20T10:59:43.098Z'}

class TestAssignmentsServices(object):
    @classmethod
    def setup_class(cls):
        cls.test_session = requests.Session()
        cls.mock_post_patcher = patch('bbcli.cli.requests.Session.post')
        cls.mock_get_patcher = patch('bbcli.services.announcements_service.requests.Session.get')
        cls.mock_auth_patcher = patch('bbcli.cli.authenticate_user')
        cls.mock_update_patcher = patch('bbcli.cli.requests.Session.patch')

        cls.mock_post = cls.mock_post_patcher.start()
        cls.mock_get = cls.mock_get_patcher.start()
        cls.mock_auth = cls.mock_auth_patcher.start()
        cls.mock_update = cls.mock_update_patcher.start()

    @classmethod
    def teardown_class(cls):
        cls.mock_post_patcher.stop()
        cls.mock_get_patcher.stop()
        cls.mock_auth_patcher.stop()
        cls.mock_update_patcher.stop()
        cls.test_session.close


    def test_get_assignments(self):
        self.mock_auth.return_value.ok = True
        self.mock_get.return_value.ok = True
        self.mock_get.return_value.text = json.dumps(TEST_ASSIGNMENTS_LIST)

        response = get_assignments(self.test_session, 'test_course_id')

        assert_equal(response, TEST_ASSIGNMENTS_LIST['results'])

    def test_get_column_attempts(self):
        self.mock_auth.return_value.ok = True
        self.mock_get.return_value.ok = True
        self.mock_get.return_value.text = json.dumps(TEST_ASSIGNMENT_ATTEMPTS_LIST)

        response = get_column_attempts(self.test_session, 'test_course_id', 'test_column_id')

        assert_equal(json.dumps(response), json.dumps(TEST_ASSIGNMENT_ATTEMPTS_LIST['results']))

    def test_get_column_attempt(self):
        self.mock_auth.return_value.ok = True
        self.mock_get.return_value.ok = True
        self.mock_get.return_value.text = json.dumps(TEST_ATTEMPT)

        response = get_column_attempt(self.test_session, 'test_course_id', 'test_column_id', 'test_attempt_id')

        assert_equal(response, json.dumps(TEST_ATTEMPT, indent=2))

    def create_column_attempt(self):
        self.mock_auth.return_value.ok = True
        self.mock_post.return_value.ok = True
        self.mock_post.return_value.text = json.dumps(TEST_SUBMITTED_ATTEMPT)
        
        response = create_column_attempt(self.test_session, 'test_course_id', 'test_column_id')

        assert_equal(response, TEST_SUBMITTED_ATTEMPT)

    def test_update_column_attempt(self):
        self.mock_auth.return_value.ok = True
        self.mock_update.return_value.ok = True
        self.mock_update.return_value.text = json.dumps(TEST_GRADE_ATTEMPT)

        response = update_column_attempt(self.test_session, 'test_course_id', 'test_column_id', 'test_attempt_id')

        assert_equal(response, TEST_GRADE_ATTEMPT)

