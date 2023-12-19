using Z9WTNS_JDA4YZ.DataClasses;

namespace Z9WTNS_JDA4YZ.Test
{
    [TestFixture]
    internal class AccountHandlerTests
    {
        [Test]
        public void CalculateNetIncome_Under25_ReturnsCorrectNetIncome()
        {
            decimal grossIncome = 50000m;
            User under25User = new User { isUnder25 = true };

            decimal netIncome = AccountHandler.CalculateNetIncome(grossIncome, under25User);
            decimal expectedNetIncome = grossIncome / 1.226993865m;

            Assert.That(netIncome, Is.EqualTo(expectedNetIncome).Within(.0001));
        }

        [Test]
        public void CalculateNetIncome_Above25_ReturnsCorrectNetIncome()
        {
            decimal grossIncome = 70000m;
            User above25User = new User { isUnder25 = false };

            decimal netIncome = AccountHandler.CalculateNetIncome(grossIncome, above25User);
            decimal expectedNetIncome = grossIncome / 1.5037593398m;

            Assert.That(netIncome, Is.EqualTo(expectedNetIncome).Within(.0001));
        }

        [Test]
        public void SavedMoney_CalculatesNonNegativeSavings()
        {
            decimal grossIncome = 60000m;
            User under25User = new User { isUnder25 = true };

            decimal savings = AccountHandler.SavedMoney(grossIncome, under25User);

            Assert.That(savings, Is.GreaterThanOrEqualTo(0));
        }

        [Test]
        public void SavedMoney_CorrectInput_CalculatesCorrectSavings()
        {
            decimal grossIncome = 80000m;
            User under25User = new() { isUnder25 = true };
            User over25User = new() { isUnder25 = false };

            decimal actualSavings = AccountHandler.SavedMoney(grossIncome, under25User);
            decimal expectedSavings = AccountHandler.CalculateNetIncome(grossIncome, under25User) - AccountHandler.CalculateNetIncome(grossIncome, over25User);

            Assert.That(actualSavings, Is.EqualTo(expectedSavings).Within(0.0001m));
        }

        [Test]
        public void CalculateNetExpense_CorrectInput_CalculatesCorrectExpenseAmount()
        {
            decimal grossExpense = 80000m;

            decimal netExpense = AccountHandler.CalculateNetExpense(grossExpense);
            decimal actualNetExpense = grossExpense / 1.5037593398m;

            Assert.That(netExpense, Is.EqualTo(actualNetExpense).Within(0.0001m));
        }
    }
}