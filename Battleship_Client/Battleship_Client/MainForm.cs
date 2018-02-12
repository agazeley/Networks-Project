using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Newtonsoft.Json;
using System.Windows.Forms;
using System.Diagnostics;
using Newtonsoft.Json.Linq;

namespace Battleship_Client
{
    public partial class MainForm : Form
    {
        private User usr { get; set; }
        private Client my_client { get; set; }

        public MainForm(User usr, Client my_client)
        {
            this.my_client = my_client;
            this.usr = usr;

            InitializeComponent();

            string req = Client.create_request(usr.name, "data", usr.name);
            my_client.server_request(req);
            Message some = GetMessage();

            if(some.type == InfoType.LobbyData)
            {
                List<Tuple<int, int>> info = some.msg.Select(x => new Tuple<int, int>(int.Parse(x[0]), int.Parse(x[1]))).ToList();
                
            }
            //Message lobby_data = GetMessageOfType(InfoType.LobbyData);


        }

        // ProcessMessage PROTOS
        /*
        public Tuple<Message, bool> ProcessMessage(Newtonsoft.Json.Linq.JObject msg,int i)
        {
            if (msg != null)
            {
                Message new_msg = new Message(msg["game_id"].ToString(),msg["type"].ToString(),msg["msg"].ToString());
                Debug.WriteLine(new_msg);
                return new Tuple<Message, bool>(new_msg, true);
            }
            else
            {
                return new Tuple<Message, bool>(new Message(), false);
            }
        }

        public Tuple<Message,bool> ProcessMessage(Newtonsoft.Json.Linq.JObject msg)
        {

            if(msg != null)
            {
                Message new_msg = new Message(msg.Item[0], msg.Item[1], msg.Item[2]);
                return new Tuple<Message, bool>(new_msg, true);
            }
            return new Tuple<Message, bool>(new Message(), true);
        }
        
        */
        public Message GetMessage()
        {
            Newtonsoft.Json.Linq.JObject msg = new Newtonsoft.Json.Linq.JObject();
            bool data_recv = false;
            
            while (!data_recv)
            {
                msg = JsonConvert.DeserializeObject<Newtonsoft.Json.Linq.JObject>(my_client.get_reply());
                if(msg != new Newtonsoft.Json.Linq.JObject())
                {
                    data_recv = true;
                }
            }
            Debug.WriteLine(msg["game_id"].ToString());
            return new Message(msg["game_id"].ToString(),msg["type"].ToString(),msg["msg"].ToObject<JObject>());

        }
        

    }
}
