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

    public class Message : Object
    {
        public int game_id { get; set; }
        public InfoType  type { get; set; }
        public Object msg { get; set; }
        public Message() { }
        public Message(string game_id,string type,string msg)
        {
            this.game_id = int.Parse(game_id);

            switch (type)
            {
                case "game_made":
                    this.type = InfoType.GameMade;
                    break;
                case "lobby_data":
                    this.type = InfoType.LobbyData;
                    break;
                case "join_result":
                    this.type = InfoType.JoinResult;
                    break;
                case "turn":
                    this.type = InfoType.Turn;
                    break;
                case "lobby_resp":
                    this.type = InfoType.LobbyResp;
                    break;
                case "move_req":
                    this.type = InfoType.MoveReq;
                    break;
                case "move_result":
                    this.type = InfoType.MoveResult;
                    break;
                default:
                    break;
            }


            this.msg = msg;
        }
    }

    public enum InfoType
    {
        GameMade, LobbyData,JoinResult,MoveResult,Turn,LobbyResp,MoveReq
    };
}
