from pyresume.templators.latex_2_column_resume import escape_latex


def test_latex_skill_does_not_use_math_logo():
  assert escape_latex("LaTeX") == "LaTeX"
