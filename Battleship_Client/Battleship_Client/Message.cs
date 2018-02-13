using Newtonsoft.Json.Linq;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Battleship_Client
{
    public class Message : Object
    {
        public int game_id { get; set; }
        public InfoType type { get; set; }
        public Object msg { get; set; }

        public Message() { }

        public Message(JObject msg)
        {

            string type = "";
            string game_id = "";

            this.game_id = int.Parse(game_id);

            switch (type)
            {
                case "lose":
                    this.type = InfoType.Lose;
                    break;
                case "win":
                    this.type = InfoType.Win;
                    break;
                case "conn_req":
                    this.type = InfoType.ConnReq;
                    break;
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

        }
    }

    public enum InfoType
    {
        GameMade, LobbyData, JoinResult, MoveResult, Turn, LobbyResp, MoveReq, ConnReq, Win, Lose
    };

    public class LobbyRespMsg : Message
    {
        public Tuple<bool, bool> msg { get; set; }
    }

    public class VictoryRespMsg : Message
    {
        public string msg { get; set; }
    }

    public class LobbyDataMsg : Message
    {
        public Tuple<int,int> msg { get; set; }
    }

    public class MoveMsg : Message
    {
        public Tuple<bool,int,int> msg { get; set; }
    }

    public class ConfirmMsg : Message
    {
        public int msg { get; set; }
    }
}
