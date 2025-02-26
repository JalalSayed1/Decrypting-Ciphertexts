// Known Plaintext Attach
package rotor96Crypto;

// import Rotor96Crypto;
import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class KPA {

    // Load passwords from file
    public static List<String> loadPasswords(String filename) throws IOException {
        List<String> passwords = new ArrayList<>();
        BufferedReader reader = new BufferedReader(new FileReader(filename));
        String line;
        while ((line = reader.readLine()) != null) {
            if (!line.trim().isEmpty()) {
                passwords.add(line.trim());
            }
        }
        reader.close();
        return passwords;
    }

    // Load text from file
    public static String loadText(String filename) throws IOException {
        BufferedReader reader = new BufferedReader(new FileReader(filename));
        StringBuilder textBuilder = new StringBuilder();
        String line;
        while ((line = reader.readLine()) != null) {
            textBuilder.append(line).append("\n");
        }
        reader.close();
        return textBuilder.toString().trim();
    }

    // KPA dictionary attack
    public static Map<String, String> knownPlaintextAttack(String ciphertext, String knownPlaintext, String passwordFile) {
        Map<String, String> possibleDecipher = new HashMap<>();
        try {
            List<String> passwords = loadPasswords(passwordFile);
            for (String password : passwords) {
                try {
                    // Assuming Rotor96Crypto.set_key and Rotor96Crypto.encdec are methods in a class
                    String decryptedText = Rotor96Crypto.encdec(Rotor96Crypto.DEC, password, ciphertext);
                    if (decryptedText.startsWith(knownPlaintext)) {
                        System.out.println("Key found: " + password);
                        System.out.println("Decrypted text: " + decryptedText);
                        possibleDecipher.put(password, decryptedText);
                    }
                } catch (Exception e) {
                    System.err.format("Error with key %s: %s%n", password, e.getMessage());
                    e.printStackTrace();
                }
            }
        } catch (IOException e) {
            System.err.format("Error reading passwords from file: %s%n", e.getMessage());
            e.printStackTrace();
        }

        if (possibleDecipher.isEmpty()) {
            System.out.println("Key not found in dictionary.");
            return null;
        }

        return possibleDecipher;
    }

    public static void main(String[] args) {
        // Example usage
        try {
            String ciphertext = loadText("known_data/ciphertext1.txt");
            String knownPlaintext = loadText("known_data/known_plaintext.txt");
            String passwordFile = "known_data/passwords";

            System.out.println("Deciphering..");
            Map<String, String> result = knownPlaintextAttack(ciphertext, knownPlaintext, passwordFile);
            System.out.println("Done.");
            
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
