import json
from typing import List
from click.testing import CliRunner
import requests
from bbcli.services.courses_service import list_all_courses, list_course, list_courses

from unittest.mock import Mock, patch
from nose.tools import assert_list_equal, assert_equal

TEST_COURSE = {
        'id':'_33050_1',
        'uuid':'909cbb1f296140f3ab307df8bc1a0ee3',
        'externalId':'194_DAMTEST_2022V_1', 
        'dataSourceId':'_209_1',
        'courseId':'194_DAMTEST_2022V_1',
        'name':'Donn Alexander Morrison testrom',
        'created':'2022-02-03T14:10:39.451Z',
        'modified':'2022-02-03T14:10:45.960Z',
        'organization':False,
        'ultraStatus':'Classic',
        'allowGuests':False,
        'allowObservers':False,
        'closedComplete':False,
        'termId':'_108_1',
        'availability':{
            'available':'Yes',
            'duration':{
                'type':'Continuous'
            }
        },
        'enrollment':{
            'type':'InstructorLed'
        },
        'locale':{
            'id':'en_US',
            'force':False
        },
        'externalAccessUrl':'https://ntnu.blackboard.com/ultra/courses/_33050_1/cl/outline'
    }
    
TEST_COURSE_LIST = [{'id': '_33050_1', 'name': 'Donn Alexander Morrison testrom', 'termId': '_108_1'}, {'id': '_32909_1', 'name': 'Sammenslått - Ingeniørfaglig systemtenkning INGA2300 INGG2300 INGT2300 (2022 VÅR)', 'termId': '_108_1'}, {'id': '_31606_1', 'name': 'INGT2300 Ingeniørfaglig systemtenkning (2022 VÅR)', 'termId': '_108_1'}, {'id': '_32736_1', 'name': 'Sammenslått - Matematiske metoder 3 for dataingeniører IMAX2150 (2021 HØST)', 'termId': '_107_1'}, {'id': '_28936_1', 'name': 'IMAT2150 Matematiske metoder 3 for dataingeniører (2021 HØST)', 'termId': '_107_1'}, {'id': '_27251_1', 'name': 'IDATT2900 Bacheloroppgave  (start 2021 HØST)', 'termId': '_107_1'}, {'id': '_26748_1', 'name': 'Sammenslått - Fysikk/kjemi (2021 vår)', 'termId': '_64_1'}, {'id': '_21080_1', 'name': 'IFYT1001 Fysikk (2021 VÅR)', 'termId': '_64_1'}, {'id': '_22151_1', 'name': 'IDATT2106 Systemutvikling 2 med smidig prosjekt (2021 VÅR)', 'termId': '_64_1'}, {'id': '_22056_1', 'name': 'IDATT2105 Full-stack applikasjonsutvikling (2021 VÅR)', 'termId': '_64_1'}, {'id': '_22212_1', 'name': 'IDATT2104 Nettverksprogrammering (2021 VÅR)', 'termId': '_64_1'}, {'id': '_7921_1', 'name': 'Lab IIR', 'termId': '_28_1'}, {'id': '_26511_1', 'name': 'Dataingeniør Trondheim (BIDATA): Kull 2020', 'termId': '_63_1'}, {'id': '_26287_1', 'name': 'Sammenslått - Statistikk ISTX1001 ISTX1002 ISTX1003 (2020 HØST)', 'termId': '_63_1'}, {'id': '_21671_1', 'name': 'ISTT1003 Statistikk (2020 HØST)', 'termId': '_63_1'}, {'id': '_26170_1', 'name': 'IDATT2202 Operativsystemer (2020 HØST)', 'termId': '_63_1'}, {'id': '_22259_1', 'name': 'IDATT2103 Databaser (2020 HØST)', 'termId': '_63_1'}, {'id': '_22398_1', 'name': 'IDATT2101 Algoritmer og datastrukturer (2020 HØST)', 'termId': '_63_1'}, {'id': '_20124_1', 'name': 'IMAT2021 Matematiske metoder 2 for Dataingeniør (2020 VÅR)', 'termId': '_49_1'}, {'id': '_18976_1', 'name': 'IDATT2001 Programmering 2 (2020 VÅR)', 'termId': '_49_1'}, {'id': '_19418_1', 'name': 'IDATT1002 Systemutvikling (2020 VÅR)', 'termId': '_49_1'}, {'id': '_20377_1', 'name': 'Bachelor i Dataingeniør 2019-2022', 'termId': '_46_1'}, {'id': '_18715_1', 'name': 'HMS0002 HMS-kurs for 1. årsstudenter (2019 HØST)', 'termId': '_46_1'}, {'id': '_20187_1', 'name': 'Sammenslått - Ingeniørfaglig innføringsemne (2019 HØST)', 'termId': '_46_1'}, {'id': '_16575_1', 'name': 'INGT1001 Ingeniørfaglig innføringsemne (2019 HØST)', 'termId': '_46_1'}, {'id': '_20275_1', 'name': 'Sammenslått - Matematiske metoder 1 (2019 HØST)', 'termId': '_46_1'}, {'id': '_20016_1', 'name': 'IMAT1001 Matematiske metoder 1 (2019 HØST)', 'termId': '_46_1'}, {'id': '_19119_1', 'name': 'IDATT1001 Programmering 1 (2019 HØST)', 'termId': '_46_1'}]

