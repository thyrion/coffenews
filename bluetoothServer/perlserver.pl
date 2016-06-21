use Net::Bluetooth;
use LWP::Simple qw(get);
use strict;


my $url = 'http://192.168.2.56:8080/news';

 
#### create a RFCOMM server
my $obj = Net::Bluetooth->newsocket("RFCOMM");
#### bind to port 1
if($obj->bind(1) != 0) {
      die "bind error: $!\n";
}
 
#### listen with a backlog of 2
if($obj->listen(2) != 0) {
      die "listen error: $!\n";
}
 
#### register a service
#### $obj must be a open and bound socket
my $service_obj = Net::Bluetooth->newservice($obj, "00001101-0000-1000-8000-00805F9B34FB", "Test", "Test");  
unless(defined($service_obj)) {
      #### couldn't register service
}
 
print "waiting for client connections...\n";
 
while (1) {
  #### accept a client connection
  #### blocks here until a client connects
  my $client_obj = $obj->accept();
  unless(defined($client_obj)) {
        die "client accept failed: $!\n";
  }
 
  #### create a Perl filehandle for reading and writing
  my $client = $client_obj->perlfh();
 
  my $data;
  my $bytesRead;
    
    my $html = get $url;
 
  #while (1) {
	#$bytesRead = sysread $client, $data, 80;
	#print "bytesRead: $bytesRead, data: $data\n";
	#$data = "Echo: $data ";
	syswrite $client, $html;
    #}
	
  close ($client);
}
 
#### stop advertising service
$service_obj->stopservice();
#### close server connection
$obj->close();