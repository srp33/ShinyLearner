package shinylearner.core;

import java.io.PrintWriter;
import java.io.StringWriter;
import java.io.Writer;
import java.util.ArrayList;

import shinylearner.helper.ListUtilities;

/** This class contains methods for logging information about execution. Values are output to the screen and to output files.
 * @author Stephen Piccolo
 */
public class Log
{
    /** Saves debug information
     *
     * @param text Debug text
     */
    public static void Debug(Object text)
    {
        if (Settings.DEBUG)
            PrintOut(FormatText(text));
    }

    /** Saves debugging information for a non-fatal error.
     *
     * @param ex Exception that occurred.
     */
    public static void Debug(Throwable ex)
    {
        if (!Settings.DEBUG)
            return;

        if (ex == null)
        {
            PrintOut("<null Exception>");
            return;
        }

        Debug("A non-fatal error occurred. It will be logged but may not affect processing of this program.");
        Debug(GetStackTrace(ex));
    }

    /** Saves logging information
     *
     * @param text Logging text
     */
    public static void Info(Object text)
    {
        PrintOut(FormatText(text));
    }

    /** Saves exception information
     *
     * @param message Exception message
     */
    public static void Exception(String message)
    {
        Exception(new Exception(message));
    }

    /** Saves exception information
     *
     * @param ex Exception object
     */
    public static void Exception(Throwable ex)
    {
        Info(GetStackTrace(ex));
    }
    
    public static void Exception(ArrayList<String> list)
    {
        if (list == null)
            Info("<null ArrayList>");
        else
            Info("\n" + ListUtilities.Join(ListUtilities.CreateStringList(list), "\n"));
    }

    /** Saves exception information when the exception is severe enough that execution of the program should be halted.
     *
     * @param message Exception message
     */
    public static void ExceptionFatal(Object message)
    {
        ExceptionFatal(new Exception(String.valueOf(message)));
    }
    
    /** Saves exception information when the exception is severe enough that execution of the program should be halted.
     *
     * @param ex Exception object
     */
    public static void ExceptionFatal(Throwable ex)
    {
        Exception(ex);
        Exit(1);
     }

    /** Obtains stack-trace information when an exception has occurred.
     *
     * @param throwable Exception object
     * @return Stack-trace information
     */
    public static String GetStackTrace(Throwable throwable)
    {
        if (throwable == null)
            return "<null exception>";

        Writer result = new StringWriter();
        PrintWriter printWriter = new PrintWriter(result);
        throwable.printStackTrace(printWriter);
        return result.toString();
    }

    private static String FormatText(Object text)
    {
    	String output = (text == null ? "<null>" : String.valueOf(text));
    	
    	if (Singletons.ExperimentItems != null)
    		output = Singletons.ExperimentItems.Description + " | " + Singletons.ExperimentItems.AlgorithmScriptFilePath + " | " + output;
    	
    	return output;
    }

    public static void PrintOut(String out)
    {
        if (out.equals(""))
            return;

        System.out.println(out);
        System.out.flush();
    }
    
//    public static void PrintErr(Object x)
//    {
//        String out = x == null ? "<null>" : String.valueOf(x);
//
//        if (out.equals(""))
//            return;
//
//        System.err.println(out);
//        System.err.flush();
//    }

	public static void Exit(int exitCode)
	{
		System.exit(exitCode);
	}
}