TEST_TERMS_LIST = [{'id': '_22_1', 'name': 'Andre', 'description': '<p>Emner som ikke faller i vanlige semester-terminologi. F.eks. test-emner, sommerkurs o.l.</p>', 'availability': {'available': 'No', 'duration': {'type': 'Continuous'}}}, {'id': '_40_1', 'name': 'Høst 2013', 'availability': {'available': 'Yes', 'duration': {'type': 'DateRange', 'start': '2013-08-14T22:00:00.000Z', 'end': '2014-01-01T22:59:59.000Z'}}}, {'id': '_41_1', 'name': 'Høst 2014', 'availability': {'available': 'Yes', 'duration': {'type': 'DateRange', 'start': '2014-08-14T22:00:00.000Z', 'end': '2015-01-01T22:59:59.000Z'}}}, {'id': '_31_1', 'name': 'Høst 2015', 'availability': {'available': 'Yes', 'duration': {'type': 'DateRange', 'start': '2015-08-14T22:00:00.000Z', 'end': '2016-01-01T22:59:59.000Z'}}}, {'id': '_23_1', 'name': 'Høst 2016', 'availability': {'available': 'Yes', 'duration': {'type': 'DateRange', 'start': '2016-08-14T22:00:00.000Z', 'end': '2017-01-01T22:59:59.000Z'}}}, {'id': '_28_1', 'name': 'Høst 2017', 'availability': {'available': 'Yes', 'duration': {'type': 'DateRange', 'start': '2017-08-14T22:00:00.000Z', 'end': '2018-01-01T22:59:59.000Z'}}}, {'id': '_35_1', 'name': 'Høst 2018', 'availability': {'available': 'Yes', 'duration': {'type': 'DateRange', 'start': '2018-08-14T22:00:00.000Z', 'end': '2019-01-01T22:59:59.000Z'}}}, {'id': '_46_1', 'name': 'Høst 2019', 'description': '<p>2019 HØST</p>', 'availability': {'available': 'Yes', 'duration': {'type': 'DateRange', 'start': '2019-06-30T22:00:00.000Z', 'end': '2020-01-01T22:59:59.000Z'}}}, {'id': '_63_1', 'name': 'Høst 2020', 'description': '2020 HØST', 'availability': {'available': 'Yes', 'duration': {'type': 'DateRange', 'start': '2020-06-30T22:00:00.000Z', 'end': '2021-01-01T22:59:59.000Z'}}}, {'id': '_107_1', 'name': 'Høst 2021', 'description': '2021 HØST', 'availability': {'available': 'Yes', 'duration': {'type': 'DateRange', 'start': '2021-06-30T22:00:00.000Z', 'end': '2022-01-01T22:59:59.000Z'}}}, {'id': '_47_1', 'name': 'Vår 2013', 'description': '2013 VÅR', 'availability': {'available': 'Yes', 'duration': {'type': 'DateRange', 'start': '2012-12-31T23:00:00.000Z', 'end': '2013-08-15T21:59:59.000Z'}}}, {'id': '_48_1', 'name': 'Vår 2014', 'description': '2014 VÅR', 'availability': {'available': 'Yes', 'duration': {'type': 'DateRange', 'start': '2013-12-31T23:00:00.000Z', 'end': '2014-08-15T21:59:59.000Z'}}}, {'id': '_39_1', 'name': 'Vår 2015', 'availability': {'available': 'Yes', 'duration': {'type': 'DateRange', 'start': '2014-12-31T23:00:00.000Z', 'end': '2015-08-15T21:59:59.000Z'}}}, {'id': '_30_1', 'name': 'Vår 2016', 'availability': {'available': 'Yes', 'duration': {'type': 'DateRange', 'start': '2015-12-31T23:00:00.000Z', 'end': '2016-08-15T21:59:59.000Z'}}}, {'id': '_25_1', 'name': 'Vår 2017', 'availability': {'available': 'Yes', 'duration': {'type': 'DateRange', 'start': '2016-12-31T23:00:00.000Z', 'end': '2017-08-15T21:59:59.000Z'}}}, {'id': '_29_1', 'name': 'Vår 2018', 'availability': {'available': 'Yes', 'duration': {'type': 'DateRange', 'start': '2017-12-31T23:00:00.000Z', 'end': '2018-08-15T21:59:59.000Z'}}}, {'id': '_37_1', 'name': 'Vår 2019', 'description': '<p>Vår 2019</p>', 'availability': {'available': 'Yes', 'duration': {'type': 'DateRange', 'start': '2018-12-31T23:00:00.000Z', 'end': '2019-08-15T21:59:59.000Z'}}}, {'id': '_49_1', 'name': 'Vår 2020', 'description': '2020 VÅR', 'availability': {'available': 'Yes', 'duration': {'type': 'DateRange', 'start': '2019-12-31T23:00:00.000Z', 'end': '2020-08-15T21:59:59.000Z'}}}, {'id': '_64_1', 'name': 'Vår 2021', 'description': '2021 VÅR', 'availability': {'available': 'Yes', 'duration': {'type': 'DateRange', 'start': '2020-12-31T23:00:00.000Z', 'end': '2021-08-15T21:59:59.000Z'}}}, {'id': '_108_1', 'name': 'Vår 2022', 'description': '2022 VÅR', 'availability': {'available': 'Yes', 'duration': {'type': 'DateRange', 'start': '2021-12-31T23:00:00.000Z', 'end': '2022-08-15T21:59:59.000Z'}}}]
TEST_COURSE_MEMBERSHIPS_LIST = [{'id': '_2202371_1', 'userId': '_140040_1', 'courseId': '_33050_1', 'dataSourceId': '_2_1', 'created': '2022-02-03T14:21:22.934Z', 'modified': '2022-04-07T10:41:10.608Z', 'availability': {'available': 'Yes'}, 'courseRoleId': 'Instructor', 'lastAccessed': '2022-04-14T07:41:56.840Z'}, {'id': '_2170002_1', 'userId': '_140040_1', 'courseId': '_32909_1', 'childCourseId': '_31606_1', 'dataSourceId': '_190_1', 'created': '2022-01-10T13:52:35.968Z', 'modified': '2022-01-10T13:52:35.968Z', 'availability': {'available': 'Yes'}, 'courseRoleId': 'Student', 'lastAccessed': '2022-04-12T08:03:47.568Z'}, {'id': '_2170001_1', 'userId': '_140040_1', 'courseId': '_31606_1', 'dataSourceId': '_190_1', 'created': '2022-01-10T13:52:35.968Z', 'modified': '2022-01-10T13:52:40.055Z', 'availability': {'available': 'Yes'}, 'courseRoleId': 'Student', 'lastAccessed': '2022-04-12T08:09:50.538Z'}, {'id': '_1950113_1', 'userId': '_140040_1', 'courseId': '_32736_1', 'childCourseId': '_28936_1', 'dataSourceId': '_189_1', 'created': '2021-06-16T14:48:23.886Z', 'modified': '2021-08-22T03:39:59.747Z', 'availability': {'available': 'Yes'}, 'courseRoleId': 'Student', 'lastAccessed': '2022-04-13T08:44:48.605Z'}, {'id': '_1799061_1', 'userId': '_140040_1', 'courseId': '_28936_1', 'dataSourceId': '_189_1', 'created': '2021-06-16T14:48:23.886Z', 'modified': '2021-08-18T05:58:25.413Z', 'availability': {'available': 'Yes'}, 'courseRoleId': 'Student', 'lastAccessed': '2022-04-13T08:44:50.836Z'}, {'id': '_1799010_1', 'userId': '_140040_1', 'courseId': '_27251_1', 'dataSourceId': '_189_1', 'created': '2021-06-16T14:48:17.698Z', 'modified': '2021-07-01T21:44:55.485Z', 'availability': {'available': 'Yes'}, 'courseRoleId': 'Student', 'lastAccessed': '2022-04-13T18:49:48.217Z'}, {'id': '_1698193_1', 'userId': '_140040_1', 'courseId': '_26748_1', 'childCourseId': '_21080_1', 'dataSourceId': '_137_1', 'created': '2020-12-01T13:48:27.469Z', 'modified': '2021-07-01T18:56:35.176Z', 'availability': {'available': 'Yes'}, 'courseRoleId': 'Student', 'lastAccessed': '2022-02-24T12:46:33.685Z'}, {'id': '_1578419_1', 'userId': '_140040_1', 'courseId': '_21080_1', 'dataSourceId': '_137_1', 'created': '2020-12-01T13:48:27.469Z', 'modified': '2021-07-01T18:36:24.374Z', 'availability': {'available': 'Yes'}, 'courseRoleId': 'Student'}, {'id': '_1578296_1', 'userId': '_140040_1', 'courseId': '_22151_1', 'dataSourceId': '_137_1', 'created': '2020-12-01T13:48:17.232Z', 'modified': '2021-07-01T18:33:54.962Z', 'availability': {'available': 'Yes'}, 'courseRoleId': 'Student', 'lastAccessed': '2022-02-24T12:47:30.901Z'}, {'id': '_1578292_1', 'userId': '_140040_1', 'courseId': '_22056_1', 'dataSourceId': '_137_1', 'created': '2020-12-01T13:48:16.815Z', 'modified': '2021-07-01T21:02:13.469Z', 'availability': {'available': 'Yes'}, 'courseRoleId': 'Student', 'lastAccessed': '2022-02-23T12:02:28.245Z'}, {'id': '_1578288_1', 'userId': '_140040_1', 'courseId': '_22212_1', 'dataSourceId': '_137_1', 'created': '2020-12-01T13:48:16.419Z', 'modified': '2021-07-01T22:00:31.942Z', 'availability': {'available': 'Yes'}, 'courseRoleId': 'Student', 'lastAccessed': '2022-04-06T07:11:32.061Z'}, {'id': '_1576797_1', 'userId': '_140040_1', 'courseId': '_7921_1', 'dataSourceId': '_2_1', 'created': '2020-12-01T08:18:46.350Z', 'modified': '2021-07-01T21:52:45.398Z', 'availability': {'available': 'Yes'}, 'courseRoleId': 'Student', 'lastAccessed': '2021-01-29T12:29:44.448Z'}, {'id': '_1471353_1', 'userId': '_140040_1', 'courseId': '_26511_1', 'dataSourceId': '_2_1', 'created': '2020-08-12T08:00:27.724Z', 'modified': '2021-07-01T18:05:27.249Z', 'availability': {'available': 'Yes'}, 'courseRoleId': 'Student', 'lastAccessed': '2022-01-27T23:14:36.786Z'}, {'id': '_1355366_1', 'userId': '_140040_1', 'courseId': '_26287_1', 'childCourseId': '_21671_1', 'dataSourceId': '_136_1', 'created': '2020-06-24T12:46:53.972Z', 'modified': '2021-07-01T21:46:01.545Z', 'availability': {'available': 'Yes'}, 'courseRoleId': 'Student', 'lastAccessed': '2022-01-30T20:14:48.151Z'}, {'id': '_1355365_1', 'userId': '_140040_1', 'courseId': '_21671_1', 'dataSourceId': '_136_1', 'created': '2020-06-24T12:46:53.972Z', 'modified': '2021-07-01T21:47:37.536Z', 'availability': {'available': 'Yes'}, 'courseRoleId': 'Student'}, {'id': '_1355339_1', 'userId': '_140040_1', 'courseId': '_26170_1', 'dataSourceId': '_136_1', 'created': '2020-06-24T12:46:50.584Z', 'modified': '2021-07-01T17:50:03.902Z', 'availability': {'available': 'Yes'}, 'courseRoleId': 'Student', 'lastAccessed': '2021-03-04T12:17:07.070Z'}, {'id': '_1355336_1', 'userId': '_140040_1', 'courseId': '_22259_1', 'dataSourceId': '_136_1', 'created': '2020-06-24T12:46:50.328Z', 'modified': '2021-07-01T20:49:45.419Z', 'availability': {'available': 'Yes'}, 'courseRoleId': 'Student', 'lastAccessed': '2022-02-27T10:06:08.755Z'}, {'id': '_1355334_1', 'userId': '_140040_1', 'courseId': '_22398_1', 'dataSourceId': '_136_1', 'created': '2020-06-24T12:46:50.156Z', 'modified': '2021-07-01T20:41:06.878Z', 'availability': {'available': 'Yes'}, 'courseRoleId': 'Student', 'lastAccessed': '2021-02-22T11:16:48.492Z'}, {'id': '_1157613_1', 'userId': '_140040_1', 'courseId': '_20124_1', 'dataSourceId': '_115_1', 'created': '2019-12-05T11:58:57.000Z', 'modified': '2021-07-01T20:30:11.616Z', 'availability': {'available': 'Yes'}, 'courseRoleId': 'Student', 'lastAccessed': '2021-11-03T12:11:21.815Z'}, {'id': '_1157600_1', 'userId': '_140040_1', 'courseId': '_18976_1', 'dataSourceId': '_115_1', 'created': '2019-12-05T11:58:55.000Z', 'modified': '2021-07-01T20:23:45.086Z', 'availability': {'available': 'Yes'}, 'courseRoleId': 'Student', 'lastAccessed': '2022-04-06T07:25:32.063Z'}, {'id': '_1157598_1', 'userId': '_140040_1', 'courseId': '_19418_1', 'dataSourceId': '_115_1', 'created': '2019-12-05T11:58:54.000Z', 'modified': '2021-07-01T18:06:54.921Z', 'availability': {'available': 'Yes'}, 'courseRoleId': 'Student', 'lastAccessed': '2021-02-22T11:16:48.492Z'}, {'id': '_1092393_1', 'userId': '_140040_1', 'courseId': '_20377_1', 'dataSourceId': '_2_1', 'created': '2019-09-06T06:46:20.000Z', 'modified': '2021-07-01T20:19:28.268Z', 'availability': {'available': 'Yes'}, 'courseRoleId': 'Student', 'lastAccessed': '2021-01-29T12:29:44.448Z'}, {'id': '_1041298_1', 'userId': '_140040_1', 'courseId': '_18715_1', 'dataSourceId': '_113_1', 'created': '2019-08-15T12:49:52.000Z', 'modified': '2021-07-01T21:38:11.204Z', 'availability': {'available': 'Yes'}, 'courseRoleId': 'Student', 'lastAccessed': '2021-01-29T12:29:44.448Z'}, {'id': '_1017688_1', 'userId': '_140040_1', 'courseId': '_20187_1', 'childCourseId': '_16575_1', 'dataSourceId': '_113_1', 'created': '2019-08-12T10:49:52.000Z', 'modified': '2021-07-01T21:40:08.101Z', 'availability': {'available': 'Yes'}, 'courseRoleId': 'Student', 'lastAccessed': '2022-02-24T12:50:33.685Z'}, {'id': '_1017687_1', 'userId': '_140040_1', 'courseId': '_16575_1', 'dataSourceId': '_113_1', 'created': '2019-08-12T10:49:52.000Z', 'modified': '2021-07-01T17:52:59.620Z', 'availability': {'available': 'Yes'}, 'courseRoleId': 'Student'}, {'id': '_1017686_1', 'userId': '_140040_1', 'courseId': '_20275_1', 'childCourseId': '_20016_1', 'dataSourceId': '_113_1', 'created': '2019-08-12T10:49:52.000Z', 'modified': '2021-07-01T17:19:27.132Z', 'availability': {'available': 'Yes'}, 'courseRoleId': 'Student', 'lastAccessed': '2021-02-22T11:16:48.492Z'}, {'id': '_1017685_1', 'userId': '_140040_1', 'courseId': '_20016_1', 'dataSourceId': '_113_1', 'created': '2019-08-12T10:49:52.000Z', 'modified': '2021-07-01T20:12:10.899Z', 'availability': {'available': 'Yes'}, 'courseRoleId': 'Student'}, {'id': '_1017684_1', 'userId': '_140040_1', 'courseId': '_19119_1', 'dataSourceId': '_113_1', 'created': '2019-08-12T10:49:52.000Z', 'modified': '2021-07-01T19:41:17.783Z', 'availability': {'available': 'Yes'}, 'courseRoleId': 'Student', 'lastAccessed': '2021-02-22T11:16:48.492Z'}]

