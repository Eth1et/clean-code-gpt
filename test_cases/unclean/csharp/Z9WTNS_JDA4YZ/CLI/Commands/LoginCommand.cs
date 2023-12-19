namespace Z9WTNS_JDA4YZ.CLI.Commands
{
    internal class LoginCommand : ICommand
    {
        public HashSet<string> Names => new HashSet<string> { "login", "l" };

        public object? Execute(params object[] inputs)
        {
            return AccountHandler.Login();
        }
    }
}
