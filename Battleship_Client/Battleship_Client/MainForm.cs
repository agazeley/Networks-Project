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

            Message lobby_data = GetMessageOfType(InfoType.LobbyData);


        }

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

        public Message GetMessageOfType(InfoType type)
        {
            bool data_recv = false;
            Tuple < Message, bool> Processed = new Tuple< Message, bool>(new Message(), false);
            while (!data_recv)
            {
                Newtonsoft.Json.Linq.JObject msg = JsonConvert.DeserializeObject<Newtonsoft.Json.Linq.JObject>(my_client.get_reply());
                Processed = ProcessMessage(msg);
                data_recv = Processed.Item2;
            }
            return Processed.Item1;

        }


    }
}
