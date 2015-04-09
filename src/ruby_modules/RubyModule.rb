

class RubyModule
  def initialize
    #turns send data from Beastbots into args for use in ruby script
    @args = STDIN.gets.split(":")
  end
  
  def send_to_channel(text)
    puts "channel:" + text
  end

  def send_to_user(text)
    puts "user:" + text
  end
  
end

puts "I'm the ruby module file. I contain handy functions to interface with Beastbot"