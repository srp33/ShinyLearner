package shinylearner.helper;

import shinylearner.core.Log;

import java.io.*;
import java.util.ArrayList;
import java.util.zip.GZIPOutputStream;

/** This class provides helper methods for reading, writing, updating, and deleting files.
 * @author Stephen Piccolo
 */
public class FileUtilities
{
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

    public static void AppendLinesToFile(String filePath, ArrayList<String> lines) throws Exception
    {
        if (lines == null | lines.size() == 0)
        {
            Log.ExceptionFatal("The object to be saved to " + filePath + " was null or empty.");
            return;
        }

        PrintWriter printWriter;

        if (filePath.endsWith(".gz"))
        {
            printWriter = new PrintWriter(new BufferedWriter(new OutputStreamWriter(new GZIPOutputStream(new FileOutputStream(new File(filePath), true)), "UTF-8")));
        }
        else
        {
            printWriter = new PrintWriter(new BufferedWriter(new FileWriter(filePath, true)));
        }

        for (String line : lines)
            printWriter.write(line + "\n");

        printWriter.close();
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
    	    if (FileExists(match))
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
}
