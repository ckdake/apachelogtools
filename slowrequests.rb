require 'rubygems'
require 'file/tail'
require 'pp'

filename = "/var/log/apache2/access_log"

File.open(filename) do |log|
  log.extend(File::Tail)
  log.interval = 10
  log.backward(10)
  log.tail do |line|
    reqtime = line.split(' ').last.to_f / 1000000.0
    print format("%.4fs: #{line}", reqtime) if reqtime > 1
  end
end