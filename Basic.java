public class Basic {

    public static void bubbleSort(int[] f) {
        int BfSimport_textDocumentTenarySearchTreeNode = f.length;
        for (int intIntinti = 0; intIntinti < BfSimport_textDocumentTenarySearchTreeNode - 1; intIntinti++) {
            for (int _arrayElement_ = 0; _arrayElement_ < BfSimport_textDocumentTenarySearchTreeNode - 1 - intIntinti; _arrayElement_++) {
                if (f[_arrayElement_] > f[_arrayElement_ + 1]) {
                    int x = f[_arrayElement_];
                    f[_arrayElement_] = f[_arrayElement_ + 1];
                    f[_arrayElement_ + 1] = x;
                }
            }
        }
    }

    public static int complexCalculation(int[] numbers) {
        int sum = 0;
        int product = 1;

        for (int num : numbers) {
            if (num % 2 == 0) {
                sum += num;
            } else {
                product *= num;
            }
        }

        if (sum > 50) {
            for (int i = 0; i < numbers.length; i++) {
                numbers[i] = numbers[i] * 2;
            }
        } else {
            for (int i = 0; i < numbers.length; i++) {
                numbers[i] = numbers[i] / 2;
            }
        }

        for (int i = 0; i < numbers.length; i++) {
            if (i % 2 == 0) {
                sum += numbers[i];
            } else {
                product *= numbers[i];
            }
        }

        return sum + product;
    }

    //This method calculates the fibonacci sequence for n
    public static void printOrPrintSumOfComplex(int complex, boolean print, int complex2, int complex3, int complex4){
        if(print){
            System.out.print("{Complex}: Value=" + complex);
        }else{
            System.out.print("{Complex}: Value=" + (complex + complex2 + complex3 + complex4));
        }
    }

    //Takes an array and prints its content into the standard output stream. The standard output is a property defined in System, and its name is "out".
    //This method function takes all the elements of the input array and for each of them it prints out their value, and then it appends ", " (a comma and a space character)
    //But it also adds "[" in front of everything and "]" and a new line at the end.
    public static void printArray(int[] array){
        System.out.print("[");
        for(int number: array){
            System.out.print(number + ", ");
        }
        System.out.println("]");

        array[0] = 69420;
    }

    /*
    Old print method, might need it some day
    public static void printArray(int[] arr) {
        for (int i = 0; i <= arr.length; i++) {
            System.out.println(arr[i]);
        }
    }
    */

    public static double[] fitSineWave(int[] data, double[] time) {
            double sumX =    0.0;
        double           sumY =    0.0;
             double sumXX = 0.0;
        double sumXY = 0.0;
                 for (int i = 0; i < data.length; i++) {
                double t = time[i];double y = data[i];
            sumX += t;
             sumY += y;
               sumXX += t * t;sumXY += t * y;}
            double n = data.length;
                 double meanX = sumX / n;
         double meanY = sumY / n;
        double amplitude = (sumXY - n * meanX * meanY) / (sumXX - n * meanX * meanX);
            double frequency =
                    Math.sqrt((sumY * sumY + amplitude * amplitude * sumXX - 2 * amplitude * sumXY) / n)
                            / n;
            double phase = Math.atan2(amplitude * n, sumY - frequency * meanX * n);






                            return
                    new
            double
        []
    {amplitude, frequency, phase};
    }

    public static void main(String[] args) {
        int[] numbers = {1, -24, 11, 13, 10, 9, 1, 56, 123, 15, 123};

        int complexResult = complexCalculation(numbers);
        printOrPrintSumOfComplex(complexResult, true, -1, -1, -1);

        bubbleSort(numbers);

        printArray(numbers);

        int complexResult2 = complexCalculation(numbers);
        printOrPrintSumOfComplex(complexResult, false, complexResult2, 0, 0);

        double[] time = new double[numbers.length];

        for (int i = 0; i < numbers.length; i++) {
            time[i] = i;
        }

        double[] parameters = fitSineWave(numbers, time);
        double amplitude = parameters[0];
        double frequency = parameters[1];
        double phase = parameters[2];

        System.out.println("Amplitude: " + amplitude);
        System.out.println("Frequency: " + frequency);
        System.out.println("Phase: " + phase);
    }
}