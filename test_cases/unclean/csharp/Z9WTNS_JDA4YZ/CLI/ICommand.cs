namespace Z9WTNS_JDA4YZ.CLI
{
    internal interface ICommand
    {
        HashSet<string> Names { get; }
        object? Execute(params object[] inputs);
    }
}
