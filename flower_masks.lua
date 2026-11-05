-- Returns Totoro's outline as the only flower obstacle. Text bounds are diagnostic
-- preview regions, not growth exclusions, because the text is drawn over the flowers.
return function(page_width, resume_totoro_center_x)
  local poly = {}
  for i, p in ipairs(dofile("totoro_outline.lua")) do
    poly[i] = { page_width - (resume_totoro_center_x - 2.75 / 2 + p[1] * 2.75), 1.5 + p[2] * 2.75 }
  end
  return { poly }
end
