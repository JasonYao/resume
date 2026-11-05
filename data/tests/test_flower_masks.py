import pytest

from pyresume.flower_masks import _format_regions, mask_regions_from_bbox


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

    assert regions == [(0.353, 26.529, 3.528, 27.234)]


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


def test_format_regions_writes_lua_masks_and_preview_boxes():
    lua_content, tex_content = _format_regions([(1.0, 2.0, 3.0, 4.0)])

    assert lua_content == "return {\n  { 1.000, 2.000, 3.000, 4.000 },\n}\n"
    assert tex_content == "\\resumeFlowerMaskBox{1.000cm}{2.000cm}{3.000cm}{4.000cm}\n"
