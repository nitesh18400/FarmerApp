from django.test import TestCase

from ..models import Farmer, HindiFarmerDetails, MarathiFarmerDetails, TeleguFarmerDetails, PunjabiFarmerDetail


def expected_result(lang):
    return f"{lang}test_{lang}testVillage_{lang}testDistrict_{lang}testState_0000000000"


# Create your tests here.
class FarmerModelTestCase(TestCase):
    def setUp(self):
        inserted_farmer = Farmer.objects.create(name="test",
                                                village_name="testVillage",
                                                district_name="testDistrict",
                                                state_name="testState",
                                                phone_number="0000000000")
        HindiFarmerDetails.objects.create(
            name="hitest",
            farmer=inserted_farmer,
            village_name="hitestVillage",
            district_name="hitestDistrict",
            state_name="hitestState",
        )

        MarathiFarmerDetails.objects.create(
            name="mrtest",
            farmer=inserted_farmer,
            village_name="mrtestVillage",
            district_name="mrtestDistrict",
            state_name="mrtestState",
        )

        TeleguFarmerDetails.objects.create(
            name="tetest",
            farmer=inserted_farmer,
            village_name="tetestVillage",
            district_name="tetestDistrict",
            state_name="tetestState",
        )

        PunjabiFarmerDetail.objects.create(
            name="putest",
            farmer=inserted_farmer,
            village_name="putestVillage",
            district_name="putestDistrict",
            state_name="putestState",
        )

    def test_get_farmer_details(self):
        farmer = Farmer.objects.get(name="test")
        self.assertEqual(farmer.get_details(), expected_result(""))

    def test_get_farmer_hindi_details(self):
        hindi_farmer = HindiFarmerDetails.objects.get(name="hitest")
        self.assertEqual(hindi_farmer.get_details(), expected_result("hi"))

    def test_get_farmer_marathi_details(self):
        marathi_farmer = MarathiFarmerDetails.objects.get(name="mrtest")
        self.assertEqual(marathi_farmer.get_details(), expected_result("mr"))

    def test_get_farmer_telegu_details(self):
        telegu_farmer = TeleguFarmerDetails.objects.get(name="tetest")
        self.assertEqual(telegu_farmer.get_details(), expected_result("te"))

    def test_get_farmer_punjabi_details(self):
        punjabi_farmer = PunjabiFarmerDetail.objects.get(name="putest")
        self.assertEqual(punjabi_farmer.get_details(), expected_result("pu"))
