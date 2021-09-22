from pyresume.templators.templating import ResumeData
from pyresume.templators.templating import TemplatedData

from pyresume.templators import templators
from pyresume.templators import load_data


def template_data(data: ResumeData) -> list[TemplatedData]:
    return [templator.template(data) for templator in templators]
