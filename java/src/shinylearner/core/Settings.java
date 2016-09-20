package shinylearner.core;

import java.util.ArrayList;
import java.util.HashMap;

import shinylearner.helper.FileUtilities;

/** This class stores application wide values. These values are typically machine-specific and are set via command-line parameters.
 * @author Stephen Piccolo
 */
public class Settings
{
	public static boolean DEBUG;
    public static String MAIN_DIR;
    public static String TEMP_DIR;
    public static ArrayList<String> DATA_FILES = new ArrayList<String>();
    public static String DEPENDENT_VARIABLE_NAME;
    public static String EXPERIMENT_FILE;
    public static String OUTPUT_DATA_FILE_PATH;
    public static String OUTPUT_PREDICTIONS_FILE_PATH;
    public static String OUTPUT_FEATURES_FILE_PATH;
    public static String OUTPUT_BENCHMARK_FILE_PATH;

	/** Parses configuration settings that have been specified at the command line and saves these settings so they can be used throughout the application.
	 *
	 * @param args Command-line arguments
	 * @throws Exception
	 */
	public static void ParseCommandLineSettings(String[] args) throws Exception
	{
		DEBUG = Boolean.parseBoolean(GetArgValue(args, "DEBUG", "false"));
		MAIN_DIR = GetArgValue(args, "MAIN_DIRECTORY", System.getProperty("user.dir"));
		TEMP_DIR = FileUtilities.CreateDirectoryIfNotExists(GetArgValue(args, "TEMP_DIR", null));
		
		for (String x : GetArgValue(args, "DATA_FILES", null).split(","))
			for (String filePath : FileUtilities.GetFilesMatchingPattern(x))
				DATA_FILES.add(filePath);			
		
		DEPENDENT_VARIABLE_NAME = GetArgValue(args, "DEPENDENT_VARIABLE_NAME", "Class");
		EXPERIMENT_FILE = GetArgValue(args, "EXPERIMENT_FILE", null);
		OUTPUT_DATA_FILE_PATH = GetArgValue(args, "OUTPUT_DATA_FILE_PATH", "");
		OUTPUT_PREDICTIONS_FILE_PATH = GetArgValue(args, "OUTPUT_PREDICTIONS_FILE_PATH", "");
		OUTPUT_FEATURES_FILE_PATH = GetArgValue(args, "OUTPUT_FEATURES_FILE_PATH", "");
		OUTPUT_BENCHMARK_FILE_PATH = GetArgValue(args, "OUTPUT_BENCHMARK_FILE_PATH", "");
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
	
	public static void Check() throws Exception
	{
		if (!FileUtilities.DirectoryExists(MAIN_DIR))
			Log.ExceptionFatal("No directory exists at " + MAIN_DIR + ".");
		if (!FileUtilities.DirectoryExists(TEMP_DIR))
			Log.ExceptionFatal("No directory exists at " + TEMP_DIR + ".");
		
		if (TEMP_DIR.endsWith("/"))
			TEMP_DIR = TEMP_DIR.substring(0, TEMP_DIR.lastIndexOf("/"));
		
		if (DATA_FILES.size() == 0)
			Log.ExceptionFatal("No data files were specified.");
		for (String dataFilePath : DATA_FILES)
			if (!FileUtilities.FileExists(dataFilePath))
				Log.ExceptionFatal("No file exists at " + dataFilePath);

		if (!FileUtilities.FileExists(EXPERIMENT_FILE))
			Log.ExceptionFatal("No file exists at " + EXPERIMENT_FILE);
		
		if (OUTPUT_DATA_FILE_PATH.equals("") && OUTPUT_PREDICTIONS_FILE_PATH.equals("") && OUTPUT_FEATURES_FILE_PATH.equals("") && OUTPUT_BENCHMARK_FILE_PATH.equals(""))
			Log.ExceptionFatal("No output files have been specified.");

		if (!OUTPUT_DATA_FILE_PATH.equals(""))
			FileUtilities.CreateFileDirectoryIfNotExists(OUTPUT_DATA_FILE_PATH);
		
		if (!OUTPUT_PREDICTIONS_FILE_PATH.equals(""))
			FileUtilities.CreateFileDirectoryIfNotExists(OUTPUT_PREDICTIONS_FILE_PATH);

		if (!OUTPUT_FEATURES_FILE_PATH.equals(""))
			FileUtilities.CreateFileDirectoryIfNotExists(OUTPUT_FEATURES_FILE_PATH);
		
		if (!OUTPUT_BENCHMARK_FILE_PATH.equals(""))
			FileUtilities.CreateFileDirectoryIfNotExists(OUTPUT_BENCHMARK_FILE_PATH);
	}
}
