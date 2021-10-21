from django.utils import timezone
from rest_framework import serializers

from camac.instance.master_data import MasterData

KIND_OF_WORK_NEW = 6001
FLOOR_GROUND_FLOOR = 3100
COUNTRY_SWITZERLAND = "Schweiz"
TYPE_OF_CLIENT_PERSON = 6161


def complete_floor(dwelling):
    if dwelling.get("floor_type") == FLOOR_GROUND_FLOOR:
        return FLOOR_GROUND_FLOOR

    if dwelling.get("floor_type") and dwelling.get("floor_number"):
        return dwelling.get("floor_type") + int(dwelling.get("floor_number")) - 1

    return None  # pragma: no cover


def to_int(string):
    return int(string) if string else None


def get_kind_of_work(building):
    building_proposal = building.get("proposal")
    return (
        building_proposal[0] if building_proposal and len(building_proposal) else None
    )


def dwelling_data(dwelling):
    return {
        "floor": complete_floor(dwelling),
        "floorType": dwelling.get("floor_type"),
        "floorNumber": to_int(dwelling.get("floor_number")),
        "locationOfDwellingOnFloor": dwelling.get("location_on_floor"),
        "noOfHabitableRooms": dwelling.get("number_of_rooms"),
        "kitchen": dwelling.get("has_kitchen_facilities"),
        "surfaceAreaOfDwelling": dwelling.get("area"),
        "multipleFloor": dwelling.get("multiple_floors"),
        "usageLimitation": dwelling.get("usage_limitation"),
    }


