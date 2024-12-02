# See: https://adventofcode.com/2023/day/10

defmodule Day10 do

  defp peek(value), do: IO.inspect(value, charlist: :as_list)

  defp to_pipes_map(pipe_row), do: (
    pipe_row |> String.graphemes()
    |> Enum.with_index()
    |> Enum.map(fn({direction, index}) -> {index, direction} end)
    |> Map.new() |> peek()
  )
  defp starting_position(pipes_map), do: (
    peek("finding start...")
    row = pipes_map
    |> Map.filter(fn({y, row}) ->
        Map.size(Map.filter(row, fn({x, pipe}) -> pipe == "S" end)) > 0
      end
    ) |> Map.keys() |> hd()
    column = pipes_map[row] |> Map.filter(fn({x, pipe}) -> pipe == "S" end) |> Map.keys() |> hd()
    {column, row}
  )

  def run, do: (
    filename = "sample1.txt"
    # filename = "sample2.txt"
    filename = "sample3.txt"
    filename = "sample4.txt"
    # filename = "input.txt"
    {:ok, contents} = File.read(filename)
    pipes_map =
      contents
      |> String.split("\n")
      |> Enum.map(&to_pipes_map/1)
      |> Enum.with_index()
      |> Enum.map(fn({pipes, index}) -> {index, pipes} end)
      |> Map.new() |> peek()
    start = starting_position(pipes_map) |> peek()

    part1(pipes_map, start) |> IO.puts()
    part2(pipes_map, start) |> IO.puts()
  )

  defp begin_moving(pipes_map, {x, y}), do: (
    cond do
      # Up
      y > 0 and pipes_map[y-1][x] in ["|", "7", "F"] ->
        move(pipes_map, {x, y-1}, [{x, y}])
      # Down
      y < Map.size(pipes_map)-1 and pipes_map[y+1][x] in ["|", "J", "L"] ->
        move(pipes_map, {x, y+1}, [{x, y}])
      # Left
      x > 0 and pipes_map[y][x-1] in ["-", "F", "L"] ->
        move(pipes_map, {x-1, y}, [{x, y}])
      # Right
      x < Map.size(pipes_map[y])-1 and pipes_map[y][x+1] in ["-", "7", "J"] ->
        move(pipes_map, {x+1, y}, [{x, y}])
    end
  )

  defp is_from_above?(y, y_prev), do: ( y_prev < y )
  defp is_from_below?(y, y_prev), do: ( y_prev > y )
  defp is_from_left?(x, x_prev), do: ( x_prev < x )
  defp is_from_right?(x, x_prev), do: ( x_prev > x )

  defp move(pipes_map, {x, y}, visited), do: (
    {prev_x, prev_y} = hd(visited)
    cond do
      # We've visited the full loop, time to bail.
      pipes_map[y][x] == "S" -> visited

      pipes_map[y][x] == "-" and is_from_left?(x, prev_x) ->
        move(pipes_map, {x+1, y}, [{x, y} | visited]) # move right

      pipes_map[y][x] == "-" and is_from_right?(x, prev_x) ->
        move(pipes_map, {x-1, y}, [{x, y} | visited]) # move left

      pipes_map[y][x] == "|" and is_from_above?(y, prev_y) ->
        move(pipes_map, {x, y+1}, [{x, y} | visited]) # move down

      pipes_map[y][x] == "|" and is_from_below?(y, prev_y) ->
        move(pipes_map, {x, y-1}, [{x, y} | visited]) # move up

      pipes_map[y][x] == "7" and is_from_below?(y, prev_y) ->
        move(pipes_map, {x-1, y}, [{x, y} | visited]) # move left

      pipes_map[y][x] == "7" and is_from_left?(x, prev_x) ->
        move(pipes_map, {x, y+1}, [{x, y} | visited]) # move down

      pipes_map[y][x] == "J" and is_from_above?(y, prev_y) ->
        move(pipes_map, {x-1, y}, [{x, y} | visited]) # move left

      pipes_map[y][x] == "J" and is_from_left?(x, prev_x) ->
        move(pipes_map, {x, y-1}, [{x, y} | visited]) # move up

      pipes_map[y][x] == "F" and is_from_below?(y, prev_y) ->
        move(pipes_map, {x+1, y}, [{x, y} | visited]) # move right

      pipes_map[y][x] == "F" and is_from_right?(x, prev_x) ->
        move(pipes_map, {x, y+1}, [{x, y} | visited]) # move down

      pipes_map[y][x] == "L" and is_from_above?(y, prev_y) ->
        move(pipes_map, {x+1, y}, [{x, y} | visited]) # move right

      pipes_map[y][x] == "L" and is_from_right?(x, prev_x) ->
        move(pipes_map, {x, y-1}, [{x, y} | visited])  # move up
    end
  )

  defp part1(pipes_map, starting_position), do: (
    IO.puts("Part 1 Solution:")
    total_steps = begin_moving(pipes_map, starting_position) |> length()
    total_steps / 2
  )

  defp is_contained_by?(pipes, {x, y}), do: (
    cond do
      {x, y} in pipes -> 0
      true ->
        pipes_before_x = pipes |> Enum.filter(fn({pipe_x, pipe_y}) -> pipe_y == y and pipe_x < x end) |> length()
        pipes_after_x = pipes |> Enum.filter(fn({pipe_x, pipe_y}) -> pipe_y == y and pipe_x > x end) |> length()
        pipes_before_y = pipes |> Enum.filter(fn({pipe_x, pipe_y}) -> pipe_x == x and pipe_y < y end) |> length()
        pipes_after_y = pipes |> Enum.filter(fn({pipe_x, pipe_y}) -> pipe_x == x and pipe_y > y end) |> length()
        cond do
          rem(pipes_before_x, 2) == 1 and rem(pipes_after_x, 2) == 1 -> 1
          # pipes_before_y > 0 and pipes_after_y > 0 and pipes_before_x > 0 and pipes_after_x > 0 -> 1
          true -> 0
        end
    end
  )

  defp part2(pipes_map, starting_position), do: (
    IO.puts("Part 2 Solution:")
    pipes_loop = begin_moving(pipes_map, starting_position)
    height = Map.size(pipes_map) - 1
    width = Map.size(pipes_map[0]) - 1
    Enum.map(0..height, fn(y) ->
      Enum.map(0..width, fn(x) -> is_contained_by?(pipes_loop, {x, y})
      end) |> Enum.sum()
    end) |> peek() |> Enum.sum()
  )
end

Day10.run()
