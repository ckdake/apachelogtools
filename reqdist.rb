require 'rubygems'
require 'file/tail'
require 'pp'

filename = "/var/log/apache2/access_log"

def max(data)
  max = 0
  data.each do |i|
    max = i if i && i > max
  end
  max
end

def printsummary(data, total)
  divide_by = (max(data) / 50) + 1
  
  data.each_index do |i|
    print "#{i * 100}ms to #{(i+1) * 100}ms: ".rjust(20)
    ((data[i] / divide_by) + 1).times { putc '#' } if data[i]
    print "\n"
  end
end

def matches_filters(filters, line)
  return true if filters.empty?
  filters.each do |f|
    return true if line.match(f)
  end
  return false
end

File.open(filename) do |log|
  starttime = lastprint = Time.now.to_i
  
  filters = []
  ARGV.each do |a|
    filters << a
  end
  
  # Data is array of buckets, index * 100 is number of ms to process request
  total = 0
  data = []
  
  log.extend(File::Tail)
  log.interval = 10
  log.backward(10)
  log.tail do |line|
    process = true
    
    if matches_filters(filters, line)
      reqtime = line.split(' ').last.to_i / 100000
      data[reqtime] = 0 unless data[reqtime]
      data[reqtime] += 1
      total += 1
    end
    
    if Time.now.to_i > lastprint + 5
      lastprint = Time.now.to_i
      printsummary(data, total)
    end
  end
end

