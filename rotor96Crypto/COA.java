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
            "hello", "world", "this", "is", "the", "and", "of", "to", "in", "that",
            "have", "it", "for", "not", "on", "with", "he", "as", "you", "do", "at",
            "be", "by", "are", "or", "from", "but", "my", "if", "your", "has", "they",
            "we", "can", "her", "was", "said", "there", "use", "an", "each", "which",
            "she", "doe", "about", "out", "many", "then", "them", "these", "so", "some"
        );

        for (String password : passwords) {
            try {
                String decryptedText = Rotor96Crypto.encdec(Rotor96Crypto.DEC, password, ciphertext);
                String[] decryptedWords = decryptedText.toLowerCase().split("\\s+");
                
                for (String decryptedWord : decryptedWords) {
                    if (commonWords.contains(decryptedWord)) {
                        possibleDecipher.put(password, decryptedText);
                        System.out.println("Key found: " + password);
                        System.out.println("Found '" + decryptedWord + "' in Decrypted text: \n" + decryptedText + "\n");
                        break;
                    }
                }
            } catch (Exception e) {
                System.err.println("Error with key " + password + ": " + e.getMessage());
            }
        }
        return possibleDecipher;
    }

    public static void main(String[] args) {
        String ciphertext;
        String passwordFilename = "../known_data/passwords";

        try {
            ciphertext = loadText("../known_data/ciphertext2.txt");
        } catch (IOException e) {
            System.err.println("Error reading ciphertext file: " + e.getMessage());
            return;
        }

        System.out.println("Deciphering...");
        Map<String, String> possibleDecipher = cipherOnlyAttack(ciphertext, passwordFilename);
        System.out.println("Done.");
    }
}
