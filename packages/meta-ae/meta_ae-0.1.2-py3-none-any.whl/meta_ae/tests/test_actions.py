from dateutil.relativedelta import relativedelta
from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase, tag
from edc_action_item.models import ActionItem
from edc_constants.constants import YES, CLOSED, NEW
from edc_facility.import_holidays import import_holidays
from edc_facility.models import Holiday
from edc_randomization.management.commands import import_randomization_list
from edc_randomization.models import RandomizationList
from edc_randomization.randomization_list_importer import RandomizationListImporter
from edc_sites.tests.site_test_case_mixin import SiteTestCaseMixin
from edc_utils.date import get_utcnow
from meta_screening.models import (
    ScreeningPartOne,
    ScreeningPartTwo,
    ScreeningPartThree,
    SubjectScreening,
)
from meta_screening.tests.options import (
    part_one_eligible_options,
    part_two_eligible_options,
    part_three_eligible_options,
)
from meta_sites.sites import fqdn, meta_sites
from model_mommy import mommy
from edc_adverse_event.constants import (
    AE_FOLLOWUP_ACTION,
    AE_TMG_ACTION,
    DEATH_REPORT_ACTION,
    DEATH_REPORT_TMG_ACTION,
)
from edc_reportable.constants import GRADE4, GRADE5


class MetaTestCaseMixin(SiteTestCaseMixin):

    fqdn = fqdn

    default_sites = meta_sites

    site_names = [s[1] for s in default_sites]

    import_randomization_list = True

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        if cls.import_randomization_list:
            RandomizationListImporter(verbose=False)
        import_holidays(test=True)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        RandomizationList.objects.all().delete()
        Holiday.objects.all().delete()

    def get_subject_screening(self):
        part_one = ScreeningPartOne.objects.create(
            user_created="erikvw", user_modified="erikvw", **part_one_eligible_options
        )
        screening_identifier = part_one.screening_identifier
        self.assertEqual(part_one.eligible_part_one, YES)

        screening_part_two = ScreeningPartTwo.objects.get(
            screening_identifier=screening_identifier
        )
        for k, v in part_two_eligible_options.items():
            setattr(screening_part_two, k, v)
        screening_part_two.save()
        print(screening_part_two.reasons_ineligible_part_two)
        self.assertEqual(screening_part_two.eligible_part_two, YES)

        screening_part_three = ScreeningPartThree.objects.get(
            screening_identifier=screening_identifier
        )
        for k, v in part_three_eligible_options.items():
            setattr(screening_part_three, k, v)
        screening_part_three.save()
        self.assertEqual(screening_part_three.eligible_part_three, YES)

        subject_screening = SubjectScreening.objects.get(
            screening_identifier=screening_identifier
        )
        self.assertTrue(subject_screening.eligible)
        return subject_screening

    def get_subject_consent(self, subject_screening):
        return mommy.make_recipe(
            "meta_consent.subjectconsent",
            user_created="erikvw",
            user_modified="erikvw",
            screening_identifier=subject_screening.screening_identifier,
            initials=subject_screening.initials,
            dob=get_utcnow().date()
            - relativedelta(years=subject_screening.age_in_years),
        )


class TestActions(MetaTestCaseMixin, TestCase):
    @classmethod
    def setUpClass(cls):
        import_holidays()
        import_randomization_list
        return super(TestActions, cls).setUpClass()

    def test_ae_initial_creates_action(self):
        subject_screening = self.get_subject_screening()
        subject_consent = self.get_subject_consent(subject_screening)
        ae_initial = mommy.make_recipe(
            "meta_ae.aeinitial", subject_identifier=subject_consent.subject_identifier
        )

        try:
            action_item = ActionItem.objects.get(
                action_identifier=ae_initial.action_identifier
            )
        except ObjectDoesNotExist:
            self.fail("ObjectDoesNotExist unexpectedly raised.")
        else:
            self.assertEqual(action_item.status, CLOSED)
            self.assertEqual(
                action_item.subject_identifier, subject_consent.subject_identifier
            )

    def test_ae_initial_creates_ae_followup_action(self):
        subject_screening = self.get_subject_screening()
        subject_consent = self.get_subject_consent(subject_screening)
        ae_initial = mommy.make_recipe(
            "meta_ae.aeinitial", subject_identifier=subject_consent.subject_identifier
        )

        action_item = ActionItem.objects.get(
            action_identifier=ae_initial.action_identifier
        )
        try:
            action_item = ActionItem.objects.get(
                parent_action_item=action_item,
                action_type__name=AE_FOLLOWUP_ACTION,
                subject_identifier=subject_consent.subject_identifier,
            )
        except ObjectDoesNotExist:
            self.fail("ObjectDoesNotExist unexpectedly raised.")
        else:
            self.assertEqual(action_item.status, NEW)

    def test_ae_initial_G4_creates_ae_tmg_action(self):
        subject_screening = self.get_subject_screening()
        subject_consent = self.get_subject_consent(subject_screening)
        mommy.make_recipe(
            "meta_ae.aeinitial",
            subject_identifier=subject_consent.subject_identifier,
            ae_grade=GRADE4,
        )

        try:
            ActionItem.objects.get(
                action_type__name=AE_TMG_ACTION,
                subject_identifier=subject_consent.subject_identifier,
            )
        except ObjectDoesNotExist:
            self.fail("ObjectDoesNotExist unexpectedly raised.")

    def test_ae_initial_G5_creates_death_report_action(self):
        subject_screening = self.get_subject_screening()
        subject_consent = self.get_subject_consent(subject_screening)
        mommy.make_recipe(
            "meta_ae.aeinitial",
            subject_identifier=subject_consent.subject_identifier,
            ae_grade=GRADE5,
        )
        try:
            ActionItem.objects.get(
                action_type__name=DEATH_REPORT_ACTION,
                subject_identifier=subject_consent.subject_identifier,
            )
        except ObjectDoesNotExist:
            self.fail("ObjectDoesNotExist unexpectedly raised.")

        self.assertRaises(
            ObjectDoesNotExist,
            ActionItem.objects.get,
            action_type__name=DEATH_REPORT_TMG_ACTION,
            subject_identifier=subject_consent.subject_identifier,
        )

    def test_death_report_create_death_report_tmg_action(self):
        subject_screening = self.get_subject_screening()
        subject_consent = self.get_subject_consent(subject_screening)
        mommy.make_recipe(
            "meta_ae.aeinitial",
            subject_identifier=subject_consent.subject_identifier,
            ae_grade=GRADE5,
        )
        action_item = ActionItem.objects.get(
            action_type__name=DEATH_REPORT_ACTION,
            subject_identifier=subject_consent.subject_identifier,
        )

        mommy.make_recipe(
            "meta_ae.deathreport",
            subject_identifier=subject_consent.subject_identifier,
            action_identifier=action_item.action_identifier,
        )

        action_item.refresh_from_db()
        self.assertEqual(action_item.status, CLOSED)

        try:
            action_item = ActionItem.objects.get(
                action_type__name=DEATH_REPORT_TMG_ACTION,
                subject_identifier=subject_consent.subject_identifier,
            )
        except ObjectDoesNotExist:
            self.fail("ObjectDoesNotExist unexpectedly raised.")
        else:
            self.assertEqual(action_item.status, NEW)
