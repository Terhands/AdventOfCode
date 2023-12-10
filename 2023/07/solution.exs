# See: https://adventofcode.com/2023/day/7

defmodule Day7 do

  defp peek(value), do: IO.inspect(value, charlist: :as_list)

  defp to_camel_hand(data), do: (
    [hand, bid_str] = data |> String.split(" ", trim: true)
    {hand, String.to_integer(bid_str)}
  )

  def run, do: (
    filename = "sample.txt"
    filename = "input.txt"
    {:ok, contents} = File.read(filename)
    hand_data = contents |> String.split("\n") |> Enum.map(&to_camel_hand/1)
    part1(hand_data) |> IO.puts()
    part2(hand_data) |> IO.puts()
  )

  defp hand_strength({hand, _}), do: (
    case Enum.sort(String.split(hand, "", trim: true)) do
      [v, v, v, v, v] -> 7
      [v, v, v, v, _] -> 6
      [_, v, v, v, v] -> 6
      [v, v, v, x, x] -> 5
      [v, v, x, x, x] -> 5
      [v, v, v, _, _] -> 4
      [_, v, v, v, _] -> 4
      [_, _, v, v, v] -> 4
      [v, v, x, x, _] -> 3
      [_, v, v, x, x] -> 3
      [v, v, _, x, x] -> 3
      [v, v, _, _, _] -> 2
      [_, v, v, _, _] -> 2
      [_, _, v, v, _] -> 2
      [_, _, _, v, v] -> 2
      _ -> 1
    end
  )

  defp cards_strength({hand, _}), do: (
    hand
    |> String.split("", trim: true)
    |> Enum.map(fn (card) ->
      case card do
        "A" -> 14
        "K" -> 13
        "Q" -> 12
        "J" -> 11
        "T" -> 10
        _ -> String.to_integer(card)
      end
    end)
  )

  defp part1(hand_data), do: (
    IO.puts("Part 1 Solution:")
    # peek(hand_data)
    hand_data
    |> Enum.sort_by(&cards_strength/1)
    |> Enum.sort_by(&hand_strength/1)
    |> Enum.with_index(1)
    |> Enum.map(fn({{hand, bid}, rank}) -> bid * rank end)
    |> Enum.sum()
  )

  defp most_common_char(str), do: (
    case Enum.sort(String.split(str, "", trim: true)) do
      [v, v, v, v] -> v
      [v, v, v, _] -> v
      [_, v, v, v] -> v
      [v, v, _, _] -> v
      [_, v, v, _] -> v
      [_, _, v, v] -> v
      [v, _, _, _] -> v
      [v, v, v] -> v
      [v, v, _] -> v
      [_, v, v] -> v
      [v, _, _] -> v
      [v, v] -> v
      [v, _] -> v
      [v] -> v
      [] -> "J"
    end
  )

  defp hand_strength2({hand, bid}), do: (
    best_hand = cond do
      String.contains?(hand, "J") ->
        jless = String.replace(hand, "J", "")
        String.replace(hand, "J", most_common_char(jless))
      true -> hand
    end #|> peek()
    hand_strength({best_hand, bid})
  )

  defp cards_strength2({hand, bid}), do: (
    cards_strength({hand, bid})
    |> Enum.map(fn(val) ->
      case val do
        11 -> 0
        x -> x
      end
    end)
  )

  defp part2(hand_data), do: (
    IO.puts("Part 2 Solution:")
    hand_data
    |> Enum.sort_by(&cards_strength2/1)
    |> Enum.sort_by(&hand_strength2/1)
    |> Enum.with_index(1)
    |> Enum.map(fn({{hand, bid}, rank}) -> bid * rank end)
    |> Enum.sum()
  )
end

Day7.run()
