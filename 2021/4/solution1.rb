#!/usr/bin/ruby


class BingoCard 

	def initialize(card_contents)
		@card_contents = card_contents
	end

	def winning?
		# check for a winning row
		for i in 0 ... @card_contents.size do
			is_winning = true
			for n in  0 ... @card_contents[i].size do
				if @card_contents[i][n] != 'X'
					is_winning = false
					break
				end
			end
			return is_winning if is_winning
		end

		# check for a winning column
		for i in 0 ... @card_contents[0].size do
			is_winning = true
			for n in  0 ... @card_contents.size do
				if @card_contents[n][i] != 'X'
					is_winning = false
					break
				end
			end
			
			return is_winning if is_winning
		end
		return is_winning
	end

	def stamp_number(number)
		for i in 0 ... @card_contents.size do
			for n in  0 ... @card_contents[i].size do
				if @card_contents[i][n] == number
					@card_contents[i][n] = 'X'
					break
				end
			end
		end
	end

	def total()
		total = 0
		for i in 0 ... @card_contents.size do
			for n in  0 ... @card_contents[i].size do
				if @card_contents[i][n] != 'X'
					total += @card_contents[i][n].to_i
				end
			end
		end
		return total
	end

	def print()
		puts '--------------'
		for i in 0 ... @card_contents.size do
			puts @card_contents[i].join(' ')
		end
		puts '--------------'
	end
end


f_in = File.open(ARGV[0])
contents = f_in.readlines.map(&:chomp)
contents.push('')  # chomp is removing my last empty line, but I use it to detect the end of a card


call_numbers = contents[0].split(',')

# Build out the cards
cards = Array.new
current_card_contents = Array.new

for line in contents[2, contents.size + 1] do
	if line == '' or !line
		cards.push(BingoCard.new(current_card_contents))
		current_card_contents = Array.new
	elsif
		current_card_contents.push(line.split(' '))
	end
end

# cards.map { |card| card.print }

# puts "Part 1"
# for call_number in call_numbers do
# 	cards.map { |card| card.stamp_number(call_number) }
# 	for card in cards do
# 		puts call_number
# 		if card.winning?
# 			card.print
# 			puts card.total * call_number.to_i
# 		end
# 	end
# end

puts "Part 2"
losing_cards = cards
for call_number in call_numbers do
	losing_cards.map { |card| card.stamp_number(call_number) }
	for card in losing_cards do
		puts call_number
		if losing_cards.size > 1 and card.winning?
			losing_cards.delete(card)
		elsif card.winning?
			puts card.total * call_number.to_i
			return
		end
	end

end


f_in.close
