# This is client code to receive video and audio frames over UDP
import socket
import threading, wave, pyaudio, time, queue
import sys,select,webbrowser

host_name = socket.gethostname()
host_ip = '192.168.1.2'#  socket.gethostbyname(host_name)
print(host_ip)
port = 9633
BUFF_SIZE = 65536

q = queue.Queue(maxsize=100)
try:
    def audio_stream_UDP():
        client_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        client_socket.setsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF,BUFF_SIZE)
        p = pyaudio.PyAudio()
        CHUNK = 10*1024
        stream = p.open(format=p.get_format_from_width(2),
					    channels=2,
					    rate=44100,
					    output=True,
					    frames_per_buffer=CHUNK)
        message = b'Hello'
        client_socket.sendto(message,(host_ip,port))
        socket_address = (host_ip,port)
	
        def getAudioData():
		        while (q.qsize() < 57):
			        frame,_= client_socket.recvfrom(BUFF_SIZE)
			        q.put(frame)
			        
        t1 = threading.Thread(target=getAudioData, args=())
        t1.start()
        time.sleep(5)
        print('Now Playing...')
        while (q.qsize() < 57):
            frame = q.get()
            stream.write(frame)
        client_socket.close()
        
        port_id = 9999
        s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        s.bind((host_ip,port_id))
        buf = 1024
        addr = (host_ip,port_id)
        data,addr = s.recvfrom(buf)
        print("Received File:",data.strip())
        f = open ("data.strip()",'wb')
        print("location of user receiving strsrted")
        data,addr = s.recvfrom(buf)
        try:
            while(data):
                f.write(data)
                s.settimeout(2)
                data,addr = s.recvfrom(buf)
        except:
            f.close()
            s.close()
            print ("File Downloaded")
            webbrowser.open_new_tab('Location.html')
        
    t1 = threading.Thread(target=audio_stream_UDP, args=())
    t1.start()
except:
    pass
