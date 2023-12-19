namespace Z9WTNS_JDA4YZ.CLI.Commands
{
    internal class ExitCommand : ICommand
    {
        public HashSet<string> Names => new HashSet<string> { "exit", "quit", "e", "q" };

        public object? Execute(params object[] inputs)
        {
            Environment.Exit(0);
            return true;
        }
    }
}
