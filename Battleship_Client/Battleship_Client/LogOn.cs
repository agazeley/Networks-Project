using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Diagnostics;
using System.Drawing;
using System.Linq;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace Battleship_Client
{
    public partial class LogOn : Form
    {
        private Client my_client { get; set; }
        private UdpClient c;

        public LogOn()
        {
            InitializeComponent();

            IPEndPoint localpt = new IPEndPoint(IPAddress.Any, 5000);
            c = new UdpClient(localpt);
            c.Client.SetSocketOption(SocketOptionLevel.Socket, SocketOptionName.ReuseAddress, true);
        }

        private void btn_logon_Click(object sender, EventArgs e)
        {
            #region TEST CODE TEST CODE
            /*
            // Debug.WriteLine(tb_name.Text);
            // Debug.WriteLine(tb_ip.Text );

            IPEndPoint ep = new IPEndPoint(IPAddress.Parse(tb_ip.Text), 80);

            c.Connect("localhost",80);
            byte[] msg = Encoding.ASCII.GetBytes("Connect?");
            c.Send(msg, msg.Length);
            Debug.WriteLine("Sending: " + msg.ToString());

            if (c.Available > 0)
            {
                string reply = Encoding.ASCII.GetString(c.Receive(ref ep));
                Debug.WriteLine(reply);
            }

            */
            #endregion



            my_client = new Client(tb_ip.Text, 80);
            if (my_client.start_client(tb_name.Text))
            {
                // Success
                MessageBox.Show("Successfully connected!");
                this.Hide();
                MainForm Main = new MainForm(new User(tb_name.Text), my_client);
                Main.Show();
            }
            else
            {
                // Oh noooooo
                MessageBox.Show("OH NO IT DIDNT WORK :/");
            }

        }
    }
}
