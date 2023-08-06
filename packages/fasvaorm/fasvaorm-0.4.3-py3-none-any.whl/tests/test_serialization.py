import unittest

from fasvaorm import Drive, Vehicle, Campaign
from tests.test_models import TEST_DRIVE, TEST_VEHICLE, TEST_CAMPAIGN


class TestDriveSerialization(unittest.TestCase):

    def test_serialize_flat(self):

        drive = Drive(**TEST_DRIVE)
        drive.vehicle = Vehicle(**TEST_VEHICLE)
        drive.campaign = Campaign(**TEST_CAMPAIGN)

        result = drive.to_dict()

        data = TEST_DRIVE.copy()
        data['vehicle'] = TEST_VEHICLE
        data['vehicle']['idvehicle'] = None

        data['campaign'] = TEST_CAMPAIGN
        data['campaign']['idcampaign'] = None

        for k in ['name', 'start', 'end']:
            self.assertEqual(data[k], result[k])

    def test_serialize_deep(self):
        drive = Drive(**TEST_DRIVE)
        drive.vehicle = Vehicle(**TEST_VEHICLE)
        drive.campaign = Campaign(**TEST_CAMPAIGN)

        result = drive.to_dict(deep=True)

        data = TEST_DRIVE.copy()
        data['iddrive'] = None

        data['vehicle'] = TEST_VEHICLE
        data['idvehicle'] = None
        data['vehicle']['idvehicle'] = None

        data['campaign'] = TEST_CAMPAIGN
        data['idcampaign'] = None
        data['campaign']['idcampaign'] = None

        self.assertEqual(data, result)
