using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Battleship_Client
{
    public class User
    {
        private string name { get; set; }

        public User()
        {

        }
        public User(string name)
        {
            this.name = name;
        }
    }
}
