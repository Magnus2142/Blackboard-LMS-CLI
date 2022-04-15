import json
from click.testing import CliRunner

from unittest.mock import Mock, patch
from nose.tools import assert_list_equal, assert_equal, assert_true
from bbcli.cli import entry_point

TEST_ANNOUNCEMENT = {"id":"_388961_1","title":"TEST annonucement","body":"This is a test announcement","creator":"_140040_1","draft":False,"availability":{"duration":{"type":"Restricted","start":"2022-04-12T08:06:33.422Z","end":None}},"created":"2022-04-12T08:06:33.423Z","modified":"2022-04-12T08:06:33.452Z","position":2}
TEST_ANNOUNCEMENTS_LIST = {"results":[{"id":"_389026_1","title":"Testing announcement","body":"Here is a new announcement. Here is a \n<a href=\"https://ntnu.no\">link</a>.","creator":"_36000_1","draft":False,"availability":{"duration":{"type":"Restricted","start":"2022-04-13T16:33:01.758Z","end":None}},"created":"2022-04-13T16:33:01.759Z","modified":"2022-04-13T16:33:01.811Z","position":1},{"id":"_388961_1","title":"TEST annonucement","body":"This is a test announcement","creator":"_140040_1","draft":False,"availability":{"duration":{"type":"Restricted","start":"2022-04-12T08:06:33.422Z","end":None}},"created":"2022-04-12T08:06:33.423Z","modified":"2022-04-12T08:06:33.452Z","position":2},{"id":"_388929_1","title":"Title","creator":"_140040_1","draft":False,"availability":{"duration":{"type":"Restricted","start":"2022-04-11T13:08:11.740Z","end":None}},"created":"2022-04-11T13:08:11.741Z","modified":"2022-04-11T13:08:11.764Z","position":3},{"id":"_388916_1","title":"Title","body":"123123123","creator":"_140040_1","draft":False,"availability":{"duration":{"type":"Restricted","start":"2022-04-11T11:51:36.101Z","end":None}},"created":"2022-04-11T11:51:36.102Z","modified":"2022-04-11T11:51:36.127Z","position":4},{"id":"_388900_1","title":"ttest","creator":"_140040_1","draft":False,"availability":{"duration":{"type":"Restricted","start":"2022-04-11T10:06:36.842Z","end":None}},"created":"2022-04-11T10:06:36.843Z","modified":"2022-04-11T10:06:36.868Z","position":5},{"id":"_388883_1","title":"test date","creator":"_140040_1","draft":False,"availability":{"duration":{"type":"Restricted","start":"2022-04-11T08:14:56.225Z","end":None}},"created":"2022-04-11T08:14:56.228Z","modified":"2022-04-11T08:14:56.256Z","position":6},{"id":"_388882_1","title":"test date","body":"yy","creator":"_140040_1","draft":False,"availability":{"duration":{"type":"Restricted","start":"2022-04-11T08:14:43.985Z","end":None}},"created":"2022-04-11T08:14:43.986Z","modified":"2022-04-11T08:14:44.024Z","position":7},{"id":"_388881_1","title":"test date","body":"yy","creator":"_140040_1","draft":False,"availability":{"duration":{"type":"Restricted","start":"2022-04-11T08:14:15.569Z","end":None}},"created":"2022-04-11T08:14:15.570Z","modified":"2022-04-11T08:14:15.596Z","position":8},{"id":"_388880_1","title":"tt","creator":"_140040_1","draft":False,"availability":{"duration":{"type":"Restricted","start":"2022-04-11T08:09:55.734Z","end":None}},"created":"2022-04-11T08:09:55.736Z","modified":"2022-04-11T08:09:55.769Z","position":9},{"id":"_388879_1","title":"tt","creator":"_140040_1","draft":False,"availability":{"duration":{"type":"Restricted","start":"2022-04-11T08:08:49.680Z","end":None}},"created":"2022-04-11T08:08:49.682Z","modified":"2022-04-11T08:08:49.720Z","position":10}],"paging":{"nextPage":"/learn/api/public/v1/courses/_33050_1/announcements?offset=10"}}
TEST_COURSES_LIST = [{'id': '_33050_1', 'name': 'Donn Alexander Morrison testrom'}, {'id': '_32909_1', 'name': 'Sammenslått - Ingeniørfaglig systemtenkning INGA2300 INGG2300 INGT2300 (2022 VÅR)'}, {'id': '_31606_1', 'name': 'INGT2300 Ingeniørfaglig systemtenkning (2022 VÅR)'}, {'id': '_32736_1', 'name': 'Sammenslått - Matematiske metoder 3 for dataingeniører IMAX2150 (2021 HØST)'}, {'id': '_28936_1', 'name': 'IMAT2150 Matematiske metoder 3 for dataingeniører (2021 HØST)'}, {'id': '_27251_1', 'name': 'IDATT2900 Bacheloroppgave  (start 2021 HØST)'}]

TEST_CREATED_ANNOUNCEMENT = {"id":"_389054_1","title":"Test announcement","body":"This is a test announcement","creator":"_140040_1","draft":False,"availability":{"duration":{"type":"Restricted","start":"2022-04-15T22:04:00.000Z","end":None}},"created":"2022-04-15T13:50:15.623Z","modified":"2022-04-15T13:50:15.623Z","participants":5,"position":1}

