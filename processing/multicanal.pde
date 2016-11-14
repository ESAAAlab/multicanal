import hypermedia.net.*;
import processing.sound.*;

UDP udp;
SoundFile file;
int id = 0;

void setup() {
  background(0);
  String[] c = loadStrings("config.txt");
  id = Integer.parseInt(c[0]);
  file = new SoundFile(this, "mp3/sound_"+id+".mp3");
  udp = new UDP(this, 55056);
  udp.listen(true);
}

void draw() {
  
}

void receive( byte[] data, String ip, int port ) {
  String message = new String(data);
  if (Integer.parseInt(message)==id) {
    file.play();
  } else {
    file.stop();
  }
}