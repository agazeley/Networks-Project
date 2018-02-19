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
            Message msg = GetMessage();

            IList<int> list = (IList<int>)msg.msg;
            for(int i =0; i < list.Count;)
            {
                dgv_lob.Rows.Add(list[i],list[i + 1]);
                i = i + 2;
            }


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

        private void btn_join_Click(object sender, EventArgs e)
        {
            int selected_count = dgv_lob.SelectedRows.Count;

            if(selected_count == 1)
            {
                int game_id = (int)dgv_lob.SelectedRows[0].Cells[0].Value;
                Debug.WriteLine(game_id.ToString());

                string data = Client.create_request(usr.name, "join_game", game_id.ToString());
                if (my_client.server_request(data))
                {
                    Message msg = GetMessage();
                    if(msg.type == InfoType.JoinResult && (int)msg.msg == 1)
                    {
                        MessageBox.Show("SUCCESSFULLY JOINED A GAME");
                    }
                    else
                    {
                        MessageBox.Show("Did not join game number " + game_id.ToString());
                    }
                }
            }
            else if(selected_count > 1)
            {
                MessageBox.Show("Selected more than one lobby to join. Please try again.");
            }
            else
            {
                //Did not select a row so don't do anything
            }
        }
    }
}
