# --- Day 3: Gear Ratios ---

# You and the Elf eventually reach a gondola lift station; he says the gondola lift will take you up
# to the water source, but this is as far as he can bring you. You go inside.

# It doesn't take long to find the gondolas, but there seems to be a problem: they're not moving.

# "Aaah!"

# You turn around to see a slightly-greasy Elf with a wrench and a look of surprise. "Sorry, I wasn't
# expecting anyone! The gondola lift isn't working right now; it'll still be a while before I can fix
# it." You offer to help.

# The engineer explains that an engine part seems to be missing from the engine, but nobody can figure
# out which one. If you can add up all the part numbers in the engine schematic, it should be easy to
# work out which part is missing.

# The engine schematic (your puzzle input) consists of a visual representation of the engine. There
# are lots of numbers and symbols you don't really understand, but apparently any number adjacent to
# a symbol, even diagonally, is a "part number" and should be included in your sum. (Periods (.) do
# not count as a symbol.)

# Here is an example engine schematic:

# 467..114..
# ...*......
# ..35..633.
# ......#...
# 617*......
# .....+.58.
# ..592.....
# ......755.
# ...$.*....
# .664.598..

# In this schematic, two numbers are not part numbers because they are not adjacent to a symbol:
# 114 (top right) and 58 (middle right). Every other number is adjacent to a symbol and so is a part
# number; their sum is 4361.

# Of course, the actual engine schematic is much larger. What is the sum of all of the part numbers
# in the engine schematic?

# grab positional ranges for each non-period in the input, as well as symbol vs digit
# Then use the ranges to determine if any given digit intersects with any given symbol

# filename = "sample1.txt"
filename = "input.txt"
{:ok, contents} = File.read(filename)

defmodule Coordinates do
    # This isn't really a true coordinate, I want something closer to a vector this maps to:
    # (value, x-end, e-start, y)  -> this is a bit of an artifact of the tail-recursion we're doing
    # when merging our coordinates... not quite sure how to correct that.
    defp to_coordinates({value, x}, y), do: {value, x, x, y}

    def str_to_coordinates({str, y}), do: (
      String.split(str, "", trim: true)
      |> Enum.with_index(1)
      |> Enum.map(&to_coordinates(&1, y))
    )

    # if we're overlapping, and both our values are digits, we should merge into a single vertor-like coordinate
    defp merge_step({value, x1s, x1e, y1}, [{next_value, x2s, x2e, y2} | tail]), do: (
        cond do
          # we're sorted by x and y, and don't have any gaps yet, so if we get two digits on the same row
          # they're safe to combine
          Regex.match?(~r/\d/, value)
            and Regex.match?(~r/\d/, next_value)
            and y1 == y2 -> [{next_value <> value, x1s, x2e, y1} | tail]
          # If we have a non digit value, just re-assemble as-is
          true ->  [{value, x1s, x1e, y1} | [{next_value, x2s, x2e, y2} | tail]]
        end
    )

    # Making sure I can get access to the first two elements of my list by pulling it apart a bit
    # first -> overloading to handle the empty case
    defp prep([]), do: []
    defp prep([head | tail]), do: [[head]|tail]

    def merge_coordinates(coordinates), do: (
      coordinates
      |> prep()
      |> Enum.reduce(&merge_step/2)
    )

    def contacts?({_, x1_end, x1_start, y1}, {_, x2, _, y2}), do: (
      (y1 == y2 or y1 == y2 + 1 or y1 == y2 - 1)
      and x1_start-1 <= x2 and x1_end+1 >= x2
    )

    def gear_ratio(gear, parts), do: (
      connects_to = parts
      |> Enum.filter(&contacts?(&1, gear))
      case length(connects_to) do
        2 -> Enum.map(connects_to, fn ({val, _, _, _}) -> val end) |> Enum.product()
        _ -> 0
      end
    )
end

IO.puts "Part 1 Solution:"
schematic = String.split(contents, "\n", trim: true)
|> Enum.with_index(1)
|> Enum.map(&Coordinates.str_to_coordinates(&1))
|> List.flatten()
|> Coordinates.merge_coordinates()
|> Enum.filter(fn ({val, _, _, _}) -> val != "." end)

schematic_symbols = schematic
|> Enum.filter(fn ({val, _, _, _}) -> not Regex.match?(~r/\d+/, val) end)

schematic_numbers = schematic
|> Enum.filter(fn ({val, _, _, _}) -> Regex.match?(~r/\d+/, val) end)
|> Enum.map(fn ({val, a, b, c}) -> {String.to_integer(val), a, b, c} end)

schematic_numbers
|> Enum.filter(fn (coord) -> Enum.any?(Enum.map(schematic_symbols, &Coordinates.contacts?(coord, &1))) end)
|> Enum.map(fn ({val, _, _, _}) -> val end)
|> Enum.sum()
|> IO.puts()

IO.puts "Part 2 Solution:"

parts = schematic_numbers
|> Enum.filter(fn (coord) -> Enum.any?(Enum.map(schematic_symbols, &Coordinates.contacts?(coord, &1))) end)

gears = schematic_symbols
|> Enum.filter(fn ({symbol, _, _, _}) -> symbol == "*" end)
|> Enum.map(&Coordinates.gear_ratio(&1, parts))
|> Enum.sum()
|> IO.puts
