from pathlib import Path
import warnings


TEMPLATOR = Path(__file__).resolve().parents[2] / "pyresume" / "templators" / "latex_2_column_resume" / "__init__.py"


def test_templator_compiles_without_syntax_warnings():
  with warnings.catch_warnings(record=True) as caught:
    warnings.simplefilter("always", SyntaxWarning)
    compile(TEMPLATOR.read_text(), str(TEMPLATOR), "exec")

  assert not caught
