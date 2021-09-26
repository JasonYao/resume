# stdlib imports
from typing import Optional
from typing import Union
from dataclasses import dataclass
from re import sub
from datetime import date
from dateutil import relativedelta

# Dependency imports
from jinja2 import Template
from jinja2 import Environment
from jinja2 import PackageLoader
from jinja2 import select_autoescape

# Project imports
from ..templating import Templator
from ..templating import TemplateType
from ..templating import TemplatedData
from ..templating import ResumeData
from ..templating import Education
from ..templating import HigherEducation
from ..templating import WorkDescription
from ..templating import WorkPosition


@dataclass(frozen=True, order=True)
class WorkExperience(WorkDescription):
    work_duration: str


"""
NOTE: We follow advice from http://eosrei.net/articles/2015/11/latex-templates-python-and-jinja2-generate-pdfs,
  where we replace the default curly braces with other values, since jinja2
  will otherwise get confused
"""
env = Environment(
    loader=PackageLoader("pyresume.templators.latex_2_column_resume"),
    autoescape=select_autoescape(),
    block_start_string='\BLOCK{',
    block_end_string='}',
    variable_start_string='\VAR{',
    variable_end_string='}',
    comment_start_string='\#{',
    comment_end_string='}',
    line_statement_prefix='%%',
    line_comment_prefix='%#',
    trim_blocks=True,
)


def get_latest_education(education_history: list[Education]) -> Union[Education, HigherEducation, None]:
    """
    Currently we presume that the education history passed in is ordered,
    we can add in sorting here by attendance date if we need to in the
    future
    """
    if len(education_history) == 0:
        return None

    latest_education = education_history[0]
    return latest_education


def escape_latex(unescaped_sequence: Union[str, dict]) -> Union[str, dict]:
    if type(unescaped_sequence) is not str:
        return unescaped_sequence

    escaped_latex_key_characters = unescaped_sequence.replace("&", "\\&")\
        .replace("%", "\\%")\
        .replace("~", "\\textasciitilde")\
        .replace("LaTeX", "\\LaTeX")
    escaped_bolded_text = sub("\*\*.*?\*\*", lambda matched_text: f"\\textbf{{{matched_text.group(0).replace('**', '')}}}", escaped_latex_key_characters)
    escaped_italicized_text = sub("\_.*?\_", lambda matched_text: f"\\textit{{{matched_text.group(0).replace('_', '')}}}", escaped_bolded_text)
    return escaped_italicized_text


def normalize_position(position: WorkPosition) -> WorkPosition:
    return WorkPosition(
        title=escape_latex(position.title),
        start_date=position.start_date.strftime("%b %Y"),
        end_date="Present" if position.end_date is None else position.end_date.strftime("%b %Y"),
        descriptions=[escape_latex(description) for description in position.descriptions],
    )


def round_job_duration(duration: relativedelta.relativedelta) -> relativedelta:
    years = duration.years
    months = duration.months
    days = duration.days

    if days > 0:
        months += 1
        days = 0

    if months > 12:
        years += 1
        months -= 12

    return relativedelta.relativedelta(days=days, months=months, years=years)


def map_to_experience(job: WorkDescription) -> WorkExperience:
    work_start_date = min([position.start_date for position in job.positions])
    end_dates = {position.end_date for position in job.positions}

    if None in end_dates:
        # This means that I'm still working this job
        work_end_date = date.today()
    else:
        # This means that we've already left the job
        work_end_date = max(end_dates)

    rounded_job_duration = round_job_duration(relativedelta.relativedelta(work_end_date, work_start_date))
    if rounded_job_duration.years > 0:
        work_duration = f"{rounded_job_duration.years} years, {rounded_job_duration.months} months"
    elif rounded_job_duration.years == 0 and rounded_job_duration.months == 0 and rounded_job_duration.days >= 0:
        work_duration = f"Recently Started"
    elif rounded_job_duration.years < 0 or rounded_job_duration.months < 0 or rounded_job_duration.days < 0:
        work_duration = f"Starting Soon"
    else:
        work_duration = f"{rounded_job_duration.months} months"

    positions = [normalize_position(position) for position in job.positions]
    return WorkExperience(
        company_name=job.company_name,
        location=job.location,
        positions=positions,
        work_duration=work_duration
    )


class ResumeTex2ColumnTemplator(Templator):
    def __init__(self, template: Optional[Template]):
        self.loaded_template = template

    def template(self, data: ResumeData) -> TemplatedData:
        latest_education = get_latest_education(data.summaries.education)

        latex_data = {
            # Top section
            'name': data.summaries.personal_data.name,
            'email': data.summaries.personal_data.contact.email,
            'github_full': data.summaries.personal_data.contact.github.full_url,
            'github': data.summaries.personal_data.contact.github.truncated_url,
            'linkedin_full': data.summaries.personal_data.contact.linkedin.full_url,
            'linkedin': data.summaries.personal_data.contact.linkedin.truncated_url,
            'phone_well_formed': data.summaries.personal_data.contact.phone.well_formed_phone_number,
            'phone_iso': data.summaries.personal_data.contact.phone.iso,
            'website_full': data.summaries.personal_data.contact.url.full_url,
            'website': data.summaries.personal_data.contact.url.truncated_url,

            # Left column - education
            'university_name': latest_education.name,
            'college_name': latest_education.college,
            'full_degree': latest_education.degree.abbreviation,
            'graduation_date': latest_education.end_date.strftime("%b %Y"),

            # Left column - skills
            'programming_skills': {skill_header: [escape_latex(skill) for skill in skills] for skill_header, skills in data.summaries.skills.programming.items()},
            'languages': [language.name for language in data.summaries.skills.general.languages],
            'misc': data.summaries.skills.general.misc,

            # Right column - experience
            'employers': [map_to_experience(job) for job in data.job_history]
        }

        escaped_data = {key: escape_latex(value) for key, value in latex_data.items()}
        templated_data = self.loaded_template.render(**escaped_data)

        return TemplatedData(
            data=templated_data,
            file_name="Resume_Jason_Yao",
            type=self.type()
        )

    def type(self) -> TemplateType:
        return TemplateType.LATEX


def load_template() -> Template:
    return env.get_template("2_column_resume.tex.jinja")


def load_templator() -> Templator:
    template = load_template()
    return ResumeTex2ColumnTemplator(template)