class TestAnnouncements(object):
    @classmethod
    def setup_class(cls):
        cls.mock_get_patcher = patch('bbcli.cli.requests.Session.get')
        cls.mock_auth_patcher = patch('bbcli.cli.authenticate_user')
        cls.mock_list_courses_patcher = patch('bbcli.services.announcements_service.list_courses')
        cls.mock_post_patcher = patch('bbcli.cli.requests.Session.post')
        cls.mock_input_body_patcher = patch('bbcli.services.announcements_service.input_body')
        cls.mock_delete_patcher = patch('bbcli.cli.requests.Session.delete')
        cls.mock_update_patcher = patch('bbcli.cli.requests.Session.patch')
        cls.mock_click_edit_patcher = patch('bbcli.cli.click.edit')


        cls.mock_get = cls.mock_get_patcher.start()
        cls.mock_auth = cls.mock_auth_patcher.start()
        cls.mock_list_courses = cls.mock_list_courses_patcher.start()
        cls.mock_post = cls.mock_post_patcher.start()
        cls.mock_input_body = cls.mock_input_body_patcher.start()
        cls.mock_delete = cls.mock_delete_patcher.start()
        cls.mock_update = cls.mock_update_patcher.start()
        cls.mock_click_edit = cls.mock_click_edit_patcher.start()

    @classmethod
    def teardown_class(cls):
        cls.mock_get_patcher.stop()
        cls.mock_auth_patcher.stop()
        cls.mock_list_courses_patcher.stop()
        cls.mock_post_patcher.stop()
        cls.mock_input_body_patcher.stop()
        cls.mock_delete_patcher.stop()
        cls.mock_update_patcher.stop()
        cls.mock_click_edit_patcher.stop()


    def test_list_announcement(self):
        self.mock_auth.return_value.ok = True
        self.mock_get.return_value.ok = True
        self.mock_get.return_value.text = json.dumps(TEST_ANNOUNCEMENT)

        runner = CliRunner()
        result = runner.invoke(entry_point, ['announcements', 'list', '-c', '_33050_1', '-a', '_388961_1'])

        assert_equal(result.exit_code, 0)

    def test_list_course_announcements(self):
        self.mock_auth.return_value.ok = True
        self.mock_get.return_value.ok = True
        self.mock_get.return_value.text = json.dumps(TEST_ANNOUNCEMENTS_LIST)

        runner = CliRunner()
        result = runner.invoke(entry_point, ['announcements', 'list', '-c', '_33050_1'])

        assert_equal(result.exit_code, 0)

    def test_list_all_announcements(self):
        self.mock_auth.return_value.ok = True
        self.mock_get.return_value.ok = True
        self.mock_get.return_value.text = json.dumps(TEST_ANNOUNCEMENTS_LIST)
        self.mock_list_courses.return_value.ok = True
        self.mock_list_courses.return_value = TEST_COURSES_LIST

        runner = CliRunner()
        result = runner.invoke(entry_point, ['announcements', 'list'])

        assert_true(self.mock_list_courses.called)
        assert_equal(result.exit_code, 0)

    def test_create_announcement(self):
        self.mock_auth.return_value.ok = True

        self.mock_post.return_value.ok = True
        self.mock_post.return_value.text = json.dumps(TEST_CREATED_ANNOUNCEMENT)

        self.mock_input_body.return_value = 'This is a test announcement'

        runner = CliRunner()
        result = runner.invoke(entry_point, ['announcements', 'create', 'Test announcement', '-c', '_33050_1', '--start-date', '15/04/22 22:00:00'])
        
        assert_equal(result.exit_code, 0)

    def test_create_announcement_with_empty_title(self):
        self.mock_auth.return_value.ok = True

        runner = CliRunner()
        result = runner.invoke(entry_point, ['announcements', 'create', '', '-c', '_33050_1', '--start-date', '15/04/22 22:00:00'])
        
        assert_equal(result.exit_code, 2)

    def test_create_annonucement_with_wrong_date_format(self):
        self.mock_auth.return_value.ok = True

        runner = CliRunner()
        result = runner.invoke(entry_point, ['announcements', 'create', 'Test announcement', '-c', '_33050_1', '--start-date', '15-04-22 22:00'])

        assert_equal(result.exit_code, 1)

    def test_delete_announcement(self):
        self.mock_auth.return_value.ok = True
        self.mock_delete.return_value.ok = True

        runner = CliRunner()
        result = runner.invoke(entry_point, ['announcements', 'delete', '-c', '_33050_1', '-a', '_389054_1'])

        assert_equal(result.exit_code, 0)

    def test_update_announcement(self):
        self.mock_auth.return_value.ok = True

        mock_list_annonucement_patcher = patch('bbcli.services.announcements_service.list_announcement')
        mock_list_announcement = mock_list_annonucement_patcher.start()
        mock_list_announcement.return_value.ok = True
        mock_list_announcement.return_value = TEST_ANNOUNCEMENT

        self.mock_click_edit.return_value = {
            'title': TEST_ANNOUNCEMENT['title'],
            'body': TEST_ANNOUNCEMENT['body'],
            'created': TEST_ANNOUNCEMENT['created'],
            'availability': TEST_ANNOUNCEMENT['availability'],
            'draft': TEST_ANNOUNCEMENT['draft']
        }

        self.mock_update.return_value.ok = True
        self.mock_update.return_value.text = json.dumps(TEST_ANNOUNCEMENT)

        runner = CliRunner()
        result = runner.invoke(entry_point, ['announcements', 'update', '-c', '_33050_1', '-a', '_389054_1'])

        mock_list_annonucement_patcher.stop()

        assert_equal(result.exit_code, 0)