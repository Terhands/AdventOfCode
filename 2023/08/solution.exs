# See: https://adventofcode.com/2023/day/7

defmodule Day8 do

  defp peek(value), do: IO.inspect(value, charlist: :as_list)

  defp parse_instructions(instruction_line), do: (
    instruction_line
    |> String.graphemes()
    |> Enum.with_index()
    |> Enum.map(fn({val, index}) -> {index, val} end)
    |> Map.new()
  )
  defp parse_position(position_line), do: (
    [key, left_key, right_key] = position_line
    |> String.replace("=", "") |> String.replace("(", "") |> String.replace(")", "") |> String.replace(",", "") |> String.replace("=", "") |> String.replace("  ", " ")
    |> String.split(" ")
    {key, {left_key, right_key}}
  )
  defp parse_map_data(map_data_str), do: (
    map_data_str
    |> Enum.map(&parse_position/1)
    |> Map.new()
  )

  def run, do: (
    filename = "sample1.txt"
    filename = "sample2.txt"
    filename = "input.txt"
    {:ok, contents} = File.read(filename)
    [instructions_str | map_data_strs] = contents |> String.split("\n", trim: true) |> Enum.filter(fn(val) -> val != "" end)
    instructions = parse_instructions(instructions_str) #|> peek()
    map_data = parse_map_data(map_data_strs) #|> peek()

    part1(map_data, instructions) |> IO.puts()
    part2(map_data, instructions) |> IO.puts()
  )

  defp steps_to_exit(desert_map, instructions, current_desert_position, current_step), do: (
    case current_desert_position do
      "ZZZ" -> current_step
      _ ->
        instruction = instructions[rem(current_step, map_size(instructions))]
        next_position = move(instruction, desert_map[current_desert_position])
        # peek("From #{current_desert_position}, moving #{instruction}, lands at: #{next_position}")
        steps_to_exit(desert_map, instructions, next_position, current_step + 1)
    end
  )
  defp move(instruction, {left, right}), do: (
    case instruction do
      "R" -> right
      "L" -> left
    end
  )

  defp part1(desert_map, instructions), do: (
    IO.puts("Part 1 Solution:")
    steps_to_exit(desert_map, instructions, "AAA", 0)
  )

  defp part2(desert_map, instructions), do: (
    IO.puts("Part 2 Solution:")
  )
end

Day8.run()
