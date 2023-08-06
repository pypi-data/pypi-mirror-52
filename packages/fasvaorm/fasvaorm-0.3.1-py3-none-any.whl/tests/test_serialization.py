import unittest

from fasvaorm import Drive, Vehicle, Campaign
from tests.test_models import TEST_DRIVE, TEST_VEHICLE, TEST_CAMPAIGN


class TestDrive(unittest.TestCase):

    def test_create_drive(self):
        """Test if we can add the a drive which depends on a vehicle to our database
        """

        drive = Drive(**TEST_DRIVE)
        drive.vehicle = Vehicle(**TEST_VEHICLE)
        drive.campaign = Campaign(**TEST_CAMPAIGN)

        result = drive.to_dict()

        data = TEST_DRIVE
        data['vehicle'] = TEST_VEHICLE
        data['vehicle']['idvehicle'] = None

        data['campaign'] = TEST_CAMPAIGN
        data['campaign']['idcampaign'] = None

        self.assertEqual(data, result)
