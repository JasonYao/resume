from json import dumps as json_dumps
from json import JSONEncoder
from datetime import date
from enum import Enum
from dataclasses import asdict
from dataclasses import is_dataclass

from pycountry import countries

from ..templating import Templator
from ..templating import TemplateType
from ..templating import TemplatedData
from ..templating import ResumeData

country_type = type(countries.get(alpha_3="CAN"))


class EnhancedJSONEncoder(JSONEncoder):
    def default(self, o):
        if is_dataclass(o):
            return asdict(o)
        elif type(o) == country_type:
            return o.alpha_3
        elif isinstance(o, Enum):
            return o.value
        elif type(o) == date:
            return o.isoformat()

        return super().default(o)


class RawJSONTemplator(Templator):
    def template(self, data: ResumeData) -> TemplatedData:
        templated_data = json_dumps(data.__dict__(), indent=4, cls=EnhancedJSONEncoder)

        return TemplatedData(
            data=templated_data,
            file_name="raw-data",
            type=self.type()
        )

    def type(self) -> TemplateType:
        return TemplateType.JSON


def load_templator() -> Templator:
    return RawJSONTemplator()
