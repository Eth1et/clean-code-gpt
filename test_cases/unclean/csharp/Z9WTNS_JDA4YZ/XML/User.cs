namespace Z9WTNS_JDA4YZ.DataClasses
{
    [Serializable]
    public sealed record class User
    {
        public int Id { get; set; }
        public string Username { get; set; }
        public string HashedPassword { get; set; }
        public bool isUnder25 { get; set; }

        public User()
        {
            Id = 0;
            Username = "";
            HashedPassword = "";
        }

        public User(int id, string username, string hashedPassword, bool under25)
        {
            Id = id;
            Username = username;
            HashedPassword = hashedPassword;
            isUnder25 = under25;
        }
    }
}
