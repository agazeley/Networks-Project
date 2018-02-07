using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Net.Sockets;
using System.Diagnostics;
using Newtonsoft.Json;

namespace Battleship_Client
{
    class Client
    {
        private int server_port;
        private string server_ip;
        private int msg_size = 2048;
        private UdpClient client;

        public Client()
        {
            this.client = new UdpClient();
        }

        public Client(string ip,int port)
        {
            this.client = new UdpClient();
            this.server_ip = ip;
            this.server_port = port;
        }

        public bool start_client(string name)
        {
            Debug.WriteLine("Connecting to " + this.server_ip + ": " + this.server_port.ToString());
            string data = create_request(name, "connect", "1");

            if (send(data, this.server_ip, this.server_port))
            {
                return true;
            }
            else
            {
                return false;
            }
        }
        public bool send(string data)
        {
            byte[] byte_data = Encoding.ASCII.GetBytes(data);
            try
            {
                this.client.Send(byte_data, byte_data.Length);
                return true;
            }
            catch(Exception e)
            {
                Debug.WriteLine(e.Message);
                return false;
            }
        }

        public bool send(string data,string ip,int port)
        {
            byte[] byte_data = Encoding.ASCII.GetBytes(data);
            try
            {
                this.client.Send(byte_data, byte_data.Length, ip, port);
                return true;
            }
            catch(Exception e)
            {
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

    }
}
