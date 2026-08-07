"""
Management command: seed_dummy_data
Populates the database with realistic-looking ESEA dummy data.
Safe to re-run: uses get_or_create / update_or_create where possible.
"""

import random
from datetime import date, timedelta

from django.contrib.auth.hashers import make_password
from django.core.management.base import BaseCommand
from django.utils.timezone import now

from core.models import (
    CustomUser, Organisation, OrganisationMember,
    Network, NetworkMember, Membership,
    Method, Topic, DirectIndicator, IndirectIndicator,
    StakeholderGroup, Survey, Section, Question, AnswerOption,
    Campaign, EseaAccount, Respondent, SurveyResponse, QuestionResponse,
    Dashboard,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _rand_date(years_back=1):
    base = date.today() - timedelta(days=365 * years_back)
    return base + timedelta(days=random.randint(0, 365))


# ---------------------------------------------------------------------------
# Command
# ---------------------------------------------------------------------------

class Command(BaseCommand):
    help = "Seed the database with realistic ESEA dummy data"

    def handle(self, *args, **options):
        self.stdout.write(self.style.MIGRATE_HEADING("=== Seeding dummy data ==="))

        # ---- Users --------------------------------------------------------
        self.stdout.write("  Creating users…")
        admin = self._upsert_user("admin", "admin@openesea.org", "Admin", "van", "ESEA", superuser=True)
        alice  = self._upsert_user("alice.dupont",  "alice@verdantcorp.com",   "Alice",  "",    "Dupont")
        bob    = self._upsert_user("bob.schmidt",   "bob@nexocraft.de",        "Bob",    "van", "Schmidt")
        caro   = self._upsert_user("caro.jensen",   "caro@circlegoods.dk",     "Caro",   "",    "Jensen")
        diana  = self._upsert_user("diana.moreau",  "diana@solisgroup.fr",     "Diana",  "de",  "Moreau")
        evan   = self._upsert_user("evan.kowalski", "evan@biomaterialspl.com", "Evan",   "",    "Kowalski")
        felix  = self._upsert_user("felix.auditor", "felix@audit-firm.eu",     "Felix",  "",    "Gruber")

        # ---- Organisations ------------------------------------------------
        self.stdout.write("  Creating organisations…")
        verdant   = self._upsert_org("Verdant Corp",       alice,  "Sustainable textile manufacturer based in Lyon.")
        nexo      = self._upsert_org("Nexocraft GmbH",     bob,    "Precision engineering firm focused on clean-tech components.")
        circle    = self._upsert_org("Circle Goods ApS",   caro,   "Circular-economy retailer, Copenhagen.")
        solis     = self._upsert_org("Solis Group SA",     diana,  "Renewable-energy consultancy, Paris.")
        biomats   = self._upsert_org("BioMaterials Sp. z o.o.", evan, "Bio-based packaging producer, Warsaw.")

        # Nest the users as org members; also add admin as admin to every org
        for org, user in [(verdant, alice), (nexo, bob), (circle, caro), (solis, diana), (biomats, evan)]:
            OrganisationMember.objects.get_or_create(
                organisation=org, user=user,
                defaults=dict(role=OrganisationMember.ORGANISATIONADMIN, invitation="accepted")
            )
            OrganisationMember.objects.get_or_create(
                organisation=org, user=admin,
                defaults=dict(role=OrganisationMember.ORGANISATIONADMIN, invitation="accepted")
            )

        # ---- Method -------------------------------------------------------
        self.stdout.write("  Creating ESEA method…")
        method, _ = Method.objects.get_or_create(
            name="ESEA Standard",
            defaults=dict(
                created_by=admin,
                ispublic=True,
                description="Holistic Environmental, Social & Economic Accountability standard for SMEs.",
                version="2.00",
                certification_theshold="60.00",
            )
        )

        # ---- Topics -------------------------------------------------------
        self.stdout.write("  Creating topics…")
        env   = self._upsert_topic(method, "Environment",      None,  "Environmental impact and resource use.")
        soc   = self._upsert_topic(method, "Social",           None,  "Employee and community wellbeing.")
        econ  = self._upsert_topic(method, "Economic",         None,  "Financial health and fair trade.")
        energy  = self._upsert_topic(method, "Energy",         env,   "Energy consumption and renewables.")
        water   = self._upsert_topic(method, "Water",          env,   "Water use and discharge.")
        labour  = self._upsert_topic(method, "Labour Rights",  soc,   "Fair wages, health & safety.")
        div     = self._upsert_topic(method, "Diversity & Inclusion", soc, "Gender, age and disability inclusion.")
        supply  = self._upsert_topic(method, "Supply Chain",   econ,  "Supplier assessment and payments.")
        innov   = self._upsert_topic(method, "Innovation",     econ,  "R&D investment and new products.")

        # ---- Stakeholder groups -------------------------------------------
        self.stdout.write("  Creating stakeholder groups…")
        sg_employees, _ = StakeholderGroup.objects.get_or_create(name="Employees",  defaults=dict(description="Organisation employees"))
        sg_customers, _ = StakeholderGroup.objects.get_or_create(name="Customers",  defaults=dict(description="Customers and end-users"))
        sg_suppliers, _ = StakeholderGroup.objects.get_or_create(name="Suppliers",  defaults=dict(description="Tier-1 and Tier-2 suppliers"))
        sg_anyone, _    = StakeholderGroup.objects.get_or_create(name="anyone",     defaults=dict(description="Open to all"))

        # ---- Surveys & Sections -------------------------------------------
        self.stdout.write("  Creating surveys and questions…")
        env_survey  = self._upsert_survey("Environmental Questionnaire",  method, sg_employees)
        soc_survey  = self._upsert_survey("Social Questionnaire",         method, sg_employees)
        econ_survey = self._upsert_survey("Economic Questionnaire",       method, sg_anyone)

        # Sections per survey
        env_sec1 = self._upsert_section(env_survey, 1, "Energy & Emissions")
        env_sec2 = self._upsert_section(env_survey, 2, "Water & Waste")
        soc_sec1 = self._upsert_section(soc_survey, 1, "Working Conditions")
        soc_sec2 = self._upsert_section(soc_survey, 2, "Diversity")
        ec_sec1  = self._upsert_section(econ_survey, 1, "Supply Chain")
        ec_sec2  = self._upsert_section(econ_survey, 2, "Innovation & R&D")

        # ---- Answer options -----------------------------------------------
        yes_no = self._upsert_options(["Yes", "No"])
        freq   = self._upsert_options(["Never", "Rarely", "Sometimes", "Often", "Always"])
        satis  = self._upsert_options(["Very dissatisfied", "Dissatisfied", "Neutral", "Satisfied", "Very satisfied"])
        agree  = self._upsert_options(["Strongly disagree", "Disagree", "Neutral", "Agree", "Strongly agree"])

        # ---- Direct Indicators & Questions --------------------------------
        # Environment
        di_energy_kwh     = self._upsert_di(method, "ENV_E1", "Total energy consumption (kWh)", "integer", energy, "")
        di_renewable_pct  = self._upsert_di(method, "ENV_E2", "Share of renewable energy (%)", "double",  energy, "")
        di_co2_tonnes     = self._upsert_di(method, "ENV_E3", "CO₂ emissions (metric tonnes)", "double",  energy, "")
        di_water_m3       = self._upsert_di(method, "ENV_W1", "Water consumption (m³)", "integer", water,  "")
        di_waste_recycle  = self._upsert_di(method, "ENV_W2", "Waste recycling rate (%)", "double",  water,  "")

        # Social
        di_female_pct     = self._upsert_di(method, "SOC_D1", "Female employees (%)", "double",    div,    "")
        di_safety_inc     = self._upsert_di(method, "SOC_L1", "Work-related incidents (count)", "integer", labour, "")
        di_training_hrs   = self._upsert_di(method, "SOC_L2", "Average training hours per employee", "double", labour, "")
        di_wellbeing      = self._upsert_di(method, "SOC_L3", "Employee wellbeing satisfaction", "singlechoice", labour, "", options=satis)

        # Economic
        di_local_supp_pct = self._upsert_di(method, "ECO_S1", "Local suppliers (%)", "double",    supply, "")
        di_rd_invest      = self._upsert_di(method, "ECO_I1", "R&D investment (% of revenue)", "double", innov, "")
        di_certifications = self._upsert_di(method, "ECO_I2", "Has ISO 14001 certification", "singlechoice", innov, "", options=yes_no)

        # ---- Questions (linked to sections) --------------------------------
        q_energy_kwh    = self._upsert_question(method, env_sec1, energy, di_energy_kwh,    1, "How many kWh of energy did your organisation consume last year?",      "Number", "field")
        q_renewable     = self._upsert_question(method, env_sec1, energy, di_renewable_pct, 2, "What percentage of your energy came from renewable sources?",          "Number", "field")
        q_co2           = self._upsert_question(method, env_sec1, energy, di_co2_tonnes,    3, "What were your total CO₂ equivalent emissions in metric tonnes?",       "Number", "field")
        q_water         = self._upsert_question(method, env_sec2, water,  di_water_m3,      1, "Total water consumed (m³)?",                                           "Number", "field")
        q_waste_rec     = self._upsert_question(method, env_sec2, water,  di_waste_recycle, 2, "What percentage of your waste is recycled or composted?",              "Number", "field")

        q_female_pct    = self._upsert_question(method, soc_sec2, div,    di_female_pct,    1, "What percentage of your workforce identifies as female?",              "Number", "field")
        q_safety_inc    = self._upsert_question(method, soc_sec1, labour, di_safety_inc,    1, "How many work-related incidents occurred last year?",                  "Number", "field")
        q_training      = self._upsert_question(method, soc_sec1, labour, di_training_hrs,  2, "On average, how many training hours did each employee receive?",       "Number", "field")
        q_wellbeing     = self._upsert_question(method, soc_sec1, labour, di_wellbeing,     3, "How would you rate the general wellbeing in your organisation?",       "Radio",  "radiobutton", options=satis)

        q_local_supp    = self._upsert_question(method, ec_sec1,  supply, di_local_supp_pct,1, "What percentage of your suppliers are based locally (within 500 km)?", "Number", "field")
        q_rd            = self._upsert_question(method, ec_sec2,  innov,  di_rd_invest,     1, "What share of your revenue was invested in R&D last year (%)?",       "Number", "field")
        q_iso14001      = self._upsert_question(method, ec_sec2,  innov,  di_certifications,2, "Does your organisation hold an ISO 14001 certification?",             "Radio",  "radiobutton", options=yes_no)

        # ---- Indirect Indicators ------------------------------------------
        self.stdout.write("  Creating indirect indicators…")
        self._upsert_ii(method, "ENV_SCORE",  energy, "Environmental Score",  "[ENV_E2] * 0.4 + (100 - [ENV_E3]) * 0.3 + [ENV_W2] * 0.3", "double", "scoring")
        self._upsert_ii(method, "SOC_SCORE",  labour, "Social Score",         "[SOC_D1] * 0.3 + (100 - [SOC_L1]*5) * 0.4 + [SOC_L2] * 0.3", "double", "scoring")
        self._upsert_ii(method, "ESEA_TOTAL", econ,   "ESEA Overall Score",   "([ENV_SCORE] + [SOC_SCORE]) / 2", "double", "scoring")

        # ---- Network ------------------------------------------------------
        self.stdout.write("  Creating network…")
        network, created = Network.objects.get_or_create(
            name="European SME Sustainability Network",
            defaults=dict(
                owner=admin,
                created_by=admin,
                ispublic=True,
                description="Pan-European network supporting SME ESEA reporting and certification.",
            )
        )
        if created:
            # Admin is automatically added by NetworkManager; add felix as auditor
            NetworkMember.objects.get_or_create(
                network=network, user=felix,
                defaults=dict(role=NetworkMember.AUDITOR, invitation="accepted")
            )
        network.methods.add(method)

        # Memberships
        for org in [verdant, nexo, circle, solis, biomats]:
            network.organisations.add(org)
            Membership.objects.get_or_create(
                network=network, organisation=org,
                defaults=dict(status="accepted", join_date=now() - timedelta(days=random.randint(30, 400)), requester="network")
            )

        # ---- Campaigns, ESEA Accounts, Respondents & Survey Responses ------
        # One campaign per year (2022-2025), one primary reporter per org.
        # This ensures each indicator has exactly one data point per year —
        # preventing the summing-across-respondents issue in dashboard charts.
        self.stdout.write("  Creating campaign and ESEA accounts…")

        domains = {
            verdant:  ("verdantcorp.com",   alice),
            nexo:     ("nexocraft.de",      bob),
            circle:   ("circlegoods.dk",    caro),
            solis:    ("solisgroup.fr",     diana),
            biomats:  ("biomaterialspl.com",evan),
        }

        surveys = [env_survey, soc_survey, econ_survey]
        reporting_years = [2022, 2023, 2024, 2025]

        self.stdout.write("  Creating respondents and survey responses…")
        for yr in reporting_years:
            campaign_name = f"Annual ESEA Report {yr}"
            is_current = (yr == 2025)
            campaign, _ = Campaign.objects.get_or_create(
                name=campaign_name,
                defaults=dict(
                    created_by=admin,
                    network=network,
                    method=method,
                    required=True,
                    year=yr,
                    open_survey_date=now() - timedelta(days=(2025 - yr) * 365 + 60),
                    close_survey_date=now() - timedelta(days=(2025 - yr) * 365 - 30),
                    auditstatus="Audits in Progress" if is_current else "Audited",
                )
            )

            for org in [verdant, nexo, circle, solis, biomats]:
                domain, owner = domains[org]
                account, _ = EseaAccount.objects.get_or_create(
                    organisation=org,
                    campaign=campaign,
                    defaults=dict(
                        method=method,
                        year=yr,
                        deployed_to_respondents=True,
                        sufficient_responses=True,
                        response_rate="78.50",
                    )
                )
                # The Campaign post_save signal creates EseaAccounts with the
                # DEFAULT year (current year). Force-correct via queryset update
                # (bypasses post_save to avoid duplicate accountant respondents).
                EseaAccount.objects.filter(pk=account.pk).update(
                    year=yr,
                    deployed_to_respondents=True,
                    sufficient_responses=True,
                )

                # One primary reporter per org (the owner) — avoids multi-respondent summing
                reporter_email = f"reporter.{yr}@{domain}"
                reporter_fn = owner.first_name
                reporter_ln = owner.last_name
                reporter_pfx = owner.last_name_prefix
                respondent, _ = Respondent.objects.get_or_create(
                    organisation=org,
                    email=reporter_email,
                    defaults=dict(
                        first_name=reporter_fn,
                        last_name_prefix=reporter_pfx,
                        last_name=reporter_ln,
                    )
                )

                for survey in surveys:
                    sr, created = SurveyResponse.objects.get_or_create(
                        survey=survey,
                        respondent=respondent,
                        esea_account=account,
                        defaults=dict(finished=True)
                    )
                    if created:
                        sr.finished = True
                        sr.save()
                        self._fill_responses(sr, org, yr)

        self._seed_dashboards(method)
        self.stdout.write(self.style.SUCCESS("=== Seeding complete! ==="))

    # -----------------------------------------------------------------------
    # Dashboard seeding
    # -----------------------------------------------------------------------

    def _seed_dashboards(self, method):
        self.stdout.write("  Creating dashboards…")
        method_id = method.id

        # ── coordinate helpers ──────────────────────────────────────────────
        # CSS mapping: left=X Start%, right=(100-X End)%, bottom=Y Start%, top=(100-Y End)%
        def pos(x0, x1, y0, y1):
            return {"X Start": x0, "X End": x1, "Y Start": y0, "Y End": y1}

        def ifield(key, name):
            return {"Indicator": key, "Name": name, "Filters": []}

        # Each vis_ helper accepts an optional sub-position within its container (0-100).
        # This lets multiple visualisations share one coloured container panel.
        def vis_single(title, key, label, x0=0, x1=100, y0=0, y1=100):
            return {
                "Title": title,
                "Position": pos(x0, x1, y0, y1),
                "DataDisplay": {
                    "Type": "Single Value Display",
                    "Sideways": False,
                    "Options": {},
                    "DataConfiguration": {
                        "Value Field": ifield(key, label),
                        "Filters": [], "Category Limit": 0,
                    },
                },
            }

        def vis_radial(title, key, label, x0=0, x1=100, y0=0, y1=100):
            return {
                "Title": title,
                "Position": pos(x0, x1, y0, y1),
                "DataDisplay": {
                    "Type": "Radial Progress Bar",
                    "Sideways": False,
                    "Options": {"ShowValue": True, "isPercentage": True},
                    "DataConfiguration": {
                        "Current Value Field": ifield(key, label),
                        "Target Value Field": ifield(key, label),
                        "Filters": [], "Category Limit": 0,
                    },
                },
            }

        def vis_progress(title, key, label, x0=0, x1=100, y0=0, y1=100):
            return {
                "Title": title,
                "Position": pos(x0, x1, y0, y1),
                "DataDisplay": {
                    "Type": "Progress Bar",
                    "Sideways": False,
                    "Options": {"isPercentage": True},
                    "DataConfiguration": {
                        "Current Value Field": ifield(key, label),
                        "Target Value Field": ifield(key, label),
                        "Filters": [], "Category Limit": 0,
                    },
                },
            }

        def container(bg, visualisations, x0, x1, y0, y1):
            return {
                "Title": "",
                "Position": pos(x0, x1, y0, y1),
                "Style": {"Background Color": bg},
                "Images": [],
                "TextParagraphs": [],
                "Visualisations": visualisations,
            }

        def overview(name, containers):
            return {
                "Name": name,
                "HeadSection": {
                    "Title": name, "Text": "",
                    "OverviewSelection": True, "Data Filters": [],
                    "Visualisation": None, "Download Button": False, "Position": None,
                },
                "BodySection": {"Position": None, "Containers": containers},
                "SidePanel": {"OverviewSelection": None, "Data Filters": []},
                "Filters": [], "Style": {"Background Color": None},
            }

        # ── chart helpers (use Year as category axis for bar/line/pie/table) ──
        YEAR_FIELD = {"Named Field": "Year", "Name": "Year"}

        def vis_bar(title, key, label, x0=0, x1=100, y0=0, y1=100, sideways=False):
            return {
                "Title": title,
                "Position": pos(x0, x1, y0, y1),
                "DataDisplay": {
                    "Type": "Bar Chart",
                    "Sideways": sideways,
                    "Options": {"Sideways": sideways},
                    "DataConfiguration": {
                        "Value Field": ifield(key, label),
                        "Category Field": YEAR_FIELD,
                        "Filters": [], "Category Limit": 0,
                    },
                },
            }

        def vis_line(title, key, label, x0=0, x1=100, y0=0, y1=100):
            return {
                "Title": title,
                "Position": pos(x0, x1, y0, y1),
                "DataDisplay": {
                    "Type": "Line Chart",
                    "Sideways": False,
                    "Options": {},
                    "DataConfiguration": {
                        "Value Field": ifield(key, label),
                        "Category Field": YEAR_FIELD,
                        "Filters": [], "Category Limit": 0,
                    },
                },
            }

        def vis_pie(title, key, label, x0=0, x1=100, y0=0, y1=100):
            return {
                "Title": title,
                "Position": pos(x0, x1, y0, y1),
                "DataDisplay": {
                    "Type": "Pie Chart",
                    "Sideways": False,
                    "Options": {},
                    "DataConfiguration": {
                        "Value Field": ifield(key, label),
                        "Category Field": YEAR_FIELD,
                        "Filters": [], "Category Limit": 0,
                    },
                },
            }

        def vis_frac(title, frac_key, frac_label, total_key, total_label, x0=0, x1=100, y0=0, y1=100):
            return {
                "Title": title,
                "Position": pos(x0, x1, y0, y1),
                "DataDisplay": {
                    "Type": "Fractional Value Display",
                    "Sideways": False,
                    "Options": {},
                    "DataConfiguration": {
                        "Fractional Value Field": ifield(frac_key, frac_label),
                        "Total Value Field": ifield(total_key, total_label),
                        "Filters": [], "Category Limit": 0,
                    },
                },
            }

        # ── colour tokens ───────────────────────────────────────────────────
        DARK  = "#263238"   # dark blue-grey hero
        DKGRN = "#1b5e20"   # dark green hero
        DKBLU = "#1a237e"   # dark navy
        WHT   = "#ffffff"
        LGRY  = "#f5f5f5"
        MGRY  = "#eceff1"
        LBLU  = "#e3f2fd"
        LGRN  = "#e8f5e9"
        TEAL  = "#e0f7fa"
        AMB   = "#fff8e1"
        ROSE  = "#fce4ec"
        PURP  = "#f3e5f5"
        CYAN  = "#e0f2f1"
        IND   = "#e8eaf6"
        ORG   = "#fff3e0"
        LIME  = "#f9fbe7"

        # ===================================================================
        # Dashboard 1 — "Energy & Climate"
        # Inspired by Envizi: dark left hero + central gauge + right KPI stack
        # ===================================================================
        # Body layout (75 % screen height):
        #  ┌─────────────┬────────────────────┬─────────────┐
        #  │ dark hero   │  large radial ring │  right KPIs │
        #  │ 2 stacked   │  Renewable %       │  Water m³   │
        #  │ kWh + CO₂   │                    │  + Recycl.% │
        #  └─────────────┴────────────────────┴─────────────┘
        ec_spec = {
            "Name": "Energy & Climate",
            "Methods": [method_id],
            "Style": {"Background Color": None},
            "Overviews": [
                overview("Summary", [
                    # Left dark hero panel — two stacked KPIs inside one container
                    container(DARK, [
                        vis_single("Energy Consumption",  "ENV_E1", "kWh",     x0=2, x1=98, y0=53, y1=97),
                        vis_single("CO₂ Emissions",       "ENV_E3", "t CO₂e",  x0=2, x1=98, y0=3,  y1=47),
                    ], 1, 30, 2, 98),
                    # Centre — prominent radial gauge
                    container(WHT, [
                        vis_radial("Renewable Energy Share", "ENV_E2", "Renewable %"),
                    ], 32, 68, 2, 98),
                    # Right light panel — water + recycling stacked
                    container(MGRY, [
                        vis_single("Water Consumption",   "ENV_W1", "m³",       x0=2, x1=98, y0=53, y1=97),
                        vis_progress("Waste Recycled",    "ENV_W2", "Recycled %", x0=2, x1=98, y0=3, y1=47),
                    ], 70, 99, 2, 98),
                ]),
                overview("Environmental Detail", [
                    container(LBLU, [
                        vis_radial("Renewable Energy", "ENV_E2", "Renewable %"),
                    ], 1, 48, 2, 98),
                    container(TEAL, [
                        vis_progress("Waste Recycling Rate", "ENV_W2", "Recycled %"),
                    ], 52, 99, 2, 98),
                ]),
            ],
        }

        # ===================================================================
        # Dashboard 2 — "Social Workforce Dashboard"
        # Inspired by Greenbase: dark bg with radials + adjacent KPI numbers
        # ===================================================================
        # Overview 1 layout:
        #  ┌──────────┬────────────────────────┬──────────┐
        #  │ gender   │ Training hrs   │Incident│  Local   │
        #  │ radial   │ (top half)     │(bottom)│ suppl.%  │
        #  └──────────┴────────────────────────┴──────────┘
        sw_spec = {
            "Name": "Social Workforce Dashboard",
            "Methods": [method_id],
            "Style": {"Background Color": None},
            "Overviews": [
                overview("Workforce at a Glance", [
                    container(ROSE, [
                        vis_radial("Female Employees", "SOC_D1", "Female %"),
                    ], 1, 25, 2, 98),
                    container(MGRY, [
                        vis_single("Avg Training Hours", "SOC_L2", "h / employee", x0=2, x1=98, y0=53, y1=97),
                        vis_single("Work Incidents",     "SOC_L1", "incidents",    x0=2, x1=98, y0=3,  y1=47),
                    ], 27, 74, 2, 98),
                    container(CYAN, [
                        vis_progress("Local Suppliers", "ECO_S1", "Local %"),
                    ], 76, 99, 2, 98),
                ]),
                overview("Safety & Innovation", [
                    # Dark left — big incident counter (striking hero number)
                    container(DKBLU, [
                        vis_single("Work-Related Incidents", "SOC_L1", "incidents"),
                    ], 1, 30, 2, 98),
                    # Centre — R&D Investment
                    container(IND, [
                        vis_single("R&D Investment", "ECO_I1", "% of revenue"),
                    ], 32, 65, 2, 98),
                    # Right — local supplier radial
                    container(LGRN, [
                        vis_radial("Local Supplier Share", "ECO_S1", "Local %"),
                    ], 67, 99, 2, 98),
                ]),
            ],
        }

        # ===================================================================
        # Dashboard 3 — "Sustainability Scorecard"
        # Inspired by RIMM: large score gauge left + stacked progress bars right
        # ===================================================================
        # Overview 1 layout:
        #  ┌──────────────┬──────────────────────────────────┐
        #  │ big radial   │ ── Renewable Energy % ─── 68 %  │  top row
        #  │ Renewable %  │ ── Waste Recycling % ──── 72 %  │  mid row
        #  │ (hero gauge) │ ── Female Employees % ─── 54 %  │  bot row
        #  └──────────────┴──────────────────────────────────┘
        # Overview 2 layout — 4-cell metrics grid:
        #  ┌──────────┬──────────┬──────────┬──────────┐
        #  │ Energy   │  Water   │  CO₂     │ Training │
        #  └──────────┴──────────┴──────────┴──────────┘
        sc_spec = {
            "Name": "Sustainability Scorecard",
            "Methods": [method_id],
            "Style": {"Background Color": None},
            "Overviews": [
                overview("KPI Overview", [
                    # Left: hero radial gauge (dark green tint)
                    container(LGRN, [
                        vis_radial("Renewable Energy\n(Environmental Proxy Score)", "ENV_E2", "Renewable %"),
                    ], 1, 32, 2, 98),
                    # Right: 3 stacked progress bars (scorecard rows)
                    container(WHT, [
                        vis_progress("Renewable Energy %",  "ENV_E2", "Renewable %",   x0=2, x1=98, y0=68, y1=97),
                        vis_progress("Waste Recycling %",   "ENV_W2", "Recycled %",    x0=2, x1=98, y0=35, y1=64),
                        vis_progress("Female Employees %",  "SOC_D1", "Female %",      x0=2, x1=98, y0=2,  y1=31),
                    ], 34, 99, 2, 98),
                ]),
                overview("Metrics at a Glance", [
                    container(LBLU, [
                        vis_single("Energy Consumption", "ENV_E1", "kWh"),
                    ], 1, 24, 2, 98),
                    container(TEAL, [
                        vis_single("Water Consumption",  "ENV_W1", "m³"),
                    ], 26, 49, 2, 98),
                    container(AMB, [
                        vis_single("CO₂ Emissions",      "ENV_E3", "t CO₂e"),
                    ], 51, 74, 2, 98),
                    container(LGRN, [
                        vis_single("Avg Training Hours", "SOC_L2", "h / employee"),
                    ], 76, 99, 2, 98),
                ]),
            ],
        }

        for spec in [ec_spec, sw_spec, sc_spec]:
            if not Dashboard.objects.filter(specification__Name=spec["Name"]).exists():
                Dashboard.objects.create(specification=spec)

        # ===================================================================
        # Dashboard 4 — "Accuvio Resource Overview"
        # Inspired by Accuvio: central bar chart + pie (top) + progress row (bottom)
        # ===================================================================
        acc_spec = {
            "Name": "Accuvio Resource Overview",
            "Methods": [method_id],
            "Style": {"Background Color": None},
            "Overviews": [
                overview("Resource Breakdown", [
                    # Top half: wide bar chart left, pie right
                    container(WHT,  [vis_bar("Energy Consumption by Year",     "ENV_E1", "kWh")],        1, 65, 52, 98),
                    container(LGRY, [vis_pie("Waste Recycled",                 "ENV_W2", "Recycled %")], 67, 99, 52, 98),
                    # Bottom half: 3 indicators
                    container(TEAL, [vis_progress("Water Recycling",           "ENV_W2", "Recycled %")], 1,  31, 2,  48),
                    container(LGRN, [vis_progress("Local Suppliers",           "ECO_S1", "Local %")],    33, 65, 2,  48),
                    container(ROSE, [vis_radial("Gender Diversity",            "SOC_D1", "Female %")],   67, 99, 2,  48),
                ]),
                overview("Environmental Detail", [
                    container(LBLU, [vis_bar("Energy (kWh) by Year",           "ENV_E1", "kWh")],        1,  48, 2, 98),
                    container(AMB,  [vis_bar("CO₂ Emissions by Year",          "ENV_E3", "t CO₂e")],    52, 99, 2, 98),
                ]),
            ],
        }

        # ===================================================================
        # Dashboard 5 — "Apambu Sustainability Rows"
        # Inspired by Apambu: stacked rows of big KPI + donut pairs
        # ===================================================================
        apa_spec = {
            "Name": "Apambu Sustainability Rows",
            "Methods": [method_id],
            "Style": {"Background Color": None},
            "Overviews": [
                overview("Resource Consumption", [
                    # Row 1 — Energy (top)
                    container(LBLU, [vis_single("Annual Energy",     "ENV_E1", "kWh")],          1,  47, 75, 98),
                    container(TEAL, [vis_radial("Renewable Energy",  "ENV_E2", "Renewable %")],  51, 99, 75, 98),
                    # Row 2 — Water
                    container(CYAN, [vis_single("Water Consumed",    "ENV_W1", "m³")],            1,  47, 50, 73),
                    container(LGRN, [vis_progress("Waste Recycled",  "ENV_W2", "Recycled %")],   51, 99, 50, 73),
                    # Row 3 — Labour
                    container(AMB,  [vis_single("Training Hours",    "SOC_L2", "h/employee")],   1,  47, 26, 48),
                    container(ROSE, [vis_radial("Female Employees",  "SOC_D1", "Female %")],     51, 99, 26, 48),
                    # Row 4 — Economy
                    container(IND,  [vis_single("R&D Investment",    "ECO_I1", "% revenue")],    1,  47, 2,  23),
                    container(PURP, [vis_progress("Local Suppliers", "ECO_S1", "Local %")],      51, 99, 2,  23),
                ]),
            ],
        }

        # ===================================================================
        # Dashboard 6 — "ArcherIRM Administrator"
        # Inspired by ArcherIRM: large count top-left + bar chart top-right + chart grid bottom
        # ===================================================================
        arim_spec = {
            "Name": "ArcherIRM Administrator",
            "Methods": [method_id],
            "Style": {"Background Color": None},
            "Overviews": [
                overview("Administrator Overview", [
                    # Top: big count number + bar chart
                    container(LGRY, [vis_single("Work Incidents",         "SOC_L1", "count")],             1,  28, 55, 98),
                    container(WHT,  [vis_bar("Energy Overview (kWh)",     "ENV_E1", "kWh", sideways=True)], 30, 99, 55, 98),
                    # Bottom: 3 charts
                    container(ROSE, [vis_radial("Gender Diversity",       "SOC_D1", "Female %")],           1,  30, 2,  52),
                    container(TEAL, [vis_progress("Waste Recycling",      "ENV_W2", "Recycled %")],         32, 64, 2,  52),
                    container(LGRN, [vis_bar("Local Supplier %",          "ECO_S1", "Local %", sideways=True)], 66, 99, 2, 52),
                ]),
                overview("Submission Status", [
                    container(LBLU, [vis_single("Work Incidents (Total)", "SOC_L1", "count")],  1,  32, 2, 98),
                    container(AMB,  [vis_single("R&D Investment",         "ECO_I1", "% rev")],  34, 65, 2, 98),
                    container(LGRN, [vis_radial("Renewable Energy",       "ENV_E2", "Renew %")], 67, 99, 2, 98),
                ]),
            ],
        }

        # ===================================================================
        # Dashboard 7 — "Cority Compliance Tracker"
        # Inspired by Cority Air Emissions: 2 radials left + horizontal bar center + singles right
        # ===================================================================
        cor_spec = {
            "Name": "Cority Compliance Tracker",
            "Methods": [method_id],
            "Style": {"Background Color": None},
            "Overviews": [
                overview("Compliance Status", [
                    # Left: 2 stacked radials
                    container(TEAL, [vis_radial("Renewable Energy",  "ENV_E2", "Renew %")],      1,  22, 52, 98),
                    container(LGRN, [vis_radial("Waste Recycled",    "ENV_W2", "Recycled %")],   1,  22, 2,  48),
                    # Center: horizontal bar chart
                    container(WHT,  [vis_bar("Energy by Year",       "ENV_E1", "kWh", sideways=True)], 24, 65, 2, 98),
                    # Right: 3 stacked single values
                    container(MGRY, [
                        vis_single("Water m³",       "ENV_W1", "m³",         x0=2, x1=98, y0=68, y1=97),
                        vis_single("CO₂ Emissions",  "ENV_E3", "t CO₂e",     x0=2, x1=98, y0=35, y1=65),
                        vis_single("Training Hrs",   "SOC_L2", "h/employee", x0=2, x1=98, y0=2,  y1=32),
                    ], 67, 99, 2, 98),
                ]),
                overview("Compliance Trends", [
                    container(LBLU, [vis_line("Energy Trend",        "ENV_E1", "kWh")],           1,  48, 2, 98),
                    container(AMB,  [vis_line("CO₂ Trend",           "ENV_E3", "t CO₂e")],       52, 99, 2, 98),
                ]),
            ],
        }

        # ===================================================================
        # Dashboard 8 — "Cority Quality Monitor"
        # Inspired by Cority Data Quality: 2 radials + line charts + bar + table
        # ===================================================================
        cqm_spec = {
            "Name": "Cority Quality Monitor",
            "Methods": [method_id],
            "Style": {"Background Color": None},
            "Overviews": [
                overview("Quality Overview", [
                    # Left: 2 stacked radials
                    container(ROSE, [vis_radial("Female Employees",  "SOC_D1", "Female %")],     1,  22, 52, 98),
                    container(CYAN, [vis_radial("Local Suppliers",   "ECO_S1", "Local %")],      1,  22, 2,  48),
                    # Center-top: horizontal bar chart
                    container(WHT,  [vis_bar("Energy Completeness",  "ENV_E1", "kWh", sideways=True)], 24, 65, 52, 98),
                    # Center-bottom: line chart
                    container(LGRY, [vis_line("Training Trend",      "SOC_L2", "h/emp")],        24, 65, 2,  48),
                    # Right: 2 singles
                    container(AMB,  [
                        vis_single("CO₂ Tonnes",     "ENV_E3", "t CO₂e",  x0=2, x1=98, y0=52, y1=97),
                        vis_single("Water m³",       "ENV_W1", "m³",       x0=2, x1=98, y0=2,  y1=48),
                    ], 67, 99, 2, 98),
                ]),
            ],
        }

        # ===================================================================
        # Dashboard 9 — "Deloitte Emissions Executive"
        # Inspired by Deloitte/Workday: pie + KPIs left, large bar chart right
        # ===================================================================
        del_spec = {
            "Name": "Deloitte Emissions Executive",
            "Methods": [method_id],
            "Style": {"Background Color": None},
            "Overviews": [
                overview("Executive Overview", [
                    # Left column: pie + single KPI
                    container(LGRY, [vis_pie("Energy Mix by Year",  "ENV_E1", "kWh")],         1,  28, 52, 98),
                    container(AMB,  [vis_single("CO₂ Emissions",    "ENV_E3", "t CO₂e")],     1,  28, 2,  48),
                    # Centre: 3 stacked KPI boxes
                    container(MGRY, [
                        vis_single("Total Energy",   "ENV_E1", "kWh",      x0=2, x1=98, y0=68, y1=97),
                        vis_single("Water Consumed", "ENV_W1", "m³",       x0=2, x1=98, y0=35, y1=65),
                        vis_single("R&D Invest.",    "ECO_I1", "% rev",    x0=2, x1=98, y0=2,  y1=32),
                    ], 30, 65, 2, 98),
                    # Right: large bar chart
                    container(WHT,  [vis_bar("CO₂ Emissions by Year", "ENV_E3", "t CO₂e")],  67, 99, 2, 98),
                ]),
                overview("Scope Breakdown", [
                    container(TEAL, [vis_pie("Energy by Year",       "ENV_E1", "kWh")],        1,  48, 2, 98),
                    container(LGRN, [vis_pie("Water by Year",        "ENV_W1", "m³")],         52, 99, 2, 98),
                ]),
            ],
        }

        # ===================================================================
        # Dashboard 10 — "Diligent GHG Analytics"
        # Inspired by Diligent: 2 pie charts left + large bar chart right
        # ===================================================================
        dil_spec = {
            "Name": "Diligent GHG Analytics",
            "Methods": [method_id],
            "Style": {"Background Color": None},
            "Overviews": [
                overview("GHG Summary", [
                    # Left: 2 pie charts stacked
                    container(LGRY, [vis_pie("Energy Mix",           "ENV_E1", "kWh")],        1,  44, 52, 98),
                    container(MGRY, [vis_pie("Emissions by Year",    "ENV_E3", "t CO₂e")],    1,  44, 2,  48),
                    # Right: large bar chart
                    container(WHT,  [vis_bar("CO₂ Emissions by Year","ENV_E3", "t CO₂e")],   46, 99, 2, 98),
                ]),
                overview("Emissions Detail", [
                    container(AMB,  [vis_bar("Energy (kWh)",         "ENV_E1", "kWh")],        1,  32, 2, 98),
                    container(TEAL, [vis_bar("Water (m³)",           "ENV_W1", "m³")],         34, 65, 2, 98),
                    container(ROSE, [vis_bar("CO₂ (t)",              "ENV_E3", "t CO₂e")],   67, 99, 2, 98),
                ]),
            ],
        }

        # ===================================================================
        # Dashboard 11 — "Envizi Utility Performance"
        # Inspired by Envizi Utility: dark theme, large central bar chart, right KPI stack
        # ===================================================================
        eup_spec = {
            "Name": "Envizi Utility Performance",
            "Methods": [method_id],
            "Style": {"Background Color": None},
            "Overviews": [
                overview("Utility Summary", [
                    # Wide central bar chart (dark bg)
                    container(DARK, [vis_bar("Electricity Consumption (kWh)", "ENV_E1", "kWh")], 1,  65, 2, 98),
                    # Right: 3 stacked KPIs
                    container(MGRY, [
                        vis_single("Water Consumption", "ENV_W1", "m³",        x0=2, x1=98, y0=68, y1=97),
                        vis_single("CO₂ Emissions",     "ENV_E3", "t CO₂e",   x0=2, x1=98, y0=35, y1=65),
                        vis_single("R&D Investment",    "ECO_I1", "% revenue", x0=2, x1=98, y0=2,  y1=32),
                    ], 67, 99, 2, 98),
                ]),
                overview("Utility Trends", [
                    container(LBLU, [vis_bar("Energy Trend",    "ENV_E1", "kWh", sideways=True)],  1,  48, 2, 98),
                    container(CYAN, [vis_bar("Water Trend",     "ENV_W1", "m³",  sideways=True)], 52, 99, 2, 98),
                ]),
            ],
        }

        # ===================================================================
        # Dashboard 12 — "Envizi Net Zero Pathway"
        # Inspired by Envizi Market-Based: dark hero KPI left, bar chart + breakdown right
        # ===================================================================
        enp_spec = {
            "Name": "Envizi Net Zero Pathway",
            "Methods": [method_id],
            "Style": {"Background Color": None},
            "Overviews": [
                overview("Pathway Overview", [
                    # Left dark hero: CO₂ KPI (the "3.60M" style large number)
                    container(DKBLU, [vis_single("CO₂ Emissions", "ENV_E3", "t CO₂e")],          1,  30, 2, 98),
                    # Right top: energy bar chart
                    container(WHT,   [vis_bar("Electricity Consumption", "ENV_E1", "kWh")],      32, 99, 52, 98),
                    # Right bottom: water bar chart
                    container(TEAL,  [vis_bar("Water Consumption", "ENV_W1", "m³")],             32, 99, 2,  48),
                ]),
                overview("Reduction Targets", [
                    container(AMB,  [vis_radial("Renewable Energy Target", "ENV_E2", "Renew %")], 1,  32, 2, 98),
                    container(LGRN, [vis_radial("Recycling Target",        "ENV_W2", "Recycled %")], 34, 65, 2, 98),
                    container(ROSE, [vis_radial("Gender Diversity Target", "SOC_D1", "Female %")], 67, 99, 2, 98),
                ]),
            ],
        }

        # ===================================================================
        # Dashboard 13 — "ESGBook Score Analytics"
        # Inspired by ESGBook: dual left radials + right line/bar chart for trends
        # ===================================================================
        esg_spec = {
            "Name": "ESGBook Score Analytics",
            "Methods": [method_id],
            "Style": {"Background Color": None},
            "Overviews": [
                overview("ESG Scores", [
                    # Left: 2 stacked radials (score indicators)
                    container(TEAL, [vis_radial("Renewable Energy",  "ENV_E2", "Renew %")],    1,  32, 52, 98),
                    container(ROSE, [vis_radial("Female Employees",  "SOC_D1", "Female %")],   1,  32, 2,  48),
                    # Right: line chart for energy trend
                    container(WHT,  [vis_line("Energy Trend by Year", "ENV_E1", "kWh")],       34, 99, 2,  98),
                ]),
                overview("Score Detail", [
                    container(LGRN, [vis_radial("Local Suppliers",   "ECO_S1", "Local %")],    1,  32, 52, 98),
                    container(IND,  [vis_radial("Waste Recycling",   "ENV_W2", "Recycled %")], 1,  32, 2,  48),
                    container(AMB,  [vis_line("CO₂ Trend",           "ENV_E3", "t CO₂e")],    34, 99, 2,  98),
                ]),
            ],
        }

        # ===================================================================
        # Dashboard 14 — "Measurabl Data Cards"
        # Inspired by Measurabl: 4-column grid of card tiles (KPI + chart per card)
        # ===================================================================
        meas_spec = {
            "Name": "Measurabl Data Cards",
            "Methods": [method_id],
            "Style": {"Background Color": None},
            "Overviews": [
                overview("Environmental Cards", [
                    # Card 1 — Energy: single value top half, bar chart bottom half
                    container(LBLU, [
                        vis_single("Energy (kWh)", "ENV_E1", "kWh",         x0=2, x1=98, y0=52, y1=97),
                        vis_bar("Energy by Year",  "ENV_E1", "kWh",         x0=2, x1=98, y0=2,  y1=48),
                    ], 1,  24, 2, 98),
                    # Card 2 — Water
                    container(TEAL, [
                        vis_single("Water (m³)",   "ENV_W1", "m³",          x0=2, x1=98, y0=52, y1=97),
                        vis_bar("Water by Year",   "ENV_W1", "m³",          x0=2, x1=98, y0=2,  y1=48),
                    ], 26, 49, 2, 98),
                    # Card 3 — CO₂
                    container(AMB,  [
                        vis_single("CO₂ (t)",      "ENV_E3", "t CO₂e",     x0=2, x1=98, y0=52, y1=97),
                        vis_bar("CO₂ by Year",     "ENV_E3", "t CO₂e",     x0=2, x1=98, y0=2,  y1=48),
                    ], 51, 74, 2, 98),
                    # Card 4 — Renewables
                    container(LGRN, [
                        vis_radial("Renewable %",  "ENV_E2", "Renew %",    x0=2, x1=98, y0=52, y1=97),
                        vis_progress("Recycled %", "ENV_W2", "Recycled %", x0=2, x1=98, y0=2,  y1=48),
                    ], 76, 99, 2, 98),
                ]),
                overview("Social Cards", [
                    container(ROSE, [
                        vis_radial("Female %",     "SOC_D1", "Female %",   x0=2, x1=98, y0=52, y1=97),
                        vis_bar("Gender by Year",  "SOC_D1", "Female %",   x0=2, x1=98, y0=2,  y1=48),
                    ], 1,  32, 2, 98),
                    container(ORG,  [
                        vis_single("Incidents",    "SOC_L1", "count",       x0=2, x1=98, y0=52, y1=97),
                        vis_bar("Incidents/Year",  "SOC_L1", "count",       x0=2, x1=98, y0=2,  y1=48),
                    ], 34, 65, 2, 98),
                    container(LGRN, [
                        vis_single("Training Hrs", "SOC_L2", "h/emp",       x0=2, x1=98, y0=52, y1=97),
                        vis_bar("Training/Year",   "SOC_L2", "h/emp",       x0=2, x1=98, y0=2,  y1=48),
                    ], 67, 99, 2, 98),
                ]),
            ],
        }

        # ===================================================================
        # Dashboard 15 — "Navex ESG Analytics"
        # Inspired by Navex One: top KPI strip + 3×2 chart grid below
        # ===================================================================
        nav_spec = {
            "Name": "Navex ESG Analytics",
            "Methods": [method_id],
            "Style": {"Background Color": None},
            "Overviews": [
                overview("ESG Analytics", [
                    # Top KPI strip (4 boxes)
                    container(LGRY, [vis_single("Energy kWh",   "ENV_E1", "kWh")],        1,  24, 85, 98),
                    container(TEAL, [vis_single("CO₂ Tonnes",   "ENV_E3", "t CO₂e")],   26, 49, 85, 98),
                    container(ROSE, [vis_single("Incidents",    "SOC_L1", "count")],      51, 74, 85, 98),
                    container(LGRN, [vis_single("Training Hrs", "SOC_L2", "h/emp")],      76, 99, 85, 98),
                    # Middle row: 3 charts
                    container(LBLU, [vis_pie("Energy Mix",      "ENV_E1", "kWh")],        1,  32, 44, 83),
                    container(AMB,  [vis_bar("Renewable %",     "ENV_E2", "Renew %")],   34, 65, 44, 83),
                    container(PURP, [vis_progress("Local Supp.","ECO_S1", "Local %")],   67, 99, 44, 83),
                    # Bottom row: 3 charts
                    container(ORG,  [vis_radial("Female %",     "SOC_D1", "Female %")],   1,  32, 2,  42),
                    container(CYAN, [vis_bar("Water by Year",   "ENV_W1", "m³")],         34, 65, 2,  42),
                    container(LGRN, [vis_radial("Recycling",    "ENV_W2", "Recycled %")], 67, 99, 2,  42),
                ]),
                overview("Governance Summary", [
                    container(IND,  [vis_single("R&D Investment",  "ECO_I1", "% rev")],    1,  32, 2, 98),
                    container(LGRN, [vis_progress("Local Suppliers","ECO_S1", "Local %")], 34, 65, 2, 98),
                    container(ROSE, [vis_radial("Female Employees", "SOC_D1", "Female %")], 67, 99, 2, 98),
                ]),
            ],
        }

        # ===================================================================
        # Dashboard 16 — "RIMM Topic Scorecard"
        # Inspired by RIMM_Dashboard_Overview_2: large radial hero + 5 stacked progress bars
        # ===================================================================
        rim_spec = {
            "Name": "RIMM Topic Scorecard",
            "Methods": [method_id],
            "Style": {"Background Color": None},
            "Overviews": [
                overview("Topic Progress", [
                    # Left: large radial score proxy
                    container(LGRN, [vis_radial("Renewable Energy\n(Score Proxy)", "ENV_E2", "Renew %")], 1, 30, 2, 98),
                    # Right: 5 stacked progress bars like a scorecard
                    container(WHT, [
                        vis_progress("Renewable Energy %",  "ENV_E2", "Renew %",    x0=2, x1=98, y0=81, y1=98),
                        vis_progress("Waste Recycling %",   "ENV_W2", "Recycled %", x0=2, x1=98, y0=62, y1=79),
                        vis_progress("Female Employees %",  "SOC_D1", "Female %",   x0=2, x1=98, y0=42, y1=59),
                        vis_progress("Local Suppliers %",   "ECO_S1", "Local %",    x0=2, x1=98, y0=22, y1=39),
                        vis_progress("R&D Investment %",    "ECO_I1", "% rev",      x0=2, x1=98, y0=2,  y1=19),
                    ], 32, 99, 2, 98),
                ]),
                overview("Score Details", [
                    container(MGRY, [
                        vis_single("Energy kWh",   "ENV_E1", "kWh",    x0=2, x1=48, y0=52, y1=97),
                        vis_single("Water m³",     "ENV_W1", "m³",     x0=52, x1=98, y0=52, y1=97),
                        vis_single("CO₂ Tonnes",   "ENV_E3", "t CO₂e", x0=2, x1=48, y0=2,  y1=47),
                        vis_single("Incidents",    "SOC_L1", "count",   x0=52, x1=98, y0=2,  y1=47),
                    ], 1, 44, 2, 98),
                    container(WHT, [
                        vis_progress("Renewable %",  "ENV_E2", "Renew %",    x0=2, x1=98, y0=68, y1=97),
                        vis_progress("Recycling %",  "ENV_W2", "Recycled %", x0=2, x1=98, y0=35, y1=65),
                        vis_progress("Gender %",     "SOC_D1", "Female %",   x0=2, x1=98, y0=2,  y1=31),
                    ], 46, 99, 2, 98),
                ]),
            ],
        }

        all_specs = [
            ec_spec, sw_spec, sc_spec,
            acc_spec, apa_spec, arim_spec,
            cor_spec, cqm_spec, del_spec, dil_spec,
            eup_spec, enp_spec, esg_spec,
            meas_spec, nav_spec, rim_spec,
        ]
        for spec in all_specs:
            if not Dashboard.objects.filter(specification__Name=spec["Name"]).exists():
                Dashboard.objects.create(specification=spec)

        self.stdout.write("  Dashboards created.")


    # -----------------------------------------------------------------------
    # Helpers (private)
    # -----------------------------------------------------------------------

    def _upsert_user(self, username, email, first, prefix, last, superuser=False):
        user, created = CustomUser.objects.get_or_create(
            username=username,
            defaults=dict(
                email=email,
                first_name=first,
                last_name_prefix=prefix,
                last_name=last,
                is_staff=superuser,
                is_superuser=superuser,
                password=make_password("openESEA2025!"),
            )
        )
        return user

    def _upsert_org(self, name, owner, description):
        org, created = Organisation.objects.get_or_create(
            name=name,
            defaults=dict(owner=owner, created_by=owner, ispublic=True, description=description)
        )
        if created:
            # OrganisationManager already adds owner as admin via its custom create(),
            # but we used get_or_create with model-level defaults, so add manually.
            OrganisationMember.objects.get_or_create(
                organisation=org, user=owner,
                defaults=dict(role=OrganisationMember.ORGANISATIONADMIN, invitation="accepted")
            )
        return org

    def _upsert_topic(self, method, name, parent, description):
        topic, _ = Topic.objects.get_or_create(
            method=method, name=name,
            defaults=dict(parent_topic=parent, description=description)
        )
        return topic

    def _upsert_survey(self, name, method, stakeholdergroup):
        survey, _ = Survey.objects.get_or_create(
            name=name, method=method,
            defaults=dict(
                stakeholdergroup=stakeholdergroup,
                description=f"Survey for {name}",
                welcome_text="Thank you for participating.",
                closing_text="Your responses are confidential.",
                min_threshold=50,
                response_type="single",
                anonymous=False,
            )
        )
        return survey

    def _upsert_section(self, survey, order, title):
        section, _ = Section.objects.get_or_create(
            survey=survey, order=order,
            defaults=dict(title=title)
        )
        return section

    def _upsert_options(self, texts):
        options = []
        for i, text in enumerate(texts, start=1):
            opt, _ = AnswerOption.objects.get_or_create(text=text.lower(), defaults=dict(order=i))
            options.append(opt)
        return options

    def _upsert_di(self, method, key, name, datatype, topic, description, options=None):
        di, created = DirectIndicator.objects.get_or_create(
            method=method, key=key,
            defaults=dict(name=name, datatype=datatype, topic=topic, description=description)
        )
        if created and options:
            for opt in options:
                di.options.add(opt)
        return di

    def _upsert_ii(self, method, key, topic, name, formula, datatype, itype):
        IndirectIndicator.objects.get_or_create(
            method=method, key=key,
            defaults=dict(topic=topic, name=name, formula=formula, datatype=datatype, type=itype)
        )

    def _upsert_question(self, method, section, topic, di, order, name, answertype, ui, options=None):
        q = Question.objects.filter(method=method, name=name).first()
        if q is None:
            # Use the model's manager.create() which accepts the standard kwargs
            q = Question(
                method=method,
                name=name,
                section=section,
                topic=topic,
                order=order,
                answertype=answertype,
                uiComponent=ui,
                isMandatory=True,
            )
            q.save()
            di.question = q
            di.save(update_fields=["question"])
        return q

    def _fill_responses(self, survey_response, org, year=2025):
        """Create realistic QuestionResponse records for a finished SurveyResponse."""
        survey = survey_response.survey
        for section in survey.sections.prefetch_related("questions").all():
            for question in section.questions.all():
                dis = list(question.direct_indicator.all())
                if not dis:
                    continue
                di = dis[0]
                value = self._realistic_value(di.key, org, year)
                qr = QuestionResponse(
                    survey_response=survey_response,
                    question=question,
                    direct_indicator_id=di.id,
                    value=value,
                    auditstatus="Not Under Audit",
                )
                qr.save()

    # Maps indicator keys to realistic answer generators
    _ORG_PROFILES = {
        "Verdant Corp":               dict(energy=420000, renewable=68, co2=95,  water=3200, recycle=72, female=54, incidents=1, training=18, local_supp=70, rd=4.2, iso=True,  wellbeing=4),
        "Nexocraft GmbH":             dict(energy=890000, renewable=41, co2=210, water=6100, recycle=55, female=38, incidents=3, training=12, local_supp=55, rd=6.8, iso=True,  wellbeing=3),
        "Circle Goods ApS":           dict(energy=230000, renewable=88, co2=42,  water=1800, recycle=91, female=61, incidents=0, training=24, local_supp=82, rd=2.1, iso=False, wellbeing=5),
        "Solis Group SA":             dict(energy=310000, renewable=95, co2=28,  water=2200, recycle=80, female=47, incidents=1, training=30, local_supp=60, rd=8.5, iso=False, wellbeing=4),
        "BioMaterials Sp. z o.o.":    dict(energy=560000, renewable=55, co2=140, water=4400, recycle=63, female=42, incidents=2, training=15, local_supp=45, rd=3.3, iso=True,  wellbeing=3),
    }

    _WELLBEING_LABELS = {1: "very dissatisfied", 2: "dissatisfied", 3: "neutral", 4: "satisfied", 5: "very satisfied"}

    def _realistic_value(self, key, org, year=2025):
        profile = self._ORG_PROFILES.get(org.name, {})
        # Each year since 2022 orgs improve ~3-5 % on sustainability metrics
        years_of_improvement = max(0, year - 2022)
        improve = 1.0 + years_of_improvement * 0.04   # +4 % per year, compounding
        degrade = 1.0 - years_of_improvement * 0.04   # energy/co2/incidents decrease

        def _jitter(v, factor=1.0):
            return str(round(v * factor * random.uniform(0.96, 1.04), 2))

        mapping = {
            # Energy: gradually decreasing (efficiency gains)
            "ENV_E1": _jitter(profile.get("energy", 500000), degrade),
            # Renewables: increasing each year, capped at 99
            "ENV_E2": str(round(min(99, profile.get("renewable", 50) * improve * random.uniform(0.96, 1.04)), 2)),
            # CO2: decreasing
            "ENV_E3": _jitter(profile.get("co2", 120), degrade),
            # Water: slightly decreasing
            "ENV_W1": _jitter(profile.get("water", 3000), degrade),
            # Recycling: increasing, capped at 99
            "ENV_W2": str(round(min(99, profile.get("recycle", 65) * improve * random.uniform(0.96, 1.04)), 2)),
            # Female %: slowly increasing, capped at 70
            "SOC_D1": str(round(min(70, profile.get("female", 45) * (1.0 + years_of_improvement * 0.02) * random.uniform(0.97, 1.03)), 2)),
            # Incidents: decreasing, min 0
            "SOC_L1": str(max(0, profile.get("incidents", 1) - years_of_improvement)),
            # Training: increasing
            "SOC_L2": _jitter(profile.get("training", 16), improve),
            "SOC_L3": self._WELLBEING_LABELS.get(profile.get("wellbeing", 3), "neutral"),
            # Local suppliers: increasing, capped at 95
            "ECO_S1": str(round(min(95, profile.get("local_supp", 55) * improve * random.uniform(0.96, 1.04)), 2)),
            # R&D: increasing
            "ECO_I1": _jitter(profile.get("rd", 3.0), improve),
            "ECO_I2": "yes" if profile.get("iso", False) else "no",
        }
        return mapping.get(key, "")
