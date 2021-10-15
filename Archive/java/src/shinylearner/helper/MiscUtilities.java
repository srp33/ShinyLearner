package shinylearner.helper;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.InetAddress;
import java.util.UUID;

import shinylearner.core.Log;
import shinylearner.core.Settings;

/** This class contains general-purpose helper methods that are used in various places throughout the code. It also contains Singleton objects (those that are instantiated only once and stored as static variables).
 * @author Stephen
 */
public class MiscUtilities
{
    /** Indicates the IP address of the machine where this software is being run
     *
     * @return IP address
     * @throws Exception
     */
    public static String GetMachineAddress() throws Exception
    {
        return InetAddress.getLocalHost().getHostAddress();
    }

    /** Generates a unique identifier randomly
     *
     * @return Random unique identifier
     */
    public static String GetUniqueID()
    {
        return "id." + UUID.randomUUID();
    }

//    /** Indicates whether a string value is either null or equal to the missing character
//     *
//     * @param value Value to be tested
//     * @return Whether or not it is considered missing
//     */
//    public static boolean IsMissing(String value)
//    {
//        return value == null || value.equals(Settings.MISSING_VALUE_STRING);
//    }

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
                Log.Exception("Command output: " + output.toString());

            if (!error.toString().equals(""))
            {
            	Log.Exception("Command error: " + error.toString());
            	Log.Exit(1);
            }
        }

        return output.toString();
    }
    
    public static String CreateTempFilePath()
    {
    	return Settings.TEMP_DIR + "/" + MiscUtilities.GetUniqueID();
    }
}