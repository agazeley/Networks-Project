using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;

namespace Battleship_Client
{
    class Utility
    {
        public static Message ProcessMessage(JObject msg)
        {
            InfoType type = GetInfoType(msg["type"].ToString());
            int game_id = int.Parse(msg["game_id"].ToString());
            var processed_msg = GetMsg(type, msg["msg"]);

            Message nm = new Message();
            nm.game_id = game_id;
            nm.type = type;
            nm.msg = processed_msg;

            return nm;
        }

        public static InfoType GetInfoType(string type)
        {
            switch (type)
            {
                case "lose":
                    return InfoType.Lose;
                    break;
                case "win":
                    return InfoType.Win;
                    break;
                case "conn_req":
                    return InfoType.ConnReq;
                    break;
                case "game_made":
                    return InfoType.GameMade;
                    break;
                case "lobby_data":
                    return InfoType.LobbyData;
                    break;
                case "join_result":
                    return InfoType.JoinResult;
                    break;
                case "turn":
                    return InfoType.Turn;
                    break;
                case "lobby_resp":
                    return InfoType.LobbyResp;
                    break;
                case "move_req":
                    return InfoType.MoveReq;
                    break;
                case "move_result":
                    return InfoType.MoveResult;
                    break;
                default:
                    return InfoType.ConnReq;
                    break;
            }
        }

        public static Object GetMsg(InfoType type, JToken msg)
        {
            if( type == InfoType.ConnReq || type == InfoType.GameMade || type == InfoType.JoinResult || type == InfoType.MoveReq)
            {
                return msg.ToObject<int>();
            }
            else if(type == InfoType.Win || type == InfoType.Lose)
            {
                return msg.ToObject<string>();
            }
            else if(type == InfoType.LobbyResp)
            {
                return msg.ToObject<Tuple<bool, bool>>();
            }
            else if(type == InfoType.LobbyData)
            {
                return msg.ToObject<List<int>>();
            }
            else if(type == InfoType.MoveResult)
            {
                return msg.ToObject<Tuple<bool, int, int>>();
            }
            else
            {
                return "";
            }
        }
    }
}