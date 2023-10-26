# Stdlib imports
from abc import ABC
from abc import abstractmethod
from dataclasses import dataclass
from datetime import date
from enum import Enum
from pathlib import Path
from typing import Optional
from typing import Union

# Dependency imports
from dacite import from_dict
from dacite import Config
from pycountry import countries
from iso639 import languages
from iso639.iso639 import _Language


"""
Needed due to pycountries being stupid and having dynamic class names instead
of a sane static dataclass type. Forward references with 'pycountries.db.Country'
don't work as type signatures when paired with dacite, so we do this check
upon load so typing works properly
"""
country_type = type(countries.get(alpha_3="CAN"))


def load_country(raw_country: str) -> country_type:
    return countries.get(alpha_3=raw_country)


def load_language(raw_language: str) -> _Language:
    return languages.get(alpha2=raw_language.lower())


@dataclass(frozen=True, order=True)
class PhoneNumber:
    well_formed_phone_number: str

    @property
    def iso(self) -> str:
        """
        Converts a phone number string from the form:
        +1 (201) 555-0111

        To the tel URL form per RFC 3966 (https://datatracker.ietf.org/doc/html/rfc3966)
        +1-201-555-0111
        """
        return self.well_formed_phone_number.replace('(', '').replace(')', '').replace(' ', '-')


@dataclass(frozen=True, order=True)
class Link:
    schema: str
    link: str

    @property
    def full_url(self) -> str:
        return f"{self.schema}://{self.link}"

    @property
    def truncated_url(self) -> str:
        return self.link.replace("www.", "")


@dataclass(frozen=True, order=True)
class Address:
    """
    Representation of any address in the world, with fields specified
    from https://shopify.engineering/handling-addresses-from-all-around-the-world
    """
    address_line_1: Optional[str]
    address_line_2: Optional[str]
    zone_code: str
    postal_code: str
    city: str
    country_code: country_type

    def __dict__(self) -> dict:
        val_dict = {
            'zone_code': self.zone_code,
            'postal_code': self.postal_code,
            'city': self.city,
            'country_code': self.country_code.alpha_3
        }

        if self.address_line_1 is not None:
            val_dict['address_line_1'] = self.address_line_1

        if self.address_line_2 is not None:
            val_dict['address_line_2'] = self.address_line_2

        return val_dict


@dataclass(frozen=True, order=True)
class ContactInfo:
    email: str
    phone: PhoneNumber
    url: Link
    linkedin: Link
    github: Link

    def __dict__(self) -> dict:
        return {
            'email': self.email,
            'phone': self.phone.well_formed_phone_number,
            'url': self.url.full_url,
            'linkedin': self.linkedin.full_url,
            'github': self.github.full_url
        }


@dataclass(frozen=True, order=True)
class PersonalData:
    name: str
    description: str
    image: str
    nationality: country_type
    contact: ContactInfo

    def __dict__(self) -> dict:
        return {
            'name': self.name,
            'description': self.description,
            'image': self.image,
            'nationality': self.nationality.alpha_3,
            'contact': self.contact.__dict__()
        }


class EducationalOrganizationType(Enum):
    HIGH_SCHOOL = "High School"
    UNIVERSITY = "University"


class HigherEducationDegreeFocus(Enum):
    ARTS = "Arts"
    SCIENCES = "Sciences"
    FINE_ARTS = "Fine Arts"


class HigherEducationLevel(Enum):
    ASSOCIATES = "Associates"
    BACHELORS = "Bachelors"
    MASTERS = "Masters"
    DOCTORATE = "Doctorate"


class HigherEducationDegreeArea(Enum):
    COMPUTER_SCIENCE = "Computer Science"


@dataclass(frozen=True, order=True)
class Degree:
    level: HigherEducationLevel
    focus: HigherEducationDegreeFocus
    area: HigherEducationDegreeArea

    @property
    def full_name(self) -> str:
        return f"{self.level.value} of {self.focus.value} in {self.area.value}"

    @property
    def abbreviation(self) -> str:
        levels = {
            HigherEducationLevel.ASSOCIATES: "A",
            HigherEducationLevel.BACHELORS: "B",
            HigherEducationLevel.MASTERS: "M",
            HigherEducationLevel.DOCTORATE: "PhD",
        }

        if HigherEducationLevel.DOCTORATE == self.level:
            return f"{levels[self.level]} in {self.area.value}"

        foci = {
            HigherEducationDegreeFocus.ARTS: "A",
            HigherEducationDegreeFocus.SCIENCES: "S",
            HigherEducationDegreeFocus.FINE_ARTS: "AS",
        }

        return f"{levels[self.level]}{foci[self.focus]} in {self.area.value}"


