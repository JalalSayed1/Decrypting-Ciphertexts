package rotor96Crypto;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.*;

public class COA {

    public static List<String> loadPasswords(String filename) throws IOException {
        return Files.readAllLines(Paths.get(filename));
    }

    public static String loadText(String filename) throws IOException {
        return new String(Files.readAllBytes(Paths.get(filename))).trim();
    }

    public static Map<String, String> cipherOnlyAttack(String ciphertext, String passwordFile) {
        List<String> passwords;
        Map<String, String> possibleDecipher = new HashMap<>();

        try {
            passwords = loadPasswords(passwordFile);
        } catch (IOException e) {
            System.err.println("Error reading password file: " + e.getMessage());
            return possibleDecipher;
        }

        List<String> commonWords = Arrays.asList(
                );

        for (String password : passwords) {
            try {
                String decryptedText = Rotor96Crypto.encdec(Rotor96Crypto.DEC, password, ciphertext);

                if (isEnglishSentence(decryptedText)) {
                    possibleDecipher.put(password, decryptedText);
                }
                
            } catch (Exception e) {
                System.err.println("Error with key " + password + ": " + e.getMessage());
            }
        }
        return possibleDecipher;
    }

    public static int performExperiment(String key, String ciphertext, String passwordFile) {
        int minLength = ciphertext.length();

        for (int len = 1; len <= ciphertext.length(); len++) {
            String truncatedCiphertext = ciphertext.substring(0, len);
            Map<String, String> results = cipherOnlyAttack(truncatedCiphertext, passwordFile);

            for (String decryptedText : results.values()) {
                if (isEnglishSentence(decryptedText)) {
                    System.out.println("Decrypted Text: " + decryptedText);
                    minLength = len;
                    break;
                }
            }
        }

        return minLength;

    }


    public static boolean isEnglishSentence(String text) {
        String[] commonWords = {
            "the", "be", "to", "of", "and", "a", "in", "that", "have", "I", "hello", "world", "this", "is", "the", "and", "of", "to", "in", "that", "have", "it", "for", "not", "on", "with", "he", "as", "you", "do", "at", "be", "by", "are", "or", "from", "but", "my", "if", "your", "has", "they", "we", "can", "her", "was", "said", "there", "use", "an", "each", "which", "she", "doe", "about", "out", "many", "then", "them", "these", "so", "some"
        };
        int count = 0;
        String[] words = text.toLowerCase().split("\\s+");
        for (String word : words) {
            if (Arrays.asList(commonWords).contains(word)) {
                count++;
            }
        }
        return count > words.length * 0.1;
    }

    public static void main(String[] args) {
        String ciphertext;
        String passwordFilename = "known_data/passwords";

        try {
            ciphertext = loadText("known_data/ciphertext2.txt");
        } catch (IOException e) {
            System.err.println("Error reading ciphertext file: " + e.getMessage());
            return;
        }

        System.out.println("Deciphering...");
        Map<String, String> possibleDecipher = cipherOnlyAttack(ciphertext, passwordFilename);
        System.out.println("Done.");
        for (Map.Entry<String, String> entry : possibleDecipher.entrySet()) {
            System.out.println("Key: " + entry.getKey());
            System.out.println("Decrypted Text:: " + entry.getValue() + "\n");
        }

        // Perform an experiment determine how many ciphertext characters are needed to
        // unambiguously decode the message:
        String key = "ov3ajy";
        System.out.println("Performing experiment...");
        int minlen = performExperiment(key, ciphertext, passwordFilename);
        System.out.println("Minimum ciphertext length for unambiguous decoding: " + minlen);
    }
}
