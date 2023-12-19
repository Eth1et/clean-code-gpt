namespace Z9WTNS_JDA4YZ.CLI
{
    internal class CommandRunner
    {
        internal required string Message { get; set; }
        internal required ICommand[] Commands { get; set; }

        public object Run(params object[] inputs)
        {
            while (true)
            {
                Console.Write(Message);
                string? input = Console.ReadLine()!.Trim().ToLower();

                if (string.IsNullOrEmpty(input)) continue;

                var command = Commands
                    .Where(command => command.Names.Contains(input))
                    .FirstOrDefault();

                if (command != null)
                {
                    object? result = command.Execute(inputs);

                    if (result != null) return result;
                }
            }
        }
    }
}