@dataclass(frozen=True, order=True)
class Education:
    type: EducationalOrganizationType
    name: str
    url: str
    start_date: date
    end_date: Optional[date]

    @staticmethod
    def create(data: dict) -> Union['Education', 'HigherEducation']:
        educational_type = EducationalOrganizationType(data.get("type"))
        type_hooks = {
            date: date.fromisoformat,
            HigherEducationLevel: HigherEducationLevel,
            HigherEducationDegreeFocus: HigherEducationDegreeFocus,
            HigherEducationDegreeArea: HigherEducationDegreeArea,
            EducationalOrganizationType: EducationalOrganizationType,
        }

        if educational_type == EducationalOrganizationType.UNIVERSITY:
            return from_dict(data_class=HigherEducation, data=data, config=Config(type_hooks=type_hooks))
        else:
            return from_dict(data_class=Education, data=data, config=Config(type_hooks=type_hooks))


@dataclass(frozen=True, order=True)
class HigherEducation(Education):
    college: str
    degree: str
    degree: Degree


class OrganizationType(Enum):
    ORGANIZATION = "Organization"
    CORPORATION = "Corporation"
    NON_GOVERNMENTAL_ORGANIZATION = "NGO"


@dataclass(frozen=True, order=True)
class WorkSummary:
    job_title: str
    employer: str
    url: str
    type: OrganizationType
    start_date: date
    end_date: Optional[date]


@dataclass(frozen=True, order=True)
class GeneralSkills:
    languages: list[_Language]
    misc: str

    @staticmethod
    def create(data: dict) -> 'GeneralSkills':
        type_hooks = {
            _Language: load_language
        }
        return from_dict(data_class=GeneralSkills, data=data, config=Config(type_hooks=type_hooks))

    def __dict__(self) -> dict:
        return {
            'languages': [language.alpha2 for language in self.languages],
            'misc': self.misc
        }


@dataclass(frozen=True, order=True)
class Skills:
    general: GeneralSkills
    programming: dict

    def __dict__(self) -> dict:
        return {
            'general': self.general.__dict__(),
            'programming': self.programming
        }


@dataclass(frozen=True, order=True)
class SummaryData:
    address: Address
    personal_data: PersonalData
    current_work_summary: WorkSummary
    previous_work_summaries: list[WorkSummary]
    education: list[Education]
    skills: Skills

    def __dict__(self) -> dict:
        return {
            'address': self.address.__dict__(),
            'personal_data': self.personal_data.__dict__(),
            'current_work_summary': self.current_work_summary,
            'previous_work_summaries': self.previous_work_summaries,
            'education': self.education,
            'skills': self.skills.__dict__()
        }


@dataclass(frozen=True, order=True)
class WorkPosition:
    title: str
    start_date: date
    end_date: Optional[date]
    descriptions: list[str]


@dataclass(frozen=True, order=True)
class WorkLogos:
    short: Optional[str]
    long: Optional[str]


@dataclass(frozen=True, order=True)
class WorkDescription:
    company_name: str
    location: str
    positions: list[WorkPosition]
    logos: WorkLogos


@dataclass(frozen=True, order=True)
class ResumeData:
    summaries: SummaryData
    job_history: list[WorkDescription]
    biography: str

    def __dict__(self) -> dict:
        return {
            'summaries': self.summaries.__dict__(),
            'job_history': self.job_history,
            'biography': self.biography
        }


def load_data(data: dict) -> ResumeData:
    type_hooks = {
        date: date.fromisoformat,
        country_type: load_country,
        OrganizationType: OrganizationType,
        Education: Education.create,
        GeneralSkills: GeneralSkills.create,
        Link: lambda raw_link: Link(raw_link.split('://')[0], raw_link.split('://')[1]),
        PhoneNumber: lambda raw_phone: PhoneNumber(raw_phone)
    }

    return from_dict(data_class=ResumeData, data=data, config=Config(type_hooks=type_hooks))


class TemplateType(Enum):
    JSON = "json"
    JSON_LD = "json"
    PLAINTEXT = "txt"
    LATEX = "tex"


@dataclass(frozen=True, order=True)
class TemplatedData:
    data: str
    file_name: str
    type: TemplateType

    @property
    def file_path(self) -> Path:
        return Path(f"{self.file_name}.{self.type.value}")

    def write(self):
        with self.file_path.open('w') as fp:
            fp.write(self.data)


class Templator(ABC):

    @abstractmethod
    def template(self, data: ResumeData) -> TemplatedData:
        pass

    @abstractmethod
    def type(self) -> TemplateType:
        pass
