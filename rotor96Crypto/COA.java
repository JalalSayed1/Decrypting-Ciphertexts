// Ciphertext Only Attach

public class COA {
    public static List<String> loadPasswords(String filename) throws IOException {
        List<String> passwords = new ArrayList<>();
        BufferedReader reader = new BufferedReader(new FileReader(filename));
        String line;
        while ((line = reader.readLine()) != null) {
            if (!line.trim().isEmpty()) {
                passwords.add(line.strip());
            }
        }
        reader.close();
        return passwords;
    }

    public static String loadText(String filename) throws IOException {
        BufferedReader reader = new BufferedReader(new FileReader(filename));
        StringBuilder text = new StringBuilder();
        String line;
        while ((line = reader.readLine()) != null) {
            text.append(line).append(" ");
        }
        reader.close();
        return text.toString().strip();
    }

    public static Map<String, String> cipherOnlyAttack(String ciphertext, String passwordFile) throws IOException {
        List<String> passwords = loadPasswords(passwordFile);
        Map<String, String> possibleDecipher = new HashMap<>();

        List<String> commonWords = List.of(
            "hello", "world", "this", "is", "the", "and", "of", "to", "in", "that",
            "have", "it", "for", "not", "on", "with", "he", "as", "you", "do", "at",
            "be", "by", "are", "or", "from", "but", "my", "if", "your", "has", "they",
            "we", "can", "her", "was", "said", "there", "use", "an", "each", "which",
            "she", "doe", "about", "out", "many", "then", "them", "these", "so", "some"
        );

        Rotor96Crypto rotor96Crypto = new Rotor96Crypto();
        for (String password : passwords) {
            try {
                String decryptedText = rotor96Crypto.encdec(Rotor96Crypto.DEC, password, ciphertext);

                List<String> decryptedWords = splitToWords(decryptedText.toLowerCase());
                for (String word : commonWords) {
                    if (decryptedWords.contains(word)) {
                        possibleDecipher.put(password, decryptedText);
                        System.out.println("Key found: " + password);
                        System.out.println("Found '" + word + "' in Decrypted text: \n" + decryptedText);
                        System.out.println();
                        break;
                    }
                }
            } catch (Exception e) {
                System.out.println("Error with key " + password + ": " + e);
            }
        }

        return possibleDecipher;
    }

    private static List<String> splitToWords(String text) {
        String[] words = text.split("[\\s.,;:!?']+");
        List<String> wordList = new ArrayList<>();
        for (String word : words) {
            if (!word.isEmpty()) {
                wordList.add(word);
            }
        }
        return wordList;
    }

    public static void main(String[] args) throws IOException {
        String ciphertext = loadText("../known_data/ciphertext2.txt");
        String passwordFile = "../passwords";

        System.out.println("Deciphering...");
        Map<String, String> possibleDecipher = cipherOnlyAttack(ciphertext, passwordFile);
        System.out.println("Done.");

        if (!possibleDecipher.isEmpty()) {
            java.io.PrintWriter writer = new java.io.PrintWriter("../decrypted_text/decrypted_text2.txt", "UTF-8");
            writer.println("key \t decrypted_text");
            for (Map.Entry<String, String> entry : possibleDecipher.entrySet()) {
                writer.println(entry.getKey() + " \t " + entry.getValue());
            }
            writer.close();
        }
    }
}
