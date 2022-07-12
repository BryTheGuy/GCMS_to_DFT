package chendom.edu.uoregon.iupactosmiles;

import java.io.File;
import java.io.PrintWriter;
import java.io.FileWriter;
import java.io.IOException;  // Import the IOException class to handle errors
import java.io.FileNotFoundException;  // Import this class to handle errors
import java.util.Scanner; // Import the Scanner class to read text files
import uk.ac.cam.ch.wwmm.opsin.NameToStructure;

public class Convert {
    public static void main(String[] args) {
        // Getting the file
        File f = new File("file.txt");
        // Checking if the specified file
        if (f.exists()) {   // exists or not
            // Print message if it exists
            System.out.println("Exist, removing");
            File oldFile = new File("file.txt");
            if (oldFile.delete()) {
                System.out.println("Deleted the file: " + oldFile.getName());
                readFile();
            } else {
                System.out.println("Failed to delete the file: " + oldFile.getName());
            }
        } else {
            // Print message if it does not exist
            System.out.println("Does not Exist");
            readFile();
        }
    }

    public static void readFile() {
        try {
            File molNames = new File("C:\\Users\\bryce\\Documents\\Hendon_Lab\\GCMS_Redox\\GCMS_to_DFT\\MoleculeNameList.txt");
            Scanner myReader = new Scanner(molNames);
            while (myReader.hasNextLine()) {
                String data = myReader.nextLine();
                System.out.println(data);
                toSMILES(data);
            }
            myReader.close();
        } catch (FileNotFoundException e) {
            throw new RuntimeException(e);
        }
    }

    public static void toSMILES(String molecule) {
        NameToStructure nts = NameToStructure.getInstance();
        String smiles = nts.parseToSmiles(molecule);
        System.out.println(smiles);
        writeFile(smiles);
    }

    public static void writeFile(String smilesString) {
        //Declaring reference of File class
        File file = null;
        PrintWriter pw = null;
        try {
            //Creating object of PrintWriter class
            pw = new PrintWriter(new FileWriter("file.txt", true));
            pw.println(smilesString); //Writing to the file
            pw.close(); //Closing the stream
            System.out.println("File writing done.");
        } catch (Exception e) {
            e.printStackTrace();
        } finally {
            try {
                if (pw != null) {
                    pw.close();
                }
            } catch (Exception e) {
                e.printStackTrace();
            }
        }
    }
}
