import pytest

from pyresume.flower_masks import (
    MeasuredRegions,
    dump,
    mask_regions_from_bbox,
)


def test_mask_regions_from_bbox_uses_line_bounds_and_page_coordinates():
    bbox_html = """
    <html><body>
    <page width="612.0" height="792.0">
      <flow><block>
        <line xMin="10" yMin="20" xMax="100" yMax="40">
          <word xMin="10" yMin="20" xMax="100" yMax="40">Resume</word>
        </line>
      </block></flow>
    </page>
    </body></html>
    """

    regions = mask_regions_from_bbox(bbox_html, padding=0)

    assert regions.page_width_cm == 21.59
    assert regions.page_height_cm == 27.94
    assert regions.regions == ((0.353, 26.529, 3.528, 27.234),)


def test_mask_regions_from_bbox_rejects_multiple_pages():
    bbox_html = """
    <html><body>
    <page width="612" height="792"></page>
    <page width="612" height="792"></page>
    </body></html>
    """

    with pytest.raises(ValueError, match="single-page"):
        mask_regions_from_bbox(bbox_html)


def test_mask_regions_from_bbox_rejects_empty_text():
    bbox_html = '<html><body><page width="612" height="792"></page></body></html>'

    with pytest.raises(ValueError, match="no measurable text"):
        mask_regions_from_bbox(bbox_html)


def test_measured_regions_reject_out_of_page_bounds():
    with pytest.raises(ValueError, match="fit within the page width"):
        MeasuredRegions(10.0, 10.0, ((1.0, 2.0, 11.0, 4.0),))


def test_dump_writes_lua_masks_and_preview_boxes(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    regions = MeasuredRegions(10.0, 10.0, ((1.0, 2.0, 3.0, 4.0),))

    dump(regions)

    assert (tmp_path / "resume_flower_masks.lua").read_text() == (
        "return {\n  { 1.000, 2.000, 3.000, 4.000 },\n}\n"
    )
    assert (tmp_path / "resume_flower_masks_preview.tex").read_text() == (
        "\\resumeFlowerMaskBox{1.000cm}{2.000cm}{3.000cm}{4.000cm}\n"
    )
