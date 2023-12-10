# See: https://adventofcode.com/2023/day/5

defmodule Day5 do

  defp to_seeds(seeds_str), do: (
    seeds_str
    |> String.replace("seeds: ", "")
    |> String.replace("\n", "")
    |> String.split(" ")
    |> Enum.map(&String.to_integer(&1))
  )

  defp to_range_block(range_block_str), do:
  (
    [range_key | [ranges_str | []]] = range_block_str |> String.split(" map:\n", trim: true)
    {
      String.replace(range_key, "\n", ""),
      ranges_str
      |> String.split("\n")
      |> Enum.map(fn (row) -> row |> String.split(" ", trim: true) |> Enum.map(&String.to_integer(&1)) end)
    }
  )

  # step 1 - is my source value in the sources range for a given line?
  # step 2 - if yes convert the source value to the dest value
  # step 3 - repeat walking through each map until you get to the last one (the location map)
  # step 4 - get the minimum location value

  def run, do: (
    filename = "sample.txt"
    filename = "input.txt"
    {:ok, contents} = File.read(filename)
    [seeds_str | ranges_strs] = contents |> String.split("--")
    seeds = to_seeds(seeds_str)
    planting_maps = ranges_strs |> Enum.map(&to_range_block(&1))

    part1(seeds, planting_maps) |> IO.puts()
    part2(seeds, planting_maps) |> IO.puts()
  )

  defp to_dest_value(source_value, [dest_start, source_start, range_length]), do: (
    cond do
      source_value >= source_start and source_value <= source_start + range_length -> dest_start + (source_value - source_start)
      true -> source_value
    end
  )

  defp source_to_dest(source_value, {key, range_map}), do: (
    possible_destinations = range_map
    |> Enum.filter(fn (val) -> val != [] end)
    |> Enum.map(&to_dest_value(source_value, &1))

    total_matches = possible_destinations |> Enum.filter(fn(val) -> val != source_value end)
    cond do
      length(total_matches) == 1 -> hd(total_matches)
      true -> source_value
    end
  )

  # Very lisp of you, elixir...
  defp part1(seeds, [seed_to_soil | [soil_to_fert | [fert_to_water | [water_to_light | [light_to_temp | [temp_to_humid | [humid_to_loc | []]]]]]]]), do: (
    IO.puts("Part 1 Solution:")
    seeds
    |> Enum.map(&source_to_dest(&1, seed_to_soil))
    |> Enum.map(&source_to_dest(&1, soil_to_fert))
    |> Enum.map(&source_to_dest(&1, fert_to_water))
    |> Enum.map(&source_to_dest(&1, water_to_light))
    |> Enum.map(&source_to_dest(&1, light_to_temp))
    |> Enum.map(&source_to_dest(&1, temp_to_humid))
    |> Enum.map(&source_to_dest(&1, humid_to_loc))
    |> Enum.min()
  )

  defp to_dest_ranges([src_start, src_end], [dest_start, map_source_start, range_length]), do: (
    map_source_end = map_source_start + range_length - 1
    dest_end = dest_start + range_length - 1
    cond do
      #   s--s
      # m-----m
      src_start >= map_source_start and src_end <= map_source_end ->
        {[src_start, src_end], [dest_start + (src_start - map_source_start), dest_start + (src_end - map_source_start)]}
      # s------s
      #   m--m
      src_start < map_source_start and src_end > map_source_end ->
        {[map_source_start, map_source_end], [dest_start, dest_end]}
      #    s-----s
      # m----m
      src_start >= map_source_start and src_start <= map_source_end ->
        {[src_start, map_source_end], [dest_start + (src_start - map_source_start), dest_end]}
      # s------s
      #    m-----m
      src_end >= map_source_start and src_end <= map_source_end ->
        {[map_source_start, src_end], [dest_start, dest_start + (src_end - map_source_start)]}
      true -> {[], []}
    end
  )

  defp is_value_unmapped?(value, []), do: (
    true
  )
  defp is_value_unmapped?(value, mappings), do: (
    mappings
    |> Enum.map(fn([start, finish]) -> value < start or value > finish end)
    |> Enum.all?()
  )

  # Well that was a bust, in order to determine which values were unmapped, I ended up looping over every seed number
  # ANYWAY, which kind of voids bothering to work with ranges from the get go, which would have been easily do-able in a language
  # that allows variable mutation, instead of just being a pain in general.
  defp unmapped_ranges([start, finish], mapped_ranges), do: (
    unmapped_values = start..finish
    |> Enum.filter(&is_value_unmapped?(&1, mapped_ranges))
    |> Enum.map(fn(value) -> [value, value] end)

    cond do
      unmapped_values == [] -> []
      true ->
        unmapped_values
        |> prep()
        |> Enum.reduce(
          fn([v3, _], [[v1, v2] | tail]) ->
            cond do
              v2 + 1 == v3 -> [[v1, v3] | tail]
              true -> [[v1, v2] | [[v3, v3] | tail]]
            end
          end)
    end
  )

  defp source_range_to_dest_ranges(source_range, {key, range_map}), do: (
    dest_range_mappings = range_map
    |> Enum.filter(fn (val) -> val != [] end)
    |> Enum.map(&to_dest_ranges(source_range, &1))
    mapped_source_ranges = dest_range_mappings
    |> Enum.map(fn({mapped_range, _}) -> mapped_range end)
    |> Enum.filter(fn (val) -> val != [] end)

    unmapped_source_ranges = unmapped_ranges(source_range, mapped_source_ranges)

    maps_to_destiation = dest_range_mappings
    |> Enum.map(fn({_, dest_range}) -> dest_range end)

    all_mappings = maps_to_destiation ++ unmapped_source_ranges
    all_mappings
    |> Enum.filter(fn (val) -> val != [] end)
  )

  defp merge_step([start1, end1], [[start2, end2] | tail]), do: (
    cond do
      # we're sorted by x and y, and don't have any gaps yet, so if we get two digits on the same row
      # they're safe to combine
      (start1 >= start2 and start1 <= end2)
      or (end1 >= start2 and end1 <= end2)
      or (start2 >= start1 and start2 >= end2)
      or (end2 >= start1 and end2 <= end1) ->
        [[Enum.min([start1, start2]), Enum.max([end1, end2])] | tail]
      # If we have a non digit value, just re-assemble as-is
      true ->  [[start1, end1] | [[start2, end2] | tail]]
    end
)

  # Making sure I can get access to the first two elements of my list by pulling it apart a bit
  # first -> overloading to handle the empty case
  defp prep([]), do: []
  defp prep([head | tail]), do: [[head]|tail]

  defp merge_intervals(intervals), do: (
    intervals
    |> Enum.filter(fn (val) -> val != [] end)
    |> Enum.sort(fn ([s1, _], [s2, _]) -> s1 > s2 end)
    |> prep()
    |> Enum.reduce(&merge_step/2)
  )

  # I should have just used tuples to represent my ranges, and then I could have just used flatten
  # in stead of this monstrosity...
  defp reformat(list), do: (
    list
    |> List.flatten()
    |> Enum.with_index()
    |> Enum.reduce([[], []], fn ({x, i}, [evens, odds]) ->
      case rem(i, 2) do
        0 -> [evens ++ [x], odds]
        _ -> [evens, odds ++ [x]]
      end
    end)
    |> Enum.zip()
    |> Enum.map(fn ({v1, v2}) -> [v1, v2] |> Enum.sort() end)
  )

  # Ok so part two, brute forcing would be nightmarishly slow. I think the solution here would be to keep the ranges in memory,
  # then and split them apart by start/finish of their position within the map ranges.
  # So say you have the range 79 - 14 and a map that includes 55-80 and 0-18. That would mean that instead of trying to pass a value
  # for each seed type in our range, we would instead on the following step check to see where the ranges 55-79, 14-18, and 19-54 should
  # land in the next map, and then carry that on down the line.
  # The I think we need an interval merge to make the 'optimized' version slightly less insane as well.
  defp part2(seeds, [seed_to_soil | [soil_to_fert | [fert_to_water | [water_to_light | [light_to_temp | [temp_to_humid | [humid_to_loc | []]]]]]]]), do: (
    IO.puts("Part 2 Solution:")
    seeds
    |> reformat()
    |> Enum.map(fn ([length, src_start]) -> [src_start, src_start + length - 1] end)
    |> merge_intervals()
    |> Enum.map(&source_range_to_dest_ranges(&1, seed_to_soil))
    |> reformat()
    |> merge_intervals()
    |> Enum.map(&source_range_to_dest_ranges(&1, soil_to_fert))
    |> reformat()
    |> merge_intervals()
    |> Enum.map(&source_range_to_dest_ranges(&1, fert_to_water))
    |> reformat()
    |> merge_intervals()
    |> Enum.map(&source_range_to_dest_ranges(&1, water_to_light))
    |> reformat()
    |> merge_intervals()
    |> Enum.map(&source_range_to_dest_ranges(&1, light_to_temp))
    |> reformat()
    |> merge_intervals()
    |> Enum.map(&source_range_to_dest_ranges(&1, temp_to_humid))
    |> reformat()
    |> merge_intervals()
    |> Enum.map(&source_range_to_dest_ranges(&1, humid_to_loc))
    |> reformat()
    |> merge_intervals()
    |> List.flatten()
    |> Enum.min()
  )
end

Day5.run()
