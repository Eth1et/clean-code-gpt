using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace The_Ultimate_Guesser_Game
{
    class Animals
    {
        public string name;
        public string[] info;
        public string secret;
        static public int count=0;
        public int id;

        public Animals(string aName, string[] aInfo)
        {
            aName = name;
            info = new string[aInfo.Length];

            for (int i=0; i<aInfo.Length;i++)
            {
                info[i] = aInfo[i];
            }
            id = ++count;
        }
    }
}
