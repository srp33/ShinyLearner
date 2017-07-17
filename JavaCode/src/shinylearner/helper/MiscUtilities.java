package shinylearner.helper;

import shinylearner.core.Log;
import shinylearner.core.Settings;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.util.UUID;

/** This class contains general-purpose helper methods that are used in various places throughout the code. It also contains Singleton objects (those that are instantiated only once and stored as static variables).
 * @author Stephen
 */
public class MiscUtilities
{
    /** Generates a unique identifier randomly
     *
     * @return Random unique identifier
     */
    public static String GetUniqueID()
    {
        return "id." + UUID.randomUUID();
    }

    public static String ExecuteShellCommand(String commandText) throws Exception
    {
        Log.Debug("System command:");
        Log.Debug(commandText);
        //Log.Exit(1);

        Process p = Runtime.getRuntime().exec(new String[] { "bash", "-c", commandText });

        // Read the output and error streams from the process
        BufferedReader stdInput = new BufferedReader(new InputStreamReader(p.getInputStream()));
        BufferedReader stdError = new BufferedReader(new InputStreamReader(p.getErrorStream()));

        StringBuffer output = new StringBuffer();
        StringBuffer error = new StringBuffer();

        // Parse the output stream
        String s;
        while ((s = stdInput.readLine()) != null)
            output.append(s + "\n");

        // Parse the error stream
        while ((s = stdError.readLine()) != null)
            error.append(s + "\n");

        // Close the process objects
        stdInput.close();
        stdError.close();
        p.destroy();

        // Print the error, including parameters that had been specified, to aid in troubleshooting
        if (error.length() > 0)
        {
            // Print the output
            if (output.length() > 0)
                Log.Debug("Command stdput: " + output.toString());

            Log.Debug("Command stderr: " + error.toString());
        }

        return output.toString();
    }
    
    public static String CreateTempFilePath()
    {
    	return Settings.TEMP_DIR + "/" + MiscUtilities.GetUniqueID();
    }

    public static String trimSpecific(String str, String toTrim)
    {
        if (str.startsWith(toTrim))
            str = str.substring(toTrim.length());

        if (str.endsWith(toTrim))
            str = str.substring(0, str.length() - toTrim.length());

        return str;
    }
}