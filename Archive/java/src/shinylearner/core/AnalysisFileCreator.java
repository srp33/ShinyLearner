package shinylearner.core;

import java.util.ArrayList;
import java.util.HashSet;

import shinylearner.helper.DataTypeUtilities;
import shinylearner.helper.FileUtilities;
import shinylearner.helper.ListUtilities;
import shinylearner.helper.MiscUtilities;

/** This class is used to transform data from the data format to the format that is required for external software components.
 * @author Stephen Piccolo
 */
public class AnalysisFileCreator
{
	private String _outFilePath;
	private ArrayList<String> _instanceIDs;
	private ArrayList<String> _dataPointNames;
	public static HashSet<String> AcceptedDataFormats = new HashSet<String>(ListUtilities.CreateStringList("arff", "tsv", "ttsv"));

	public static String CreateFile(String dataFormat, ArrayList<String> instanceIDs, ArrayList<String> dataPointNames, boolean includeDependentVariable) throws Exception
	{
		String filePath = MiscUtilities.CreateTempFilePath() + "." + dataFormat;
		FileUtilities.CreateFileDirectoryIfNotExists(filePath);

		AnalysisFileCreator fileCreator = new AnalysisFileCreator(filePath, instanceIDs, dataPointNames);

		switch (dataFormat) {
		case "arff": fileCreator.CreateArffFile(true); // Weka throws an error if we don't include the dependent variable
		break;
		case "tsv": fileCreator.CreateTabDelimitedFile(includeDependentVariable);
		break;
		case "ttsv": fileCreator.CreateTransposedTabDelimitedFile(includeDependentVariable);
		break;
		default: 
			Log.ExceptionFatal("Invalid data format: " + dataFormat);
		}

		return filePath;
	}

	public AnalysisFileCreator(String outFilePath, ArrayList<String> instanceIDs, ArrayList<String> dataPointNames)
	{
		_outFilePath = outFilePath;
		_instanceIDs = instanceIDs;

		if (dataPointNames == null)
			_dataPointNames = Singletons.IndependentVariableInstances.GetDataPointNamesSorted();
		else
			_dataPointNames = dataPointNames;
	}

	/** Generates files in the ARFF format.
	 * @return This instance
	 * @throws Exception
	 */
	public void CreateArffFile(boolean includeDependentVariable) throws Exception
	{
//		PrintWriter outFile = new PrintWriter(new BufferedWriter(new FileWriter(_outFilePath)));
//
//		outFile.write("@relation thedata\n\n");
//
//		Log.Debug("Appending ARFF attributes for independent variables");
//
//		for (String dataPointName : _dataPointNames)
//		{
//			ArrayList<String> uniqueValues = new ArrayList<String>(new HashSet<String>(Singletons.IndependentVariableInstances.GetUniqueValues(dataPointName)));
//			outFile.write(AppendArffAttribute(uniqueValues, FormatName(dataPointName), false));
//		}
//
//		Log.Debug("Appending ARFF attributes for dependent variable");
//		if (includeDependentVariable)
//			outFile.write(AppendArffAttribute(FormatClassValues(Singletons.DependentVariableOptions), Settings.DEPENDENT_VARIABLE_NAME, true));
//
//		outFile.write("\n@data");
//
//		Log.Debug("Creating ARFF output text object");
//		for (String instanceID : _instanceIDs)
//		{
//			ArrayList<String> dataValues = Singletons.IndependentVariableInstances.GetDataPointValues(instanceID, _dataPointNames);
//
//			outFile.write("\n" + ListUtilities.Join(dataValues, ","));
//
//			if (includeDependentVariable)
//				outFile.write("," + FormatClassValue(Singletons.DependentVariableInstances.get(instanceID)));
//		}
//
//		outFile.close();
		
		StringBuilder output = new StringBuilder();

		output.append("@relation thedata\n\n");

		Log.Debug("Appending ARFF attributes for independent variables");

		for (String dataPointName : _dataPointNames)
		{
			ArrayList<String> uniqueValues = new ArrayList<String>(new HashSet<String>(Singletons.IndependentVariableInstances.GetUniqueValues(dataPointName)));
			output.append(AppendArffAttribute(uniqueValues, FormatName(dataPointName), false));
		}

		Log.Debug("Appending ARFF attributes for dependent variable");
		if (includeDependentVariable)
			output.append(AppendArffAttribute(FormatClassValues(Singletons.DependentVariableOptions), Settings.DEPENDENT_VARIABLE_NAME, true));

		output.append("\n@data");

		Log.Debug("Creating ARFF output text object");
		for (String instanceID : _instanceIDs)
		{
			ArrayList<String> dataValues = Singletons.IndependentVariableInstances.GetDataPointValues(instanceID, _dataPointNames);

			output.append("\n" + ListUtilities.Join(dataValues, ","));

			if (includeDependentVariable)
				output.append("," + FormatClassValue(Singletons.DependentVariableInstances.get(instanceID)));
		}

		FileUtilities.WriteTextToFile(_outFilePath, output.toString());
	}

