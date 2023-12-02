# Question:
# --- Day 1: Trebuchet?! ---

# Something is wrong with global snow production, and you've been selected to take a look. The Elves have even given you a map; on it,
# they've used stars to mark the top fifty locations that are likely to be having problems.

# You've been doing this long enough to know that to restore snow operations, you need to check all fifty stars by December 25th.

# Collect stars by solving puzzles. Two puzzles will be made available on each day in the Advent calendar; the second puzzle is
# unlocked when you complete the first. Each puzzle grants one star. Good luck!

# You try to ask why they can't just use a weather machine ("not powerful enough") and where they're even sending you ("the sky")
# and why your map looks mostly blank ("you sure ask a lot of questions") and hang on did you just say the sky ("of course,
# where do you think snow comes from") when you realize that the Elves are already loading you into a trebuchet
# ("please hold still, we need to strap you in").

# As they're making the final adjustments, they discover that their calibration document (your puzzle input) has been amended
# by a very young Elf who was apparently just excited to show off her art skills. Consequently, the Elves are having trouble reading
# the values on the document.

# The newly-improved calibration document consists of lines of text; each line originally contained a specific calibration value
# that the Elves now need to recover. On each line, the calibration value can be found by combining the first digit and the last digit
# (in that order) to form a single two-digit number.

filename = "part1-data.txt"
# filename = "part1-sample1.txt"
# filename = "part2-sample.txt"
{:ok, contents} = File.read(filename)

IO.puts "Part 1 Solution:"

to_sum_strs = String.replace(contents, ~r/[[:alpha:]]/, "") |> String.split("\n", trim: true) |> Enum.map(fn (l) -> String.graphemes(l) end) |> Enum.map(fn(digit_list) -> hd(digit_list) <> hd(Enum.reverse(digit_list)) end)
Enum.sum(Enum.map(to_sum_strs, &String.to_integer/1)) |> IO.puts

# --- Part Two ---

# Your calculation isn't quite right. It looks like some of the digits are actually spelled out with letters: one, two, three, four,
# five, six, seven, eight, and nine also count as valid "digits".

# Equipped with this new information, you now need to find the real first and last digit on each line. For example:

# two1nine
# eightwothree
# abcone2threexyz
# xtwone3four
# 4nineeightseven2
# zoneight234
# 7pqrstsixteen

# In this example, the calibration values are 29, 83, 13, 24, 42, 14, and 76. Adding these together produces 281.

# What is the sum of all of the calibration values?


IO.puts "Part 2 Solution:"
# A quick search of the data and it only contains one through nine as alpha digits to be converted. No need to worry about the teens, etc.
defmodule Part2 do
  def sanitize_input(input_str), do: (
    # We'll replace any numeric words that we care about with digits.
    result = String.replace(input_str, "twone", "21") |>
    String.replace("oneight", "18") |>
    String.replace("eightwo", "82") |>
    String.replace("eighthree", "83") |>
    String.replace("threeight", "38") |>
    String.replace("fiveight", "58") |>
    String.replace("nineight", "98") |>
    String.replace("sevenine", "79") |>
    String.replace("one", "1") |>
    String.replace("two", "2") |>
    String.replace("three", "3") |>
    String.replace("four", "4") |>
    String.replace("five", "5") |>
    String.replace("six", "6") |>
    String.replace("seven", "7") |>
    String.replace("eight", "8") |>
    String.replace("nine", "9") |>
    String.replace(~r/[[:alpha:]]/, "")
  )

  def first_and_last(digits), do: (
    hd(digits) <> hd(Enum.reverse(digits))
  )
end

part_two_to_sum = (
  String.split(contents, "\n", trim: true) |>
  # IO.inspect |>
  Enum.map(&Part2.sanitize_input/1) |>
  # IO.inspect |>
  Enum.map(fn (l) -> String.graphemes(l) end) |>
  Enum.map(&Part2.first_and_last/1) |>
  IO.inspect
)
Enum.sum(Enum.map(part_two_to_sum, &String.to_integer/1)) |> IO.puts
