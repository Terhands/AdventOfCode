# See: https://adventofcode.com/2023/day/6

defmodule Day6 do

  defp peek(value), do: IO.inspect(value, charlist: :as_list)

  defp clean_race_data(data, to_replace), do: (
    data |> String.replace(to_replace, "") |> String.split(" ", trim: true) |> Enum.map(&String.to_integer/1)
  )

  defp to_race_data([time_data | [distance_data | []]]), do: (
    Enum.zip(
      time_data |> clean_race_data("Time:"),
      distance_data |> clean_race_data("Distance:")
    ) |> peek()
  )

  def run, do: (
    filename = "sample.txt"
    filename = "input.txt"
    {:ok, contents} = File.read(filename)
    part1(contents) |> IO.puts()
    part2(contents) |> IO.puts()
  )

  defp pressed_time_to_distance(pressed_time, race_end_time), do: (race_end_time - pressed_time) * pressed_time

  defp ways_to_win_race({time, distance_to_beat}), do: (
    # peek("Time: #{time} Distance To Beat: #{distance_to_beat}")
    0..time
    |> Enum.map(&pressed_time_to_distance(&1, time))
    |> Enum.filter(fn (distance_travelled) -> distance_travelled > distance_to_beat end)
    |> length()
    # |> peek()
  )

  defp part1(contents), do: (
    IO.puts("Part 1 Solution:")
    race_data = contents |> String.split("\n", trim: true) |> to_race_data()
    race_data |> Enum.map(&ways_to_win_race/1) |> Enum.product()
  )

  defp part2(contents), do: (
    IO.puts("Part 2 Solution:")
    [race_time, distance_to_beat] = contents
    |> String.replace(" ", "") |> String.replace("Time:", "") |> String.replace("Distance:", "")
    |> String.split("\n", trim: true)
    |> Enum.map(&String.to_integer/1)
    |> peek()
    ways_to_win_race({race_time, distance_to_beat})
  )
end

Day6.run()
