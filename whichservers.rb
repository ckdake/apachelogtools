=begin
= NAME
whichservers - A tool to see which servers requests for a given vhost are arriving at

=end 

require 'rubygems'
require 'file/tail'
require 'pp'

filename = "/var/log/remote_httpd/access_log"

$linecount = 0
$vhosts = Hash.new
$maxhostlen = 0
$servers = Hash.new
$filters = Array.new

def printvhost(name,servercounts)
  if not $filters.empty?
    if not $filters.include?(name)
      return nil
    end
  end 
  print name.ljust($maxhostlen) + "|"
  $servers.each { |server|
    if servercounts.has_key?(server[0])
      print "%#{7}.d" % servercounts[server[0]]
    else
      print "#{" "*7}"
    end
   print '|'
  }
  print "\n"
end

def printsummary
  # servers is used for column headings
  print "#{" "*$maxhostlen}|"
  $servers.each { |server|  
    print server[0][5..server[0].length].rjust(7)
    print "|"
  }
  print "\n"
  $vhosts.each_pair { |name,servercounts| printvhost(name,servercounts) } 
  print "\n"
end

def processline(logline)
  ar = logline.split(" ")
  hostname = ar[5]
  serverip = ar[3] 

  $linecount += 1

  if not $vhosts.has_key?(hostname)
    $vhosts[hostname] = Hash.new
    if hostname.length > $maxhostlen
       $maxhostlen = hostname.length
    end
  end

  if !$vhosts[hostname].has_key?(serverip)
    $vhosts[hostname][serverip] = 1
  else
    $vhosts[hostname][serverip] = $vhosts[hostname][serverip] + 1
  end

  if !$servers.has_key?(serverip)
    $servers[serverip] = 1
  else 
    $servers[serverip] = $servers[serverip] + 1
  end
  
  if $linecount % 100 == 0
    printsummary
  end
end

def grouptail(filename)
  File.open(filename) do |log|
    log.extend(File::Tail)
    log.interval = 10
    log.backward(10)
    log.tail { |line| processline line }
  end
end

ARGV.each do |a|
  $filters << a
end   

grouptail(filename)