	private String AppendArffAttribute(ArrayList<String> values, String dataPointName, boolean isClassAttribute) throws Exception
	{
		String outText = "@attribute " + dataPointName + " ";

		if (DataTypeUtilities.HasOnlyBinary(values))
			outText += "{" + ListUtilities.Join(ListUtilities.SortStringList(values), ",") + "}";
		else
		{
			if (!isClassAttribute && DataTypeUtilities.HasOnlyNumeric(values))
				outText += "real";
			else
			{
				outText += "{" + ListUtilities.Join(ListUtilities.SortStringList(values), ",") + "}";
			}
		}

		return outText + "\n";
	}

	/** This method generates a basic tab-delimited file with variables as rows and instances as columns.
	 * @return This instance
	 * @throws Exception
	 */
	public void CreateTransposedTabDelimitedFile(boolean includeDependentVariable) throws Exception
	{
//		PrintWriter outFile = new PrintWriter(new BufferedWriter(new FileWriter(_outFilePath)));
//
//		ArrayList<String> headerItems = FormatNames(ListUtilities.CreateStringList(_instanceIDs));
//		headerItems.add(0, "");
//		outFile.write(ListUtilities.Join(headerItems, "\t") + "\n");
//
//		for (String dataPoint : _dataPointNames)
//		{
//			ArrayList<String> rowItems = ListUtilities.CreateStringList(FormatName(dataPoint));
//
//			for (String instanceID : _instanceIDs)
//				rowItems.add(Singletons.IndependentVariableInstances.GetDataPointValue(instanceID, dataPoint));
//
//			//            rowItems = ListUtilities.ReplaceAllExactMatches(rowItems, Settings.MISSING_VALUE_STRING, "NA");
//
//			outFile.write(ListUtilities.Join(rowItems, "\t") + "\n");
//		}
//
//		if (includeDependentVariable)
//		{
//			ArrayList<String> rowItems = ListUtilities.CreateStringList(Settings.DEPENDENT_VARIABLE_NAME);
//
//			for (String instanceID : _instanceIDs)
//				rowItems.add(FormatClassValue(Singletons.DependentVariableInstances.get(instanceID)));
//
//			outFile.write(ListUtilities.Join(rowItems, "\t") + "\n");
//		}
//
//		outFile.close();

		StringBuilder output = new StringBuilder();

		ArrayList<String> headerItems = FormatNames(ListUtilities.CreateStringList(_instanceIDs));
		headerItems.add(0, "");
		output.append(ListUtilities.Join(headerItems, "\t") + "\n");

		for (String dataPoint : _dataPointNames)
		{
			ArrayList<String> rowItems = ListUtilities.CreateStringList(FormatName(dataPoint));

			for (String instanceID : _instanceIDs)
				rowItems.add(Singletons.IndependentVariableInstances.GetDataPointValue(instanceID, dataPoint));

			output.append(ListUtilities.Join(rowItems, "\t") + "\n");
		}

		if (includeDependentVariable)
		{
			ArrayList<String> rowItems = ListUtilities.CreateStringList(Settings.DEPENDENT_VARIABLE_NAME);

			for (String instanceID : _instanceIDs)
				rowItems.add(FormatClassValue(Singletons.DependentVariableInstances.get(instanceID)));

			output.append(ListUtilities.Join(rowItems, "\t") + "\n");
		}

		FileUtilities.WriteTextToFile(_outFilePath, output.toString());
	}

