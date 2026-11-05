-- Builds the flower obstacles from the regions the resume build measured (resume_flower_masks.lua, see
-- two-column-resume.cls) and Totoro's outline (totoro_outline.lua). Coordinates are page cm, mirrored in x
-- like the garden. Returns nil when the measured regions are unavailable.
return function(page_width, resume_totoro_center_x)
  local file = io.open("resume_flower_masks.lua", "r")
  if not file then return nil end
  file:close()

  local obstacles = {}
  for _, mask in ipairs(dofile("resume_flower_masks.lua")) do
    obstacles[#obstacles + 1] = { page_width - mask[3], mask[2], page_width - mask[1], mask[4] }
  end
  if #obstacles == 0 then return nil end

  local poly = {}
  for i, p in ipairs(dofile("totoro_outline.lua")) do
    poly[i] = { page_width - (resume_totoro_center_x - 2.75 / 2 + p[1] * 2.75), 1.5 + p[2] * 2.75 }
  end
  obstacles[#obstacles + 1] = poly
  return obstacles
end
