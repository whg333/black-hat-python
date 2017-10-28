package ch02;

import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.net.Socket;
import java.net.UnknownHostException;

public class TcpClient {

	public static void main(String[] args) throws UnknownHostException, IOException {
		String host = "127.0.0.1";
		int port = 9999;
		
		Socket client = new Socket(host, port);
		InputStream in = client.getInputStream();
		OutputStream out = client.getOutputStream();
		
		out.write("ABCDEF".getBytes());
		byte[] readBuf = new byte[1024];
		in.read(readBuf);
		System.out.println(new String(readBuf));
		
		in.close();
		out.close();
		client.close();
	}
	
}
