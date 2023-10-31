public class Basic {

    public static void bubbleSort(int[] array) {
        int length = array.length;
        for (int i = 0; i < length - 1; i++) {
            for (int j = 0; j < length - 1 - i; j++) {
                if (array[j] > array[j + 1]) {
                    int temp = array[j];
                    array[j] = array[j + 1];
                    array[j + 1] = temp;
                }
            }
        }
    }

    public static int sumEvenProductOdd(int[] numbers) {
        int sum = 0;
        int product = 1;

        for (int num : numbers) {
            if (num % 2 == 0) {
                sum += num;
            } else {
                product *= num;
            }
        }

        return sum + product;
    }

    public static void printOrPrintSum(int value, boolean print, int sum) {
        if (print) {
            System.out.println("{Value}: " + value);
        } else {
            System.out.println("{Sum}: " + (value + sum));
        }
    }

    public static void printArray(int[] array) {
        System.out.print("[");
        for (int i = 0; i < array.length; i++) {
            System.out.print(array[i]);
            if (i != array.length - 1) {
                System.out.print(", ");
            }
        }
        System.out.println("]");

        array[0] = 69420;
    }

    public static double[] fitSineWave(int[] data, double[] time) {
        double sumX = 0.0;
        double sumY = 0.0;
        double sumXX = 0.0;
        double sumXY = 0.0;

        for (int i = 0; i < data.length; i++) {
            double t = time[i];
            double y = data[i];

            sumX += t;
            sumY += y;
            sumXX += t * t;
            sumXY += t * y;
        }

        double n = data.length;
        double meanX = sumX / n;
        double meanY = sumY / n;
        double amplitude = (sumXY - n * meanX * meanY) / (sumXX - n * meanX * meanX);
        double frequency = Math.sqrt((sumY * sumY + amplitude * amplitude * sumXX - 2 * amplitude * sumXY) / n) / n;
        double phase = Math.atan2(amplitude * n, sumY - frequency * meanX * n);

        return new double[]{amplitude, frequency, phase};
    }

    public static void main(String[] args) {
        int[] numbers = {1, -24, 11, 13, 10, 9, 1, 56, 123, 15, 123};

        int result = sumEvenProductOdd(numbers);
        printOrPrintSum(result, true, -1);

        bubbleSort(numbers);
        printArray(numbers);

        int result2 = sumEvenProductOdd(numbers);
        printOrPrintSum(result, false, result2);

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