namespace Z9WTNS_JDA4YZ.Xml
{
    public  static class PathConst
    {
        private static string ProgramPath { get => AppContext.BaseDirectory; }

        public static string UsersPath { get => Path.Combine(new string[] { ProgramPath, "data", "users.Xml" }); }

        public static string TransactionsPath { get => Path.Combine(new string[] { ProgramPath, "data", "transactions.Xml" }); }
    }
}