	/** This method generates a tab-delimited file with variables as columns and instances as rows.
	 * @param includeInstanceIDs Whether to include the ID of each instance in the file
	 * @return This instance
	 * @throws Exception
	 */
	public void CreateTabDelimitedFile(boolean includeDependentVariable) throws Exception
	{
//		ArrayList<String> headerDataPoints = FormatNames(ListUtilities.CreateStringList(_dataPointNames));
//
//		if (includeDependentVariable)
//			headerDataPoints.add(Settings.DEPENDENT_VARIABLE_NAME);
//
//		PrintWriter outFile = new PrintWriter(new BufferedWriter(new FileWriter(_outFilePath)));
//
//		outFile.write("\t" + ListUtilities.Join(headerDataPoints, "\t") + "\n");
//
//		for (String instanceID : _instanceIDs)
//		{
//			ArrayList<String> values = Singletons.IndependentVariableInstances.GetDataPointValues(instanceID, _dataPointNames);
//
//			if (includeDependentVariable)
//				values.add(FormatClassValue(Singletons.DependentVariableInstances.get(instanceID)));
//
//			//values = ListUtilities.ReplaceAllExactMatches(values, Settings.MISSING_VALUE_STRING, "NA");
//
//			outFile.write(FormatName(instanceID) + "\t" + ListUtilities.Join(values, "\t") + "\n");
//		}
//
//		outFile.close();
		
		StringBuilder output = new StringBuilder();
		ArrayList<String> headerDataPoints = FormatNames(ListUtilities.CreateStringList(_dataPointNames));

		if (includeDependentVariable)
			headerDataPoints.add(Settings.DEPENDENT_VARIABLE_NAME);

		output.append("\t" + ListUtilities.Join(headerDataPoints, "\t") + "\n");

		for (String instanceID : _instanceIDs)
		{
			ArrayList<String> values = Singletons.IndependentVariableInstances.GetDataPointValues(instanceID, _dataPointNames);

			if (includeDependentVariable)
				values.add(FormatClassValue(Singletons.DependentVariableInstances.get(instanceID)));

			//values = ListUtilities.ReplaceAllExactMatches(values, Settings.MISSING_VALUE_STRING, "NA");

			output.append(FormatName(instanceID) + "\t" + ListUtilities.Join(values, "\t") + "\n");
		}

		FileUtilities.WriteTextToFile(_outFilePath, output.toString());
	}

	/** Some external libraries do not work well with special characters, so this method changes those special characters temporarily to other characters.
	 *
	 * @param names List of names to be formatted
	 * @return Formatted names
	 */
	public static ArrayList<String> FormatNames(ArrayList<String> names)
	{
		ArrayList<String> formatted = new ArrayList<String>();

		for (String name : names)
			formatted.add(FormatName(name));

		return formatted;
	}

	/** Some external libraries do not work well with special characters, so this method changes those special characters temporarily to other characters.
	 *
	 * @param name Name to be formatted
	 * @return Formatted name
	 */
	public static String FormatName(String name)
	{
		return name.replace("/", "_forward_").replace(" ", "_space_").replace("*", "_star_").replace("-", "_hyphen_").replace("'", "_apostraphe_").replace("\"", "_doublequote_");
	}

	/** Some external libraries do not work well with special characters. After a name has been formatted, this method changes the characters back to the original characters.
	 *
	 * @param names List of names to be unformatted
	 * @return Unformatted names
	 */
	public static ArrayList<String> UnformatNames(ArrayList<String> names)
	{
		ArrayList<String> unformatted = new ArrayList<String>();

		for (String name : names)
			unformatted.add(UnformatName(name));

		return unformatted;
	}

	/** Some external libraries do not work well with special characters. After a name has been formatted, this method changes the characters back to the original characters.
	 *
	 * @param name Name to be unformatted
	 * @return Unformatted name
	 */
	public static String UnformatName(String name)
	{
		return name.replace("_forward_", "/").replace("_space_", " ").replace("_star_", "*").replace("_hyphen_", "-").replace("_apostraphe_", "'").replace("_doublequote_", "\"");
	}

	private static String CLASS_TEMP_PREFIX = "cLaSs___";

	public static String FormatClassValue(String value)
	{
		if (DataTypeUtilities.IsInteger(value) || DataTypeUtilities.IsNumeric(value))
			value = CLASS_TEMP_PREFIX + value;

		return value;
	}
	
	public static ArrayList<String> FormatClassValues(ArrayList<String> values)
	{
		ArrayList<String> newValues = new ArrayList<String>();
		
		for (String value : values)
			newValues.add(FormatClassValue(value));
		
		return newValues;
	}

	public static String UnformatClassValue(String value)
	{
		return value.replace(CLASS_TEMP_PREFIX, "");
	}
}
