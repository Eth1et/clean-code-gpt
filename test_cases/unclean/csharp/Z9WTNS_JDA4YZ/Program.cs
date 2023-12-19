using Z9WTNS_JDA4YZ.CLI;
using Z9WTNS_JDA4YZ.CLI.Commands;
using Z9WTNS_JDA4YZ.DataClasses;
using Z9WTNS_JDA4YZ.Xml;

namespace Z9WTNS_JDA4YZ
{
    internal class Program
    {
        static void Main()
        {
            if (!XmlHandler.InitializeXmlData(PathConst.UsersPath) || !XmlHandler.InitializeXmlData(PathConst.TransactionsPath))
            {
                Console.WriteLine("A program futása leáll, mert nem sikerült inicializálni az xml fájlokat.");
                return;
            }

            CommandRunner loginRegisterRunner = new CommandRunner
            {
                Message = "Válassz egy lehetőséget ('login' vagy 'register' vagy 'exit'): ",
                Commands = new ICommand[] { new ExitCommand(), new LoginCommand(), new RegisterCommand() }
            };

            User user = (User)loginRegisterRunner.Run();

            CommandRunner programRunner = new CommandRunner
            {
                Message = "Adj hozzá tranzakciót, vagy kérdezd le a statisztikádat ('add' vagy 'stats' vagy 'exit'): ",
                Commands = new ICommand[] { new ExitCommand(), new AddTransactionCommand(), new QueryStatisticsCommand() }
            };

            programRunner.Run(user);
        }
    }
}