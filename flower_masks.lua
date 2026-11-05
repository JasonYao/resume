-- Builds the flower obstacles from the regions the resume build measured (resume_flower_masks.txt, see
-- two-column-resume.cls) and Totoro's outline (totoro_outline.lua). Coordinates are page cm, mirrored in x
-- like the garden. Returns nil when the measured regions are unavailable.
local sp_to_cm = 2.54 / 72.27 / 65536

return function(page_width, resume_totoro_center_x)
  local file = io.open("resume_flower_masks.txt", "r")
  if not file then return nil end

  local obstacles, starts = {}, {}
  for line in file:lines() do
    local kind = line:find("resumemaskS", 1, true) and "S" or (line:find("resumemaskE", 1, true) and "E")
    local n = {}
    for v in line:gmatch("[0-9-]+") do n[#n + 1] = tonumber(v) end
    if kind == "S" and n[6] then
      local left = (n[2] + n[4]) * sp_to_cm
      starts[n[1]] = { page_width - (left + n[5] * sp_to_cm), page_width - left, (n[3] + n[6]) * sp_to_cm }
    elseif kind == "E" and n[6] and starts[n[1]] then
      local s = starts[n[1]]
      obstacles[#obstacles + 1] = { s[1], (n[3] + n[6]) * sp_to_cm, s[2], s[3] }
    end
  end
  file:close()
  if #obstacles == 0 then return nil end

  local poly = {}
  for i, p in ipairs(dofile("totoro_outline.lua")) do
    poly[i] = { page_width - (resume_totoro_center_x - 2.75 / 2 + p[1] * 2.75), 1.5 + p[2] * 2.75 }
  end
  obstacles[#obstacles + 1] = poly
  return obstacles
end
