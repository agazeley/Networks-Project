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
            IList<int> list = (IList<int>)some.msg;

            for(int i =0; i < list.Count;)
            {
                dgv_lob.Rows.Add(list[i],list[i + 1]);
                i = i + 2;
            }
            Debug.WriteLine(some);

        }


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
            // msg["game_id"].ToString(),msg["type"].ToString(),msg["msg"].ToObject<JObject>()
            Debug.WriteLine(msg["game_id"].ToString());
            Debug.WriteLine(msg["type"].ToString());
            return Utility.ProcessMessage(msg);

        }

    }
}
