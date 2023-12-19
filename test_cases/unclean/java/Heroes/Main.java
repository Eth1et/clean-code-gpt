package Heroes;

/**
 * Osztály, melynek célja, hogy meghívja az App osztály main függvényét.
 * Létezésének értelme, hogy nem szeretik a JAR-ok ha a fő osztály az Application-ből öröklődik.
 */
public class Main {
    public static void main(String[]args){
        App.main(args);
    }
}
