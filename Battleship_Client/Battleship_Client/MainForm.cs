using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

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
        }
    }
}
