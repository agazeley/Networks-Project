using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Diagnostics;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace Battleship_Client
{
    public partial class LogOn : Form
    {
        private Client my_client { get; set; }
        public LogOn()
        {
            InitializeComponent();
        }

        private void btn_logon_Click(object sender, EventArgs e)
        {
            Debug.WriteLine(tb_name.Text);
            Debug.WriteLine(tb_ip.Text );

            my_client = new Client(tb_ip.Text, 80);
            if (my_client.start_client(tb_name.Text))
            {
                // Success
                this.Hide();
            }
            else
            {
                // Oh noooooo
                MessageBox.Show("OH NO IT DIDNT WORK :/");
            }
        }
    }
}