class GwrSerializer(serializers.Serializer):
    def __init__(self, case, *args, **kwargs):
        super().__init__(case, *args, **kwargs)
        self.master_data = MasterData(case)

    officialConstructionProjectFileNo = serializers.SerializerMethodField()

    typeOfClient = serializers.SerializerMethodField()
    client = serializers.SerializerMethodField()

    typeOfConstructionProject = serializers.SerializerMethodField()
    constructionProjectDescription = serializers.SerializerMethodField()
    constructionLocalisation = serializers.SerializerMethodField()
    typeOfConstruction = serializers.SerializerMethodField()
    typeOfPermit = serializers.SerializerMethodField()
    totalCostsOfProject = serializers.SerializerMethodField()
    realestateIdentification = serializers.SerializerMethodField()

    projectAnnouncementDate = serializers.SerializerMethodField()
    buildingPermitIssueDate = serializers.SerializerMethodField()
    projectStartDate = serializers.SerializerMethodField()
    projectCompletionDate = serializers.SerializerMethodField()
    work = serializers.SerializerMethodField()

    def get_client(self, case):
        applicants = self.master_data.applicants

        if not applicants or not len(applicants):
            return None  # pragma: no cover

        applicant = applicants[0]

        return {
            "address": {
                "town": applicant.get("town"),
                "swissZipCode": applicant.get("zip"),
                "street": applicant.get("street"),
                "houseNumber": applicant.get("street_number"),
                "country": {
                    "countryNameShort": "ch"
                    if applicant.get("country") == COUNTRY_SWITZERLAND
                    else None,
                },
            },
            "identification": {
                "personIdentification": {
                    "officialName": applicant.get("last_name"),
                    "firstName": applicant.get("first_name"),
                }
                if not applicant.get("is_juristic_person")
                else None,
                "isOrganisation": applicant.get("is_juristic_person"),
                "organisationIdentification": {
                    "organisationName": applicant.get("juristic_name")
                    if applicant.get("is_juristic_person")
                    else None
                },
            },
        }

    def get_officialConstructionProjectFileNo(self, case):
        # TODO Configure this for SZ
        try:
            return self.master_data.dossier_number
        except AttributeError:  # pragma: no cover
            return None

    def get_constructionProjectDescription(self, case):
        return self.master_data.proposal

    def get_constructionLocalisation(self, case):
        # TODO Configure this for SZ
        try:
            return {"municipalityName": self.master_data.municipality.get("label")}
        except AttributeError:  # pragma: no cover
            return None

    def get_typeOfConstructionProject(self, case):
        # TODO Configure this for BE and SZ
        try:
            return self.master_data.category[0]
        except (AttributeError, IndexError):  # pragma: no cover
            return None

    def get_typeOfConstruction(self, case):
        # TODO Configure this for BE and SZ
        try:
            return self.master_data.type_of_construction[0]["art_der_hochbaute"]
        except (AttributeError, IndexError):  # pragma: no cover
            return None

    def get_totalCostsOfProject(self, case):
        return self.master_data.construction_costs

    def get_realestateIdentification(self, case):
        try:
            plot_data = self.master_data.plot_data[0]
            return {
                "number": plot_data.get("plot_number"),
                "EGRID": plot_data.get("egrid_number"),
            }
        except IndexError:  # pragma: no cover
            return None

    def get_projectAnnouncementDate(self, case):
        # TODO Configure this for SZ
        try:
            submit_date = self.master_data.submit_date
            return submit_date.date().isoformat() if submit_date else None
        except AttributeError:  # pragma: no cover
            return None

    def get_buildingPermitIssueDate(self, case):
        # TODO Configure this for BE and SZ
        try:
            decision_date = self.master_data.decision_date
            return decision_date.date().isoformat() if decision_date else None
        except AttributeError:  # pragma: no cover
            return None

    def get_projectStartDate(self, case):
        # TODO Configure this for BE and SZ
        try:
            start_date = self.master_data.construction_start_date
            return start_date.date().isoformat() if start_date else None
        except AttributeError:  # pragma: no cover
            return None

    def get_projectCompletionDate(self, case):
        # TODO Configure this for BE and SZ
        try:
            end_date = self.master_data.construction_end_date
            return end_date.date().isoformat() if end_date else None
        except AttributeError:  # pragma: no cover
            return None

    def get_energy_device(self, building, is_heating, is_main_heating):

        canton = self.master_data.canton

        if canton == "SZ" and is_main_heating:
            heat_generator = (
                building.get("heating_heat_generator")
                if is_heating
                else building.get("warmwater_heat_generator")
            )
            energy_source = (
                building.get("heating_energy_source")
                if is_heating
                else building.get("warmwater_energy_source")
            )

            heat_generator_key = "heatGenerator" + (
                "Heating" if is_heating else "HotWater"
            )
            return {
                heat_generator_key: heat_generator,
                "energySourceHeating": energy_source,
            }

        if canton == "UR":
            heating_type = "is_heating" if is_heating else "is_warm_water"
            building_name = building.get("name")
            return next(
                (
                    {
                        "energySourceHeating": device.get("energy_source"),
                        "informationSourceHeating": device.get("information_source"),
                        "revisionDate": timezone.now().date(),
                    }
                    for device in self.master_data.energy_devices
                    if device.get(heating_type)
                    and device.get("name_of_building") == building_name
                    and device.get("is_main_heating") == is_main_heating
                ),
                None,
            )

        return None

    def get_dwellings(self, building):

        canton = self.master_data.canton

        if canton == "SZ":
            dwellings = building.get("dwellings") if building.get("dwellings") else []
            return [dwelling_data(dwelling) for dwelling in dwellings]

        if canton == "UR":
            return [
                dwelling_data(dwelling)
                for dwelling in self.master_data.dwellings
                if dwelling.get("name_of_building") == building.get("name")
            ]

        return []  # pragma: no cover

    def get_construction_date(self, building):
        construction_date = self.master_data.construction_end_date
        proposal = building.get("proposal")

        return (
            {"yearMonthDay": construction_date.date().isoformat()}
            if proposal and KIND_OF_WORK_NEW in proposal and construction_date
            else None
        )

    def get_work(self, case):
        # TODO Configure this for BE
        try:
            buildings = self.master_data.buildings

            return [
                {
                    "kindOfWork": get_kind_of_work(building),
                    "building": {
                        "nameOfBuilding": building.get("name"),
                        "buildingCategory": building.get("building_category"),
                        "civilDefenseShelter": building.get("civil_defense_shelter"),
                        "dateOfConstruction": self.get_construction_date(building)
                        if self.master_data.canton == "UR"
                        else None,
                        "thermotechnicalDeviceForHeating1": self.get_energy_device(
                            building, is_heating=True, is_main_heating=True
                        ),
                        "thermotechnicalDeviceForHeating2": self.get_energy_device(
                            building, is_heating=True, is_main_heating=False
                        ),
                        "thermotechnicalDeviceForWarmWater1": self.get_energy_device(
                            building, is_heating=False, is_main_heating=True
                        ),
                        "thermotechnicalDeviceForWarmWater2": self.get_energy_device(
                            building, is_heating=False, is_main_heating=False
                        ),
                        "realestateIdentification": self.get_realestateIdentification(
                            case
                        )
                        if self.master_data.canton == "UR"
                        else None,
                        "dwellings": self.get_dwellings(building),
                    },
                }
                for building in buildings
            ]
        except (AttributeError, IndexError):  # pragma: no cover
            return []

    def get_typeOfPermit(self, case):
        # TODO Configure this for BE and SZ
        try:
            reason = self.master_data.approval_reason
            return int(reason) if reason else None
        except AttributeError:  # pragma: no cover
            return None

    def get_typeOfClient(self, case):
        # TODO Configure this for BE and SZ
        try:
            type_of_applicant = (
                self.master_data.type_of_applicant
                if self.master_data.canton == "UR"
                else None
            )
            if type_of_applicant:
                return int(type_of_applicant)

            applicants = self.master_data.applicants
            applicant = applicants[0] if applicants and len(applicants) else None
            if applicant and applicant.get("is_juristic_person") is False:
                return TYPE_OF_CLIENT_PERSON

            return None  # pragma: no cover
        except AttributeError:  # pragma: no cover
            return None
