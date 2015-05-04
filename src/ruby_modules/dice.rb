#!/usr/bin/env ruby

# This script throws the dice
#
# Author: Lenoch


require 'beastbot'

def throw(sides)
  value = Random.rand(sides)
  return value.to_s
end

sides = Beastbot::Interpret::get_arguments

if sides.to_i > 0
  val = throw(sides.to_i)
  Beastbot::Talk::send_to_channel("Throws " + val)
  Beastbot::Talk::send_to_user("Throws " + val)
else 
  Beastbot::Talk::send_to_channel("Give a number of sides or a number of sides greater then 0")
end

