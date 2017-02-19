--local inspect = require("inspect")

local function sum_t(t)
  local sum = 0
  for i = 1, #t do
    if t[i] then
      sum = sum + t[i]
    end
  end
  return sum
end

local function remove_entry(t, idx)
  t[idx] = false
  for i = 1, #t do
    if t[i] then
      t[i][2][idx] = false
    end
  end
end

-- metrics = { { lang, { { word=ipa, { num, ... } }, ... } }, ... }
local metrics = {}

-- read input
local fin = assert(io.open("lm_output","r"))
for line in fin:lines() do
  if line:byte() == string.byte("#") then
    metrics[#metrics+1] = { line:sub(3), {} }
  elseif line ~= "" then
    local tab = line:find("\t")
    local rows = metrics[#metrics][2]
    rows[#rows+1] = { line:sub(1, tab-1):match("^(.-)="), {} }
    local row = rows[#rows][2]
    for field in line:sub(tab+1):gmatch("[%d.]+") do
       row[#row+1] = field
    end
  end
end
fin:close()

-- remove duplicates
for i = 1, #metrics do
  -- per language
  local language = metrics[i][2]
  local n_words = #language
  local idxs = {}

  -- store all the starting idxs of different meanings
  local prev = "";
  for j = 1, n_words do
    if language[j][1] ~= prev then
      idxs[#idxs+1] = j
      prev = language[j][1]
    end
  end

  -- loop over all indices of meanings
  for j = 1, #idxs-1 do
    local num = idxs[j+1] - idxs[j]
    -- in case of duplicates
    if num > 1 then
      -- for every duplicate
      local maxidx = idxs[j]
      local maxval = sum_t(language[maxidx][2])
      for k = 1, num-1 do
        local val = sum_t(language[idxs[j] + k][2])
        if val > maxval then -- new maxval
          remove_entry(language, maxidx)
          maxval = val
          maxidx = idxs[j] + k
        else -- this value is lower than the prev maxval
          remove_entry(language, idxs[j] + k)
        end
      end
    end
  end
end

-- write output
for i = 1, #metrics do
  local fname = "lm/lm_"..metrics[i][1]:lower():gsub("%s", "_")
  local fout = assert(io.open(fname, "w"))
  --fout:write("# "..metrics[i][1].."\n")
  local language = metrics[i][2]
  for j = 1, #language do
    if language[j] then
      fout:write(language[j][1].."\t")
      if language[j][2] then
        local row = language[j][2]
        for k = 1, #row do
          if row[k] then
            fout:write(string.format("%.16f ", row[k]))
          end
        end
        fout:write("\n")
      end
    end
  end
  fout:close()
end
