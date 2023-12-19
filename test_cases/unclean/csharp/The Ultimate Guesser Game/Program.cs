using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace The_Ultimate_Guesser_Game
{
    class Program
    {
        static void Main(string[] args)
        {
            Random rnd = new Random();
            int guessCount;
            bool wantToPlay = true;
            string choice = "";
            int recordCount=0;

            do
            {
                Console.Clear();
                Console.WriteLine("\n\n\nHi! It's the 1.0 Version of The Ultimate Guesser Game.\n\nEnter [start] to start the game.\nEnter [rules] for the rules.\nEnter [exit] to quit the game.");
                Console.Write("Choice: ");
                choice = Console.ReadLine().ToLower();

            } while (choice != "start" && choice != "rules" && choice != "exit");

            do
            {
                MENU:
                switch (choice)
                {
                    case "rules":

                        if (Rules() == true)
                        {
                            break;
                        }
                        else
                        {
                            wantToPlay = false;
                            goto GAME;
                        }

                    case "exit":

                        wantToPlay = false;
                        break;

                    default:

                        goto GAME;
                }

            
                GAME:
                if (wantToPlay == true)
                {
                    Countries hungary = new Countries("Hungary", new string[] {"This country is situated at the middle of Europe.", "This country is famous for the Unicum.", "Close to 10 million people live there.", "Lake Balaton", "Good friends with the polish people.", "Vitamin-C" });
                    Countries sweden = new Countries("Sweden", new string[] {"IKEA", "This country's flag has 2 colors: yellow and blue.", "This country is situated at North-Europe.", "The capital city of this country is Stockholm.", "The currency is called as ___ Krona (Crown) there.", "Vikings" });
                    Countries unitedKingdom = new Countries("United Kingdom", new string[] {"This is a sovereign country located off the north-western coast of the European mainland.", "The capital city is London.", "Tea is love, Tea is life.", "This state consists of 4 different countries.", "The national language is the English", "This country/state is not member of the European Union." });
                    Animals lion = new Animals("lion",new string[] {"It has four legs.","It's a perdator.","It lives in Africa.","It spends the most of the time with sleeping.","Physically strong.","Has mane."});
                    Animals python = new Animals("python",new string[] {"It's a type of snake.","A programming language is named after this.","Lives in Africa and India.","It is long.","It's spotty."});
                    Animals dog = new Animals("dog",new string[] {"It's the best friend of the people.","Many of the people keep them as pets.","There are many species of it.","It likes to play.","It's derived from the wolves."});

                    Console.WriteLine(hungary.id);
                    Console.WriteLine(sweden.id);
                    Console.WriteLine(unitedKingdom.id);
                    Console.WriteLine(python.id);
                    Console.WriteLine(Animals.count);
                    Console.ReadKey();

                    choice = "";
                    var isNumeric=false;
                    int numMin, numMax = 0;
                    guessCount = 0;

                    while (!(choice.Contains("anim")) && choice !="a" && !(choice.Contains("count")) && choice != "c" && !(choice.Contains("num")) && choice != "n" && !(choice.Contains("rand")) && choice != "r")
                    {
                        Console.Clear();
                        Console.WriteLine("\n\nWellcome to THE ULTIMATE GUESSER GAME!\n\n");
                        Console.WriteLine("Choose one of these topics by entering their name[ Animals / Countries / Numbers / Random ]");
                        Console.Write("Your Choice: ");
                        choice = Console.ReadLine().ToLower();
                    }

                    int choiceNum;

                    if (choice.Contains("anim") || choice == "a")
                    {
                        choiceNum = 0;
                    }
                    else if ((choice.Contains("count")) || choice == "c")
                    {
                        choiceNum = 1;
                    }
                    else if ((choice.Contains("num")) || choice == "n")
                    {
                        choiceNum = 2;
                    }
                    else
                    {
                        choiceNum = rnd.Next(0,3);   
                    }

                    switch (choiceNum)
                    {
                        case 0://Countries

                            break;

                        case 1://Animals

                            

                         
                            break;

                        case 2:
                            
                            do
                            {
                                Console.Clear();
                                Console.WriteLine("\n\nThe Ultimate Number Guesser is ON!\nFirstly please give the interval of whole numbers in which the program will think.");
                                Console.Write("From: ");
                                isNumeric = int.TryParse(Console.ReadLine(), out  numMin);
                            } while (!isNumeric);
                            do
                            {
                                    Console.Clear();
                                    Console.WriteLine("\n\nThe Ultimate Number Guesser is ON!\nFirstly please give the interval of whole numbers in which the program will think.");
                                    Console.WriteLine("From: "+numMin);
                                    Console.Write("To: ");
                                    isNumeric = int.TryParse(Console.ReadLine(), out numMax);

                            } while (!isNumeric);

                            int secret = rnd.Next(numMin, numMax + 1);
                            int userInput;
                            string aboveOrBelow = "";

                            do
                            {
                                do
                                {
                                    Console.Clear();
                                    Console.WriteLine("\n\nThe Program has a number in it's memory.\n");
                                    Console.WriteLine("Guesscount: " + guessCount);

                                    if (aboveOrBelow != "")
                                    {
                                        Console.WriteLine("Your Last Guess was "+aboveOrBelow+" the secret number.\n");
                                        if (recordCount!=0)
                                        {
                                            Console.WriteLine("Your record Win was with: {0} guesses.\n", recordCount);
                                        }
                                        else
                                        {
                                            Console.WriteLine();
                                            Console.WriteLine();
                                        }

                                    }
                                    else
                                    {
                                        Console.WriteLine();
                                        Console.WriteLine();
                                        if (recordCount != 0)
                                        {
                                            Console.WriteLine("Your record Win was with: {0} guesses.\n", recordCount);
                                        }
                                        else
                                        {
                                            Console.WriteLine();
                                            Console.WriteLine();
                                        }
                                    }
                                    Console.Write("Make a guess!: ");
                                    isNumeric = int.TryParse(Console.ReadLine(), out userInput);

                                } while (!isNumeric);
                                
                                if (userInput<secret)
                                {
                                    aboveOrBelow = "BELOW";
                                }
                                else
                                {
                                    aboveOrBelow = "ABOVE";
                                }

                                guessCount++;

                            } while (secret != userInput);

                            Console.Clear();
                            Console.WriteLine("\n\nCongratz You successfully guessed the secret number!\n");
                            Console.WriteLine("The secret number was: "+secret);
                            Console.WriteLine("\nYou made it with: {0} guesses.",guessCount);
                            if(recordCount==0)
                            {
                                Console.WriteLine("This is your NEW RECORD!");
                                recordCount = guessCount;
                            }
                            else
                            {
                                Console.WriteLine("Your record was with: {0} guesses.", recordCount);
                            }

                            Console.WriteLine(".");
                            Console.WriteLine("..");
                            Console.WriteLine("...");
                            Console.Write("\nPress <Enter> to continue.");
                            Console.ReadLine();
                            break;

                    }



                    Console.Clear();
                    Console.Write("Do You Want To Play Another Round?[y/n]: ");
                    choice = Console.ReadLine().ToLower();

                    while (choice != "y" && choice != "n")
                    {
                        Console.Write("\nError 02: Invalid User Input!\nDo You Want To Play Another Round?[y:yes/n:no]: ");
                        choice = Console.ReadLine();
                    }
                    switch (choice)
                    {
                        case "y":
                            wantToPlay = true;
                            break;

                        case "n":
                            wantToPlay = false;
                            break;

                    }
                    Console.Clear();
                }

            }while (wantToPlay == true);

            Console.WriteLine("BYE! :)");
        }

        private static bool Rules()
        {
            bool result;
            string aChoice = "";
            for (aChoice = "";aChoice != "y" && aChoice!= "n";)
            {
                Console.Clear();
                Console.WriteLine("\n\nIn the followings the program is going to guess a word/number/etc depending on your choice.\nYour job is pretty simple: Guess what it thinks about.");
                Console.WriteLine("The program is also going to help you with some facts.");
                Console.Write("Would you like to play?[y/n]: ");
                aChoice = Console.ReadLine().ToLower();
            } 

            if (aChoice=="y")
            {
                result = true;
            }
            else
            {
                result = false;
            }

            return result;

        }

    }
}
