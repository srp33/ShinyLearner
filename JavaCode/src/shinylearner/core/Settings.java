package shinylearner.core;

import shinylearner.helper.FileUtilities;

import java.util.ArrayList;
import java.util.HashMap;

/** This class stores application wide values. These values are typically machine-specific and are set via command-line parameters.
 * @author Stephen Piccolo
 */
public class Settings
{
	public static boolean DEBUG;
	public static boolean IMPUTE;
    public static String TEMP_DIR;
    public static ArrayList<String> RAW_DATA_FILES = new ArrayList<String>();
	public static String ANALYSIS_DATA_FILE;
    public static String DEPENDENT_VARIABLE_NAME = "Class";
    public static String EXPERIMENT_FILE;
    public static String OUTPUT_PREDICTIONS_FILE_PATH;
    public static String OUTPUT_FEATURES_FILE_PATH;
    public static String OUTPUT_BENCHMARK_FILE_PATH;
    public static String NUM_CORES;

	/** Parses configuration settings that have been specified at the command line and saves these settings so they can be used throughout the application.
	 *
	 * @param args Command-line arguments
	 * @throws Exception
	 */
	public static void ParseCommandLineSettings(String[] args) throws Exception
	{
		DEBUG = Boolean.parseBoolean(GetArgValue(args, "DEBUG", "false"));
		IMPUTE = Boolean.parseBoolean(GetArgValue(args, "IMPUTE", "false"));

		TEMP_DIR = FileUtilities.CreateDirectoryIfNotExists(GetArgValue(args, "TEMP_DIR", null));
		if (TEMP_DIR.endsWith("/"))
			TEMP_DIR = TEMP_DIR.substring(0, TEMP_DIR.lastIndexOf("/"));

		String dataFilesArg = GetArgValue(args, "RAW_DATA_FILES", "");

		if (!dataFilesArg.equals(""))
		{
			for (String x : dataFilesArg.split(","))
			{
				ArrayList<String> filePaths = FileUtilities.GetFilesMatchingPattern(x);

				if (filePaths.size() == 0)
					Log.ExceptionFatal("No input data was found that matches this pattern: " + x + ".");

				for (String filePath : filePaths)
				{
					if (!FileUtilities.FileExists(filePath))
						Log.ExceptionFatal("No file exists at " + filePath);

					RAW_DATA_FILES.add(filePath);
				}
			}
		}

		ANALYSIS_DATA_FILE = GetArgValue(args, "ANALYSIS_DATA_FILE", "");
		EXPERIMENT_FILE = GetArgValue(args, "EXPERIMENT_FILE", "");
		OUTPUT_PREDICTIONS_FILE_PATH = GetArgValue(args, "OUTPUT_PREDICTIONS_FILE_PATH", "");
		OUTPUT_FEATURES_FILE_PATH = GetArgValue(args, "OUTPUT_FEATURES_FILE_PATH", "");
		OUTPUT_BENCHMARK_FILE_PATH = GetArgValue(args, "OUTPUT_BENCHMARK_FILE_PATH", "");
		NUM_CORES = GetArgValue(args, "NUM_CORES", "1");
	}
	
	/** Parses a value with a specified key from the command-line arguments.
	 *
	 * @param args Command-line arguments
	 * @param key Key of the argument
	 * @param defaultValue Value that is used if no value is specified
	 * @return Value of the argument
	 * @throws Exception
	 */
	private static String GetArgValue(String[] args, String key, String defaultValue) throws Exception
	{
		HashMap<String, String> keyValueMap = new HashMap<String, String>();

		for (String arg : args)
			if (arg.contains("="))
			{
				String[] parts = arg.split("=");
				if (parts.length == 2 && parts[0].length() > 0 && parts[1].length() > 0)
					keyValueMap.put(parts[0], parts[1]);
			}

		if (keyValueMap.containsKey(key))
			return keyValueMap.get(key);
		else
		{
			if (defaultValue == null)
				throw new Exception("A value for " + key + " must be set at the command line.");
			else
				return defaultValue;
		}
	}
}
