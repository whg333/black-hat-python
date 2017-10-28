package ch02;

import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.net.ServerSocket;
import java.net.Socket;

public class TcpServer {

	public static void main(String[] args) throws IOException {
		String ip = "0.0.0.0";
		int port = 9999;
		
		ServerSocket server = new ServerSocket(port, 5);
		System.out.printf("[*] Listeneing on %s:%d\n", server.getInetAddress().getHostAddress(), server.getLocalPort());
		
		while(true){
			Socket client = server.accept();
			System.out.printf("[*] Accepted connection from: %s:%d\n", client.getInetAddress().getHostAddress(), client.getPort());
			
			ClientHandler clientHandler = new ClientHandler(client);
			clientHandler.start();
		}
	}
	
	private static final class ClientHandler extends Thread{
		private final Socket client;
		public ClientHandler(Socket client) {
			this.client = client;
		}
		@Override
		public void run() {
			try {
				InputStream in = client.getInputStream();
				OutputStream out = client.getOutputStream();
				
				byte[] readBuf = new byte[1024];
				in.read(readBuf);
				System.out.printf("[*] Reveived: %s\n", new String(readBuf));
				out.write("ACK!".getBytes());
				
				in.close();
				out.close();
				client.close();
			} catch (Exception e) {
				e.printStackTrace();
			}
		}
	}
	
}
