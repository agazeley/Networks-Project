using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Net.Sockets;
using System.Diagnostics;
using Newtonsoft.Json;
using System.Net;

namespace Battleship_Client
{
    public class Client
    {
        private int server_port;
        private IPAddress server_ip;
        private UdpClient client;
        private IPEndPoint ep_server;

        public Client()
        {
            this.client = new UdpClient();
        }
        public Client(string ip,int port)
        {
                this.client = new UdpClient();

            if (ip.ToLower() == "localhost")
            {
                this.server_ip = IPAddress.Parse("127.0.0.1");
                this.ep_server = new IPEndPoint(this.server_ip, port);
            }
            else
            {
                this.server_ip = IPAddress.Parse(ip);
                this.ep_server = new IPEndPoint(this.server_ip, port);
            }
            this.server_port = port;

        }

        public bool start_client(string name)
        {
            Debug.WriteLine("Connecting to " + this.server_ip + ": " + this.server_port.ToString());
            string data = create_request(name, "connect", "1");
            byte[] byte_data = Encoding.ASCII.GetBytes(data);

            try
            {
                // this.sock.SendTo(byte_data,this.ep_server);
            }
            catch (Exception e)
            {
                Debug.WriteLine("Start error");
                Debug.WriteLine(e.Message);
                return false;
            }
            string json = "";

            while(json == "")
            {
                json = this.get_reply();

            }
            var msg = JsonConvert.DeserializeObject<Dictionary<string, string>>(json);

            if (msg["type"] == "conn_request" && int.Parse(msg["msg"]) == 1)
            {

                Debug.WriteLine("Successful connection!");
                // Successful handshake!
                return true;
            }
            else
            {

                Debug.WriteLine("Failed to start :/");
                // exit(0)?
                return false;
            }
        }

        public bool send(string data)
        {

            byte[] byte_data = Encoding.ASCII.GetBytes(data);
            try
            {
                // this.sock.SendTo(byte_data,this.ep_server);
                return true;
            }
            catch(Exception e)
            {
                Debug.WriteLine("Send 1 error");
                Debug.WriteLine(e.Message);
                return false;
            }
        }

        public bool send(string data,IPEndPoint ep)
        {
            byte[] byte_data = Encoding.ASCII.GetBytes(data);
            try
            {
                // this.sock.SendTo(byte_data, ep);
                return true;
            }
            catch(Exception e)
            {
                Debug.WriteLine("Send 2 error");
                Debug.WriteLine(e.Message);
                return false;
            }
        }

        public bool server_request(string data)
        {
            byte[] byte_data = Encoding.ASCII.GetBytes(data);

            try
            {
                // this.sock.SendTo(byte_data,this.ep_server);
                return true;
            }
            catch(Exception e)
            {

                Debug.WriteLine("Server req error");
                Debug.WriteLine(e.Message);
                return false;
            }
        }


        // Need to make it so id is optional field
        public string create_request(string player, string type,string req, int id)
        {
            Dictionary<string, string> data = new Dictionary<string, string>();

            if(id != null)
            {
                data["game_id"] = id.ToString();
            }

            data["player"] = player;
            data["req_type"] = type;
            data["req"] = req;
            return JsonConvert.SerializeObject(data);
        }

        public string create_request(string player, string type, string req)
        {
            Dictionary<string, string> data = new Dictionary<string, string>();
            data["player"] = player;
            data["req_type"] = type;
            data["req"] = req;
            return JsonConvert.SerializeObject(data);
        }

        public string get_reply()
        {
            try
            {
                byte[] bytes = new byte[1024];
                // string reply = this.sock.Receive(bytes).ToString();
                // return reply;
                return "";
            }
            catch (Exception e)
            {
                Debug.WriteLine("Reply error");
                Debug.WriteLine(e.Message);
                return "";
            }

        }
    }
}
