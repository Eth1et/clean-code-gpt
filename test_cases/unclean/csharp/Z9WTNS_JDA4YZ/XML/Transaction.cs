namespace Z9WTNS_JDA4YZ.DataClasses
{
    [Serializable]
    public sealed record class Transaction
    {
        public int Id { get; set; }
        public int UserId { get; set; }
        public decimal Amount { get; set; }
        public string Message { get; set; }


        public Transaction()
        {
            Id = 0;
            UserId = 0;
            Amount = 0;
            Message = string.Empty;
        }

        public Transaction(int id, int userId, decimal amount, string message)
        {
            Id = id;
            UserId = userId;
            Amount = amount;
            Message = message;
        }
    }
}
