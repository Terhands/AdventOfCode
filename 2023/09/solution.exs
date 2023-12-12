# See: https://adventofcode.com/2023/day/9

defmodule Day9 do

  defp peek(value), do: IO.inspect(value, charlist: :as_list)

  defp to_sequence(seqeuence_str), do: (
    String.split(seqeuence_str, " ", trim: true) |> Enum.map(&String.to_integer/1)
  )

  def run, do: (
    filename = "sample1.txt"
    filename = "input.txt"
    {:ok, contents} = File.read(filename)
    sequences = String.split(contents, "\n", trim: true) |> Enum.map(&to_sequence/1)

    part1(sequences) |> IO.puts()
    part2(sequences) |> IO.puts()
  )

  defp is_done?(sequence), do: (
    sequence |> Enum.filter(fn(value) -> value != hd(sequence) end) |> length() == 0
  )
  defp calculate_next_value(sequence), do: (
    is_done?(sequence)
    cond do
      is_done?(sequence) -> [hd(sequence) | sequence]
      true ->
        curr = sequence |> Enum.chunk_every(2, 1, :discard) |> Enum.map(fn([v1, v2]) -> v2 - v1 end) #|> peek()
        next = calculate_next_value(curr)
        [hd(sequence)] ++ (Enum.zip(sequence, next) |> Enum.map(fn({v1, diff}) -> v1 + diff end))
    end
  )

  defp part1(sequences), do: (
    IO.puts("Part 1 Solution:")
    sequences
    |> Enum.map(&calculate_next_value/1)
    |> Enum.map(fn(l) -> hd(Enum.reverse(l)) end)
    |> Enum.sum()
  )

  defp part2(sequences), do: (
    IO.puts("Part 2 Solution:")
    sequences
    |> Enum.map(fn(l) -> Enum.reverse(l) end)
    |> Enum.map(&calculate_next_value/1)
    |> Enum.map(fn(l) -> hd(Enum.reverse(l)) end)
    |> Enum.sum()
  )
end

Day9.run()
