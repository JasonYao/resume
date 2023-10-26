from json import dumps as json_dumps

from iso639.iso639 import _Language

from ..templating import Templator
from ..templating import TemplateType
from ..templating import TemplatedData
from ..templating import ResumeData
from ..templating import Address
from ..templating import WorkSummary
from ..templating import Education
from ..templating import EducationalOrganizationType


def convert_address(data: Address) -> dict:
    address_locality = data.city
    address_region = data.zone_code
    postal_code = data.postal_code

    val_dict = {
        "@type": "PostalAddress",
        "addressLocality": address_locality,
        "addressRegion": address_region,
        "postalCode": postal_code,
    }

    if data.address_line_1 is not None and data.address_line_2 is not None:
        street_address = f"{data.address_line_1}, {data.address_line_2}"
        val_dict["streetAddress"] = street_address
    return val_dict


def convert_work_summary(work_summary: WorkSummary) -> dict:
    return {
        "@type": "OrganizationRole",
        "alumniOf": {
            "@type": work_summary.type.value,
            "name": work_summary.employer,
            "sameAs": work_summary.url
        },
        "startDate": work_summary.start_date.isoformat(),
        "endDate": None if work_summary.end_date is None else work_summary.end_date.isoformat()
    }


def map_education_organization_type(education_type: EducationalOrganizationType) -> str:
    switch = {
        EducationalOrganizationType.UNIVERSITY: "CollegeOrUniversity",
        EducationalOrganizationType.HIGH_SCHOOL: "HighSchool"
    }
    return switch[education_type]


def convert_education_summary(education_summary: Education) -> dict:
    mapped_education_type = map_education_organization_type(education_summary.type)
    return {
        "@type": "OrganizationRole",
        "alumniOf": {
            "@type": mapped_education_type,
            "name": education_summary.name,
            "sameAs": education_summary.url
        },
        "startDate": education_summary.start_date.isoformat(),
        "endDate": None if education_summary.end_date is None else education_summary.end_date.isoformat()
    }


def convert_language(language: _Language) -> dict:
    return {
        "@type": "Language",
        "name": language.name,
        "alternateName": language.alpha2
    }


def convert_knowledge(programming: dict) -> list[str]:
    """
    See https://stackoverflow.com/a/13016200 for more info
    """
    return [x for v in programming.values() for x in v]


def convert(data: ResumeData) -> dict:
    address = convert_address(data.summaries.address)
    formatted_phone_number = data.summaries.personal_data.contact.phone.iso
    current_work_info = convert_work_summary(data.summaries.current_work_summary)

    previous_work_info = [convert_work_summary(previous_work_summary) for previous_work_summary in data.summaries.previous_work_summaries]
    education_info = [convert_education_summary(previous_education_institution) for previous_education_institution in data.summaries.education]
    organization_alumni = [*previous_work_info, *education_info]

    knowledge = convert_knowledge(data.summaries.skills.programming)
    languages_known = [convert_language(language) for language in data.summaries.skills.general.languages]

    return {
        "@context": "https://schema.org",
        "@type": "Person",
        "address": address,
        "name": data.summaries.personal_data.name,
        "description": data.summaries.personal_data.description,
        "email": f"mailto:{data.summaries.personal_data.contact.email}",
        "image": data.summaries.personal_data.image,
        "telephone": f"tel:{formatted_phone_number}",
        "url": data.summaries.personal_data.contact.url.full_url,
        "nationality": {
            "@type": "Country",
            "name": data.summaries.personal_data.nationality.alpha_3
        },
        "jobTitle": data.summaries.current_work_summary.job_title,
        "worksFor": current_work_info,
        "alumniOf": organization_alumni,
        "knowsAbout": knowledge,
        "knowsLanguage": languages_known
    }


class JSONLDTemplator(Templator):
    def template(self, data: ResumeData) -> TemplatedData:
        converted_data = convert(data)

        return TemplatedData(
            data=json_dumps(converted_data, indent=4),
            file_name="json-schema",
            type=self.type()
        )

    def type(self) -> TemplateType:
        return TemplateType.JSON


def load_templator() -> Templator:
    return JSONLDTemplator()
