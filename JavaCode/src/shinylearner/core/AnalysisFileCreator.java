package shinylearner.core;

import shinylearner.helper.DataTypeUtilities;
import shinylearner.helper.FileUtilities;
import shinylearner.helper.ListUtilities;
import shinylearner.helper.MiscUtilities;

import java.util.ArrayList;
import java.util.HashSet;

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
			_dataPointNames = Singletons.Data.GetDataPointNamesForAnalysis();
		else
			_dataPointNames = dataPointNames;
	}

	/** Generates files in the ARFF format.
	 * @return This instance
	 * @throws Exception
	 */
	public void CreateArffFile(boolean includeDependentVariable) throws Exception
	{
		StringBuilder output = new StringBuilder();

		output.append("@relation thedata\n\n");

		Log.Debug("Appending ARFF attributes for independent variables");

		for (String dataPointName : _dataPointNames)
		{
			ArrayList<String> uniqueValues = new ArrayList<String>(new HashSet<String>(Singletons.Data.GetUniqueValuesForDataPoint(dataPointName)));
			output.append(AppendArffAttribute(uniqueValues, FormatName(dataPointName), false));
		}

		Log.Debug("Appending ARFF attributes for dependent variable");
		if (includeDependentVariable)
			output.append(AppendArffAttribute(FormatClassValues(Singletons.Data.GetClassOptions()), Settings.DEPENDENT_VARIABLE_NAME, true));

		output.append("\n@data");

		Log.Debug("Creating ARFF output text object");
		for (String instanceID : _instanceIDs)
		{
			ArrayList<String> dataValues = Singletons.Data.GetValuesForInstance(instanceID, _dataPointNames);

			output.append("\n" + ListUtilities.Join(dataValues, ","));

			if (includeDependentVariable)
				output.append("," + FormatClassValue(Singletons.Data.GetClassValue(instanceID)));
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
		StringBuilder output = new StringBuilder();

		ArrayList<String> headerItems = FormatNames(ListUtilities.CreateStringList(_instanceIDs));
		headerItems.add(0, "");
		output.append(ListUtilities.Join(headerItems, "\t") + "\n");

		for (String dataPoint : _dataPointNames)
		{
			ArrayList<String> rowItems = ListUtilities.CreateStringList(FormatName(dataPoint));

			rowItems.addAll(Singletons.Data.GetInstanceValuesForDataPoint(dataPoint));

			output.append(ListUtilities.Join(rowItems, "\t") + "\n");
		}

		if (includeDependentVariable)
		{
			ArrayList<String> rowItems = ListUtilities.CreateStringList(Settings.DEPENDENT_VARIABLE_NAME);

			for (String instanceID : _instanceIDs)
				rowItems.add(FormatClassValue(Singletons.Data.GetClassValue(instanceID)));

			output.append(ListUtilities.Join(rowItems, "\t") + "\n");
		}

		FileUtilities.WriteTextToFile(_outFilePath, output.toString());
	}

	public void CreateTabDelimitedFile(boolean includeDependentVariable) throws Exception
	{
		StringBuilder output = new StringBuilder();
		ArrayList<String> headerDataPoints = FormatNames(ListUtilities.CreateStringList(_dataPointNames));

		if (includeDependentVariable)
			headerDataPoints.add(Settings.DEPENDENT_VARIABLE_NAME);

		output.append("\t" + ListUtilities.Join(headerDataPoints, "\t") + "\n");

		for (String instanceID : _instanceIDs)
		{
			ArrayList<String> values = Singletons.Data.GetValuesForInstance(instanceID, _dataPointNames);

			if (includeDependentVariable)
				values.add(FormatClassValue(Singletons.Data.GetClassValue(instanceID)));

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
		return name.replace("/", "FoRwArD").replace(" ", "SpAcE").replace("*", "StAr").replace("-", "HyPhEn").replace("'", "ApOsTrApHe").replace("\"", "DbLqUoTe").replace(",", "ComMa").replace("%", "PeRcENtSiGN");
	}

	/** Some external libraries do not work well with special characters. After a name has been formatted, this method changes the characters back to the original characters.
	 *
	 * @param name Name to be unformatted
	 * @return Unformatted name
	 */
	public static String UnformatName(String name)
	{
		return name.replace("FoRwArD", "/").replace("SpAcE", " ").replace("StAr", "*").replace("HyPhEn", "-").replace("ApOsTrApHe", "'").replace("DbLqUoTe", "\"").replace("ComMa", ",").replace("PeRcENtSiGN", "%");
	}

	public static String CLASS_TEMP_PREFIX = "cLaSs___";

	public static String FormatClassValue(String value)
	{
		//if (DataTypeUtilities.IsInteger(value) || DataTypeUtilities.IsNumeric(value))
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
