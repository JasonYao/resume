# stdlib imports
from typing import Optional

# Dependency imports
from jinja2 import Template

# Project imports
from ..templating import Templator
from ..templating import TemplateType
from ..templating import TemplatedData
from ..templating import ResumeData


class PlainTextBiographyTemplator(Templator):
    def __init__(self, template: Optional[Template]):
        self.loaded_template = template

    def template(self, data: ResumeData) -> TemplatedData:
        templated_data = self.loaded_template.render(biography=data.biography)

        return TemplatedData(
            data=templated_data,
            file_name="biography",
            type=self.type()
        )

    def type(self) -> TemplateType:
        return TemplateType.PLAINTEXT


def load_templator() -> Templator:
    return PlainTextBiographyTemplator(Template("{{ biography }}"))
