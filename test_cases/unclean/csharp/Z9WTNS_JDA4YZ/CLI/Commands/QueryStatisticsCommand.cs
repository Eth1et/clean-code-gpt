using Z9WTNS_JDA4YZ.DataClasses;

namespace Z9WTNS_JDA4YZ.CLI.Commands
{
    internal class QueryStatisticsCommand : ICommand
    {
        public HashSet<string> Names => new HashSet<string> { "query", "stats", "quers stats", "statistics", "s" };

        public object? Execute(params object[] inputs)
        {
            User user = (User)inputs[0];

            AccountHandler.QueryStatistics(user);

            return null;
        }
    }
}
