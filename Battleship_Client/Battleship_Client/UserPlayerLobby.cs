using Newtonsoft.Json.Linq;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Battleship_Client
{
    public class User
    {
        public string name { get; set; }

        public User()
        {

        }
        public User(string name)
        {
            this.name = name;
        }
    }

    public class Player : User
    {
        private int id { get; set; }
        private string ip { get; set; }
        private int port { get; set; }

    }

    public class Lobby
    {
        private int id { get; set; }
        private Player p1 { get; set; }
        private Player p2 { get; set; }
        private Tuple<bool, bool> ready = new Tuple<bool, bool>(false, false);

    }

    
}