TEST_COURSE_LIST_SORTED_AND_SHORTENED = [{'id': '_33050_1', 'name': 'Donn Alexander Morrison testrom'}, {'id': '_32909_1', 'name': 'Sammenslått - Ingeniørfaglig systemtenkning INGA2300 INGG2300 INGT2300 (2022 VÅR)'}, {'id': '_31606_1', 'name': 'INGT2300 Ingeniørfaglig systemtenkning (2022 VÅR)'}, {'id': '_32736_1', 'name': 'Sammenslått - Matematiske metoder 3 for dataingeniører IMAX2150 (2021 HØST)'}, {'id': '_28936_1', 'name': 'IMAT2150 Matematiske metoder 3 for dataingeniører (2021 HØST)'}, {'id': '_27251_1', 'name': 'IDATT2900 Bacheloroppgave  (start 2021 HØST)'}]

class TestCoursesServices(object):
    @classmethod
    def setup_class(cls):
        cls.mock_get_patcher = patch('bbcli.services.courses_service.requests.Session.get')
        cls.mock_auth_patcher = patch('bbcli.cli.authenticate_user')
        # cls.mock_get_terms_patcher = patch('bbcli.services.courses_service.get_terms')
        # cls.mock_get_memberships_patcher = patch('bbcli.services.courses_service.get_course_memberships')

        cls.mock_get = cls.mock_get_patcher.start()
        cls.mock_auth = cls.mock_auth_patcher.start()

    @classmethod
    def teardown_class(cls):
        cls.mock_get_patcher.stop()
        cls.mock_auth_patcher.stop()


    def test_list_course(self):
        self.mock_auth.return_value.ok = True
        self.mock_get.return_value.ok = True
        self.mock_get.return_value.text = json.dumps(TEST_COURSE)

        test_session = requests.Session()
        # Id is irrelavant here because the API call is mocked anyways
        response = list_course(test_session, '_33050_1')

        assert_equal(response, TEST_COURSE)

    def test_list_courses(self):
        self.mock_auth.return_value.ok = True

        mock_get_terms_patcher = patch('bbcli.services.courses_service.get_terms')
        mock_get_memberships_patcher = patch('bbcli.services.courses_service.get_course_memberships')
        mock_get_courses_patcher = patch('bbcli.services.courses_service.get_courses_from_course_memberships')
        mock_get_terms = mock_get_terms_patcher.start()
        mock_get_memberships = mock_get_memberships_patcher.start()
        mock_get_courses = mock_get_courses_patcher.start()

        mock_get_terms.return_value = TEST_TERMS_LIST
        mock_get_memberships.return_value = TEST_COURSE_MEMBERSHIPS_LIST
        mock_get_courses.return_value = TEST_COURSE_LIST

        test_session = requests.Session()
         # user name is irrelavant here because the API call is mocked anyways
        response = list_courses(test_session, 'test_user')

        mock_get_terms_patcher.stop()
        mock_get_memberships_patcher.stop()
        mock_get_courses_patcher.stop()

        assert_equal(response, TEST_COURSE_LIST_SORTED_AND_SHORTENED)

    def test_list_all_courses(self):
        self.mock_auth.return_value.ok = True

        mock_get_memberships_patcher = patch('bbcli.services.courses_service.get_course_memberships')
        mock_get_courses_patcher = patch('bbcli.services.courses_service.get_courses_from_course_memberships')
        mock_get_memberships = mock_get_memberships_patcher.start()
        mock_get_courses = mock_get_courses_patcher.start()

        mock_get_memberships.return_value = TEST_COURSE_MEMBERSHIPS_LIST
        mock_get_courses.return_value = TEST_COURSE_LIST

        test_session = requests.Session()
        response = list_all_courses(test_session, 'test_user')

        assert_equal(response, TEST_COURSE_LIST)