using System.Security.Cryptography;
using System.Text;
using Z9WTNS_JDA4YZ.DataClasses;
using Z9WTNS_JDA4YZ.Xml;

namespace Z9WTNS_JDA4YZ
{
    public static class AccountHandler
    {       
        internal static User? Login()
        {
            List<User> users = XmlHandler.ReadObjectsFromXml<User>(PathConst.UsersPath);

            Console.Clear();
            Console.WriteLine("Kérem jelentkezen be!");
            Console.WriteLine("---------------------------------------");

            Console.Write("Kérem, írja be a Nevét: ");
            string name = Console.ReadLine()!;

            Console.Write("Kérem, írja be a jelszavát: ");
            string password = Console.ReadLine()!;

            Console.Clear();

            foreach (var user in users)
            {
                if (user.Username.Equals(name) && VerifyPassword(password, user.HashedPassword))
                {
                    Console.WriteLine("Sikeresen bejelentkezés!");
                    return user;
                }
            }

            Console.WriteLine("Belépés sikertelen!");
            Console.WriteLine();
            return null;
        }

        public static User? Register()
        {
            Console.Clear();
            Console.WriteLine("Most a regisztrációs menü sorban vagy!");

            List<User> users = XmlHandler.ReadObjectsFromXml<User>(PathConst.UsersPath);

            Console.Write("Kérem, írja be a Nevét: ");
            string name = Console.ReadLine()!;

            Console.Write("Kérem, írja be a jelszavát: ");
            string password = Console.ReadLine()!;
            string hashedPassword = HashPassword(password);

            Console.Write("Kérem, adja meg, hogy25 év alatti vagy nem (igen vagy nem): ");
            string userInput = Console.ReadLine()!.ToLower();
            bool under25 = (userInput == "igen" || userInput == "i");

            Console.Clear();

            if (XmlHandler.AppendObjectToXml(PathConst.UsersPath, new User(users.Count, name, hashedPassword, under25)))
            {
                Console.WriteLine("Sikeres regisztráció!");
                return Login();
            }
            else
            {
                Console.WriteLine("Regisztráció sikertelen!");
            }

            Console.WriteLine();
            return null;
        }

        internal static void AddTransaction(User user)
        {
            Console.WriteLine();
            Console.Write("Add megg a Bruttó bevételed vagy kiadásod: ");
            if (!decimal.TryParse(Console.ReadLine(), out decimal amount))
            {
                Console.WriteLine("Nem megfelelő összegét, sikertelen tranzakció hozzáadás!");
                return;
            }

            Console.Write("Adj meg tranzakció üzenetét: ");
            string message = Console.ReadLine()!;

            var transactions = XmlHandler.ReadObjectsFromXml<Transaction>(PathConst.TransactionsPath);

            Transaction transaction = new Transaction
            {
                Id = transactions.Count,
                UserId = user.Id,
                Amount = amount,
                Message = message
            };

            if (XmlHandler.AppendObjectToXml(PathConst.TransactionsPath, transaction))
            {
                Console.WriteLine("Tranzakció sikeresen hozzáadva!");
            }
            else
            {
                Console.WriteLine("A tranzakció hozzáadása sikertelen volt!");
            }

            Console.WriteLine();
        }

        internal static void QueryStatistics(User user)
        {
            List<Transaction> transactions = XmlHandler.ReadObjectsFromXml<Transaction>(PathConst.TransactionsPath);

            var userTransactions = transactions.Where(t => t.UserId.Equals(user.Id)).AsParallel().ToList();

            var incomes = userTransactions.Where(t => t.Amount > 0).AsParallel();
            var expenses = userTransactions.Where(t => t.Amount < 0).AsParallel();

            decimal grossIncome = incomes.Sum(t => t.Amount);
            decimal grossExpense = expenses.Sum(t => t.Amount);
            decimal grossFlow = grossExpense + grossIncome;

            decimal netIncome = CalculateNetIncome(grossIncome, user);
            decimal netExpense = CalculateNetExpense(grossExpense);
            decimal netFlow = netIncome + netExpense;

            decimal realFlow = netIncome + grossExpense;

            Console.WriteLine(
                $"""

                =================================================================================
                ||                            Tranzakciós Statisztikák                         ||
                =================================================================================
                |          |        Bevétel       |        Kiadás        |        Forgalom      |
                ---------------------------------------------------------------------------------
                |  Bruttó  |{grossIncome,21:C} |{grossExpense,21:C} |{grossFlow,21:C} |
                ---------------------------------------------------------------------------------
                |  Nettó   |{netIncome,21:C} |{netExpense,21:C} |{netFlow,21:C} |
                ---------------------------------------------------------------------------------
                |         Valódi Forgalom         |{realFlow,44:C} |
                """);

            if (user.isUnder25)
            {
                decimal savedMoney = SavedMoney(grossIncome, user);

                Console.WriteLine(
                    $"""
                    ---------------------------------------------------------------------------------
                    |    SZJA Mentesség Miatt Ennyit Spóroltál   |    {savedMoney,29:C} |
                    =================================================================================
                    """);
            }
            else
            {
                Console.WriteLine("=================================================================================");
            }

            Console.WriteLine();
        }

        public static decimal CalculateNetIncome(decimal grossIncome, User user)
        {
            if (user.isUnder25 == true)
                return grossIncome / 1.226993865m;

            return grossIncome / 1.5037593398m;
        }

        public static decimal SavedMoney(decimal grossIncome, User user)
        {
            User tempOver25 = new()
            {
                isUnder25 = false
            };

            return CalculateNetIncome(grossIncome, user) - CalculateNetIncome(grossIncome, tempOver25);
        }

        public static decimal CalculateNetExpense(decimal grossExpense)
        {
            return grossExpense / 1.5037593398m;
        }

        private static string HashPassword(string password)
        {
            using (var sha256 = SHA256.Create())
            {
                byte[] hashBytes = sha256.ComputeHash(Encoding.UTF8.GetBytes(password));
                return BitConverter.ToString(hashBytes).Replace("-", string.Empty);
            }
        }

        private static bool VerifyPassword(string password, string hashedPassword)
        {
            string newPasswordHash = HashPassword(password);
            return newPasswordHash == hashedPassword;
        }
    }
}
