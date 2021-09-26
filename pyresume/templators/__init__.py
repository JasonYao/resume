from .biography import load_templator
from .templating import load_data, Templator
from .json_raw import load_templator as json_raw_load_templator
from .json_ld import load_templator as json_ld_load_templator
from .latex_2_column_resume import load_templator as latex_2_column_load_templator

# TODO: Replace manual module loading with dynamic loading
templators: list[Templator] = [load_templator(), json_raw_load_templator(), json_ld_load_templator(), latex_2_column_load_templator()]
