package shinylearner.helper;

import java.io.BufferedWriter;
import java.io.File;
import java.io.FileOutputStream;
import java.io.FileWriter;
import java.io.OutputStreamWriter;
import java.io.PrintWriter;
import java.util.ArrayList;
import java.util.zip.GZIPOutputStream;

/** This class provides helper methods for reading, writing, updating, and deleting files.
 * @author Stephen Piccolo
 */
public class FileUtilities
{
    /** Convenience method that appends text to an existing file.
     *
     * @param filePath Absolute file path
     * @param text Text to append
     * @throws Exception
     */
    public static void AppendTextToFile(String filePath, String text) throws Exception
    {
        PrintWriter out = new PrintWriter(new BufferedWriter(new FileWriter(filePath, true)));
        out.write(text);
        out.close();
    }

    /** Appends a line to an existing file (incuding a new line character).
     *
     * @param filePath Absolute file path
     * @param text Text to append
     * @throws Exception
     */
    public static void AppendLineToFile(String filePath, String text) throws Exception
    {
        AppendTextToFile(filePath, text + "\n");
    }

    /** Writest text to a file.
     *
     * @param filePath Absolute file path
     * @param text Text to write
     * @throws Exception
     */
    public static void WriteTextToFile(String filePath, String text) throws Exception
    {
    	PrintWriter printWriter;
    	
    	if (filePath.endsWith(".gz"))
    	{
    		printWriter = new PrintWriter(new BufferedWriter(new OutputStreamWriter(new GZIPOutputStream(new FileOutputStream(new File(filePath))), "UTF-8")));
    	}
    	else
    	{
    		printWriter = new PrintWriter(new BufferedWriter(new FileWriter(filePath)));
    	}
        
        printWriter.write(text);
        printWriter.close();
    }

    /** Writes a new line to a file (including a new line character).
     *
     * @param filePath Absolute file path
     * @param text Text to write
     * @throws Exception
     */
    public static void WriteLineToFile(String filePath, String text) throws Exception
    {
        WriteTextToFile(filePath, text + "\n");
    }

    /** Writes new lines to a file (including new line characters).
     *
     * @param filePath Absolute file path
     * @param rows List of row lists to write
     * @throws Exception
     */
    public static void WriteLinesToFile(String filePath, ArrayList<ArrayList<String>> rows) throws Exception
    {
        WriteLinesToFile(filePath, rows, "");
    }

    /** Writes new lines to a file (including new line characters).
     *
     * @param filePath Absolute file path
     * @param rows List of row lists to write
     * @param headerComment Descriptive comment that will be placed at the top of the file
     * @throws Exception
     */
    public static void WriteLinesToFile(String filePath, ArrayList<ArrayList<String>> rows, String headerComment) throws Exception
    {
        if (rows == null)
        {
        	Log.Debug("The object to be saved to " + filePath + " was null.");
            return;
        }

        StringBuffer output = new StringBuffer();

        if (headerComment != null && !headerComment.equals(""))
            output.append("#" + headerComment + "\n");

        for (ArrayList<String> row : rows)
            output.append(ListUtilities.Join(row, "\t") + "\n");

        WriteTextToFile(filePath, output.toString());
    }

    /** Reads lines from a file.
     *
     * @param filePath Absolute file path
     * @param commentChar Comment character (lines starting with this character are ignored)
     * @return Each line in the file
     * @throws Exception
     */
    public static ArrayList<String> ReadLinesFromFile(String filePath, String commentChar) throws Exception
    {
        ArrayList<String> rows = new ArrayList<String>();

        for (String line : new BigFileReader(filePath))
        {
            if (line.trim().length() == 0 || (commentChar != null && line.startsWith(commentChar)))
                continue;

            rows.add(line.trim());
        }

        return rows;
    }

    /** Reads all text from a file.
     *
     * @param filePath Absolute file path
     * @return String representation of text in a file
     * @throws Exception
     */
    public static String ReadTextFile(String filePath) throws Exception
    {
        StringBuilder text = new StringBuilder();

        for (String line : new BigFileReader(filePath))
            text.append(line + "\n");

        return text.toString();
    }

    /** Parses a delimited file.
     *
     * @param filePath Absolute file path
     * @return List of lists containing each element in the file
     * @throws Exception
     */
    public static ArrayList<ArrayList<String>> ParseDelimitedFile(String filePath) throws Exception
    {
        return ParseDelimitedFile(filePath, "\t");
    }

    /** Parses a delimited file.
     *
     * @param filePath Absolute file path
     * @param delimiter Delimiter
     * @return List of lists containing each element in the file
     * @throws Exception
     */
    public static ArrayList<ArrayList<String>> ParseDelimitedFile(String filePath, String delimiter) throws Exception
    {
        return ParseDelimitedFile(filePath, delimiter, "#");
    }

