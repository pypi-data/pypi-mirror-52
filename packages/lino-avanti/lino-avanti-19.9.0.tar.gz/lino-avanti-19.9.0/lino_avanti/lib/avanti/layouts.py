# -*- coding: UTF-8 -*-
# Copyright 2017 Rumma & Ko Ltd

"""The default :attr:`custom_layouts_module
<lino.core.site.Site.custom_layouts_module>` for Lino Avanti.

"""

from lino.api import dd, rt, _

rt.models.system.SiteConfigs.detail_layout = dd.DetailLayout("""
site_company next_partner_id:10
default_build_method simulate_today
site_calendar default_event_type #pupil_guestrole
max_auto_events hide_events_before
""", size=(60, 'auto'))

rt.models.countries.Places.detail_layout = """
name country
type parent zip_code id
PlacesByPlace contacts.PartnersByCity
"""

rt.models.courses.AllEnrolments.column_names = \
'id #request_date #start_date #end_date #user course \
pupil__birth_date pupil__age pupil__country pupil__city \
pupil__gender state'

dd.update_field(
    rt.models.contacts.Partner, 'language',
    verbose_name=_("Contact language"))

# rt.models.cv.LanguageKnowledgesByPerson.display_mode = 'grid'


rt.models.cv.StudiesByPerson.column_names = 'type content duration_text language school country state education_level remarks *'

rt.models.cv.StudiesByPerson.insert_layout = """
type content
duration_text language
"""

rt.models.cv.Studies.detail_layout = """
person #start_date #end_date duration_text language
type content education_level state #success
school country city
remarks
"""

rt.models.cv.Experiences.detail_layout = """
person company country city
#sector #function title
status duration regime is_training 
#start_date #end_date duration_text termination_reason
remarks
"""

rt.models.cv.ExperiencesByPerson.column_names = "company country duration_text function status termination_reason remarks *"


dd.update_field(
    rt.models.cv.Experience, 'company',
    verbose_name=_("Work area"))

from lino_avanti.lib.avanti.roles import ClientsUser
rt.models.cal.CalendarView.required_roles = dd.login_required(
    ClientsUser)

if dd.is_installed('extensible'):
    rt.models.extensible.CalendarPanel.required_roles = dd.login_required(
        ClientsUser)


from lino_xl.lib.cv.roles import CareerUser
for t in (rt.models.households.SiblingsByPerson,
          rt.models.changes.ChangesByMaster,
          rt.models.households.MembersByHousehold):
    t.required_roles = dd.login_required(CareerUser)
