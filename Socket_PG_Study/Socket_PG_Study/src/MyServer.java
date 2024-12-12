import java.io.IOException;	//오류 처리
import java.io.PrintWriter;		//getOutputStream()을 처리
import java.net.ServerSocket;	// ServerSocket
import java.net.Socket;			// ConnectionSocket
import java.util.ArrayList;		//client의 OutputStream을 저장하는 List를 생성하기 위해 import

public class MyServer{
	public static ArrayList<PrintWriter> m_outputList;
    
    public static void main(String[] args){
    	m_outputList = new ArrayList<PrintWriter>();
        
        try{
        	ServerSocket s_socket = new ServerSocket(8000);

            while(true){
                Socket c_socket = s_socket.accept();
                ClientManagerThread c_Thread = new ClientManagerThread();
                c_Thread.setSocket(c_socket);

                m_outputList.add(new PrintWriter(c_socket.getOutputStream()));
                c_Thread.start();
                
            }


        }catch(IOException e){
            e.printStackTrace();
        }

    }
}