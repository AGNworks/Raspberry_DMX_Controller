#include <DMXSerial.h>
#include <Wire.h>

#define LEDpin 4 //just for the test mode

int sizeofdata = 3 ;
byte strip_type = 3;  // 3-RGB , 4-RGBW
byte mode = 0; //sima uzemmode vagy folyamatos modok hasznalata
byte func = 0;
byte value = 0;

byte i = 0;


int data[3];
int x=0;

//------------------------------------------------------------------------------------------------------------------------SETUP
void setup() 
{
  DMXSerial.init(DMXController);

  Wire.begin(0x20);
  Wire.onReceive(receiveEvent); //RecieveEvent

  pinMode(LEDpin, OUTPUT);
  digitalWrite(LEDpin, HIGH);
  delay(1000);
  digitalWrite(LEDpin, LOW);
 
  pinMode(LEDpin, OUTPUT);

  for (int i=0 ; i < 2; i++)
   {
    data[i] = 0;
   }
} 


//------------------------------------------------------------------------------------------------------------------------RecieveEvent
void receiveEvent(int howmany)
{
  while (Wire.available())
  {
    digitalWrite(LEDpin, HIGH);
    data[x]= Wire.read();
    x++;
    if(x==sizeofdata) { x=0;}  
    digitalWrite(LEDpin, LOW);
  }
}


//------------------------------------------------------------------------------------------------------------------------LOOP
void loop() 
{
   mode = data[0];
   func = data[1];
   value = data[2];
  
   if (data[0] == 0 && data[1] == 0)   // all OFF
    {
      turn_all_off();
    }
    
   if (data[0] == 0 && data[1] == 1)  // all ON
    {
      turn_all_on();
    }

   if (data[0] == 0 && data[1] == 2)  // all red
    {
      turn_color("red", 255);
    }

   if (data[0] == 0 && data[1] == 3)  // all green
    {
      turn_color("green", 255);
    }

   if (data[0] == 0 && data[1] == 4) // all blue
    {
      turn_color("blue", 255);
    }

   if (data[0] == 0 && data[1] == 5)  // all white, but just if it's in RGBW mode
    {
      turn_color("white", 255);
    }

   if (data[0] == 0 && data[1] == 6) //HA ATVALTOTT RGB MODRA
    {
      strip_type = 3;
    }

   if (data[0] == 0 && data[1] == 7)  //HA ATVALTOTT RGBW MODRA
    {
      strip_type = 4;
    }
    
//-----------------------------------------------------------------------------------------------------------------------------------Decoder funkciok
   if (data[0] == 1 && data[1] == 2)  // decoder red
    {
      DMXSerial.write(((value-1)*strip_type + 1), 255);
    }

   if (data[0] == 1 && data[1] == 3)  // decoder green
    {
      DMXSerial.write(((value-1)*strip_type + 2), 255);
    }

   if (data[0] == 1 && data[1] == 4) // decoder blue
    {
     DMXSerial.write(((value-1)*strip_type + 3), 255);
    }

   if (data[0] == 1 && data[1] == 5 && strip_type == 4)  // decoder all white but just if it's in RGBW mode
    {
     DMXSerial.write(((value-1)*strip_type + 4), 255);
    }

//-----------------------------------------------------------------------------------------------------------------------------------Channel control
   if (data[0] == 2)
    {
      DMXSerial.write(func, value);
    }
    
//-----------------------------------------------------------------------------------------------------------------------------------Scene control
    if (data[0] == 3 && data[1] == 1)
      {
        String color = "red" ;
        i =0;
        while (data[1] != 0 )
         {
          turn_color(color, i);
          delay(100);
          receiveEvent(5);
          i ++;
       
            if (color == "red" && i == 255)
             {
              color = "green";
              i = 0;
             }
            else if (color == "green" && i == 255)
             {
              color = "blue";
              i = 0;
             }
            else if (color == "blue" && i == 255)
             {
              turn_all_off();
              color = "red";
              i = 0;
             }
           
          if (data[1] == 0)
            {
              turn_all_off();
              break;
            }
          }
         
      }

      
} //end of LOOP




//------------------------------------------------------------------------------------------------------------------------turn_all_on
void turn_all_on()
{
    for (int i = 0; i < 512; i++)
   {
    DMXSerial.write(i+1, 255);
   }
}


//------------------------------------------------------------------------------------------------------------------------turn_all_off
void turn_all_off()
{
    for (int i = 0; i < 512; i++)
   {
    DMXSerial.write(i+1, 0);
   }
}

//------------------------------------------------------------------------------------------------------------------------turn_color
void turn_color(String color, byte bright)
{
  if (color  == "red")
  {
    for (int i = 0; i < 512; i+= strip_type )
     {
      DMXSerial.write(i+1,bright);
     }
  }
  
 if (color  == "green")
  {
    for (int i = 1; i < 512; i+= strip_type )
     {
      DMXSerial.write(i+1, bright);
     }
  }

  if (color  == "blue")
  {
    for (int i = 2; i < 512; i+= strip_type )
     {
      DMXSerial.write(i+1, bright);
     }
  }

  if (color  == "white" && strip_type == 4 )
  {
    for (int i = 3; i < 512; i+= strip_type )
     {
      DMXSerial.write(i+1, bright);
     }
  }
}


//------------------------------------------------------------------------------------------------------------------------scene_one
