using Z9WTNS_JDA4YZ.DataClasses;

namespace Z9WTNS_JDA4YZ.CLI.Commands
{
    internal class AddTransactionCommand : ICommand
    {
        public HashSet<string> Names => new HashSet<string> { "add", "a", "add transaction", "transaction", "t" };

        public object? Execute(params object[] inputs)
        {
            User user = (User)inputs[0];

            AccountHandler.AddTransaction(user);

            return null;
        }
    }
}
