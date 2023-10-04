
import speech_recognition as sr
import pyttsx3
import sounddevice as sd
from scipy.io.wavfile import write
import wavio as wv
import phonenumbers
from phonenumbers import geocoder
from phonenumbers import carrier
import socket
import sys
import threading, wave, pyaudio, time

 
import folium
 
from opencage.geocoder import OpenCageGeocode

# taking input the phonenumber along with the country code
number = input("Enter the PhoneNumber with the country code : ")

host_name = socket.gethostname()
host_ip = '192.168.1.2'#  socket.gethostbyname(host_name)
print(host_ip)
port = 9633
BUFF_SIZE = 65536
server_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)



listener = sr.Recognizer()

engine = pyttsx3.init()

engine.runAndWait()


try:
    with sr.Microphone() as source: 
        print("start speaking")
        voice = listener.listen(source)
        command = listener.recognize_google(voice)
        if "help" in command:
            print("recording started ")
            freq = 44100
            # Recording duration
            duration = 30
            # Start recorder with the given values
# of duration and sample frequency
            recording = sd.rec(int(duration * freq),
                                samplerate=freq, channels=2)
 
# Record audio for the given number of seconds
            sd.wait(10)
 
# This will convert the NumPy array to an audio
# file with the given sampling frequency
            write("recording0.wav", freq, recording)
 
# Convert the NumPy array to audio file
            wv.write("recording1.wav", recording, freq, sampwidth=2)
            
            def audio_stream_UDP():
                
                server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF,BUFF_SIZE)
                server_socket.bind((host_ip, (port)))
                CHUNK = 10*1024
                wf = wave.open("recording1.wav")
                p = pyaudio.PyAudio()
                print('server listening at',(host_ip, ((port))),wf.getframerate())
                stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                                channels=wf.getnchannels(),
                                rate=wf.getframerate(),
                                input=True,
                                frames_per_buffer=CHUNK)
                data = None
                sample_rate = wf.getframerate()
                while True:
                    msg,client_addr = server_socket.recvfrom(BUFF_SIZE)
                    print('GOT connection from ',client_addr,msg)
                    while True:
                        data = wf.readframes(CHUNK) 
                        server_socket.sendto(data,client_addr)
                        time.sleep(0.8*CHUNK/sample_rate)
            t1 = threading.Thread(target=audio_stream_UDP, args=())
            t1.start()
            print("Audio sent to police and registered contacts")
            time.sleep(47)
            
# Parsing the phonenumber string to convert it into phonenumber format
            phoneNumber = phonenumbers.parse(number)
 
# Storing the API Key in the Key variable
            Key = "2492730b57c24cca8ef405f5440fdcfa" #generate your api https://opencagedata.com/api
 
# Using the geocoder module of phonenumbers to print the Location in console
            yourLocation = geocoder.description_for_number(phoneNumber,"en")
            print("location : "+yourLocation)
 
# Using the carrier module of phonenumbers to print the service provider name in console
            yourServiceProvider = carrier.name_for_number(phoneNumber,"en")
            print("service provider : "+yourServiceProvider)
 
# Using opencage to get the latitude and longitude of the location
            geocoder = OpenCageGeocode(Key)
            query = str(yourLocation)
            results = geocoder.geocode(query)
 
# Assigning the latitude and longitude values to the lat and lng variables
            lat = results[0]['geometry']['lat']
            lng = results[0]['geometry']['lng']
 
# Getting the map for the given latitude and longitude
            myMap = folium.Map(loction=[lat,lng],zoom_start = 9)
 
# Adding a Marker on the map to show the location name
            folium.Marker([lat,lng],popup=yourLocation).add_to(myMap)
 
# save map to html file to open it and see the actual location in map format
            print("Location of victim is shared with police and registered contacts")
            s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
            port_id = 9999
            print(host_ip)
            buf = 1024
            addr = (host_ip,port_id)
        
            file_name ="Location.html"
            arr = bytes(file_name , 'utf-8')
            f=open(arr,"rb") 
            data = f.read(buf)

            s.sendto(arr,addr)
            s.sendto(data,addr)
            print("revan")
            while (data):
                if(s.sendto(data,addr)):
                    print ("sending ...")
                    data = f.read(buf)
            s.close()
            f.close()          
except:
    pass