    /** Parses a delimited file.
     *
     * @param filePath Absolute file path
     * @param delimiter Delimiter
     * @param commentChar Comment character (lines starting with this character will be ignored)
     * @return List of lists containing each element in the file
     * @throws Exception
     */
    public static ArrayList<ArrayList<String>> ParseDelimitedFile(String filePath, String delimiter, String commentChar) throws Exception
    {
        return ParseDelimitedFile(filePath, delimiter, commentChar, 0);
    }

    /** Parses a delimited file.
     *
     * @param filePath Absolute file path
     * @param delimiter Delimiter
     * @param commentChar Comment character (lines starting with this character will be ignored)
     * @param numLinesToSkip Number of lines to skip at the beginning of the file
     * @return List of lists containing each element in the file
     * @throws Exception
     */
    public static ArrayList<ArrayList<String>> ParseDelimitedFile(String filePath, String delimiter, String commentChar, int numLinesToSkip) throws Exception
    {
        if (!FileExists(filePath))
            throw new Exception("No file exists at " + filePath);

        ArrayList<ArrayList<String>> rows = new ArrayList<ArrayList<String>>();

        int linesSkipped = 0;

        BigFileReader reader = new BigFileReader(filePath);
        for (String line : reader)
        {
            if (line == null || line.equals("") || line.startsWith(commentChar))
                continue;

            if (linesSkipped < numLinesToSkip)
            {
                linesSkipped++;
                continue;
            }

            rows.add(ListUtilities.CreateStringList(line.split(delimiter)));
        }

        return rows;
    }

    /** Deletes a file.
     *
     * @param file File object
     */
    public static boolean DeleteFile(File file)
    {
        if (file.exists())
            try
            {
                return file.delete();
            }
            catch (Exception ex)
            {
                Log.Debug("Could not delete " + file.getAbsolutePath() + "."); // Often this is not a problem, but we're recording it just in case.
                return false;
            }
        else
            return true; // If the file is not there, then indicate that it has been deleted (even if it was by some other process)
    }

    /** Deletes a file.
     *
     * @param filePath Absolute file path
     */
    public static boolean DeleteFile(String filePath)
    {
        return DeleteFile(new File(filePath));
    }

    public static ArrayList<String> GetFilesMatchingPattern(String pattern) throws Exception
    {
    	ArrayList<String> filePaths = new ArrayList<String>();
    	
    	String shellOutput = MiscUtilities.ExecuteShellCommand("ls " + pattern);
    	
    	for (String match : shellOutput.split("\n"))
    		filePaths.add(match);
    	
    	return filePaths;
    }

    /** Checks whether a directory currently exists. If not, it (and any parent directories that don't exist) are attempted to be created.
     *
     * @param dirPath Absolute directory path
     * @return Absolute directory path
     * @throws Exception
     */
    public static String CreateDirectoryIfNotExists(String dirPath) throws Exception
    {
    	if (dirPath.equals("."))
    		return dirPath;
    	
        File dir = new File(dirPath);
        if (!dir.exists())
        {
            if (!dir.mkdirs())
                Log.Debug("A new directory could not be created at " + dirPath + ".");
        }

        return dirPath;
    }

    /** Indicates whether a file exists (and is not a directory).
     *
     * @param filePath Absolute file path
     * @return Whether the file exists (and is not a directory)
     * @throws Exception
     */
    public static boolean FileExists(String filePath) throws Exception
    {
        File file = new File(filePath);
        return file.exists() && !file.isDirectory();
    }

    /** Indicates whether a directory exists.
     *
     * @param filePath Absolute directory path
     * @return Whether the directory exists
     * @throws Exception
     */
    public static boolean DirectoryExists(String filePath) throws Exception
    {
        return new File(filePath).exists();
    }

    /** Checks whether the directory in an absolute file path exists. If not, it is created.
     *
     * @param filePath Absolute file path
     * @throws Exception
     */
    public static void CreateFileDirectoryIfNotExists(String filePath) throws Exception
    {
        File file = new File(filePath);
        String dirPath = file.getParent();

        if (dirPath == null) // If it is just a file name
            return;

        CreateDirectoryIfNotExists(dirPath);
    }

    /** This method parses the file extensions from a file path.
    *
    * @param filePath Full or relative file path
    * @return File extension
    */
   public static String GetFileExtension(String filePath)
   {
       String simpleName = new File(filePath).getName();

       if (simpleName.contains("."))
           return simpleName.substring(simpleName.lastIndexOf('.') + 1);
       else
    	   return "";
   }
}
