package mlflexlite.helper;

import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.PrintWriter;
import java.util.ArrayList;
import java.util.HashSet;

import mlflexlite.core.Settings;
import mlflexlite.core.Singletons;

/** This class is used to transform data from the ML-Flex data format to the format that is required for external software components.
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
        	_dataPointNames = Singletons.InstanceVault.IndependentVariableInstances.GetDataPointNames();
        else
        	_dataPointNames = dataPointNames;
    }

    private String GetDependentVariableValue(String instanceID) throws Exception
    {
        return Singletons.InstanceVault.DependentVariableInstances.get(instanceID);
    }
    
    /** Generates files in the ARFF format.
     * @return This instance
     * @throws Exception
     */
    public void CreateArffFile(boolean includeDependentVariable) throws Exception
    {
        PrintWriter outFile = new PrintWriter(new BufferedWriter(new FileWriter(_outFilePath)));

        outFile.write("@relation thedata\n\n");

        Log.Debug("Appending ARFF attributes for independent variables");
        
        for (String dataPointName : _dataPointNames)
        {
            HashSet<String> uniqueValues = new HashSet<String>(Singletons.InstanceVault.IndependentVariableInstances.GetUniqueValues(dataPointName));
            AppendArffAttribute(new ArrayList<String>(uniqueValues), dataPointName, outFile);
        }

        Log.Debug("Appending ARFF attributes for dependent variable");
        if (includeDependentVariable)
            AppendArffAttribute(Singletons.InstanceVault.DependentVariableOptions, Settings.DEPENDENT_VARIABLE_NAME, outFile);

        outFile.write("\n@data");

        Log.Debug("Creating ARFF output text object");
        for (String instanceID : _instanceIDs)
        {
			ArrayList<String> dataValues = Singletons.InstanceVault.IndependentVariableInstances.GetDataPointValues(instanceID, _dataPointNames);
			
			for (String x : dataValues)
				if (x == null)
				{
					Log.Exception("null value found!");
					Log.Exception(_dataPointNames);
					Log.ExceptionFatal(dataValues);
				}

			outFile.write("\n" + ListUtilities.Join(dataValues, ","));

            if (includeDependentVariable)
                outFile.write("," + GetDependentVariableValue(instanceID));
        }
        
        outFile.close();
    }

    private void AppendArffAttribute(ArrayList<String> values, String dataPointName, PrintWriter outFile) throws Exception
    {
        outFile.write("@attribute " + dataPointName + " ");

        if (DataTypeUtilities.HasOnlyBinary(values))
            outFile.write("{" + ListUtilities.Join(ListUtilities.SortStringList(values), ",") + "}");
        else
        {
            if (DataTypeUtilities.HasOnlyNumeric(values))
                outFile.write("real");
            else
            {
                outFile.write("{" + ListUtilities.Join(ListUtilities.SortStringList(values), ",") + "}");
            }
        }
        outFile.write("\n");
    }

    /** This method generates a basic tab-delimited file with variables as rows and instances as columns.
     * @return This instance
     * @throws Exception
     */
    public void CreateTransposedTabDelimitedFile(boolean includeDependentVariable) throws Exception
    {
        PrintWriter outFile = new PrintWriter(new BufferedWriter(new FileWriter(_outFilePath)));
        
        ArrayList<String> headerItems = ListUtilities.CreateStringList(_instanceIDs);
        headerItems.add(0, "");
        outFile.write(ListUtilities.Join(headerItems, "\t") + "\n");

        for (String dataPoint : _dataPointNames)
        {
            ArrayList<String> rowItems = ListUtilities.CreateStringList(dataPoint);

            for (String instanceID : _instanceIDs)
                rowItems.add(Singletons.InstanceVault.IndependentVariableInstances.GetDataPointValue(instanceID, dataPoint));

//            rowItems = ListUtilities.ReplaceAllExactMatches(rowItems, Settings.MISSING_VALUE_STRING, "NA");

            outFile.write(ListUtilities.Join(rowItems, "\t") + "\n");
        }

        if (includeDependentVariable)
        {
            ArrayList<String> rowItems = ListUtilities.CreateStringList(Settings.DEPENDENT_VARIABLE_NAME);

            for (String instanceID : _instanceIDs)
                rowItems.add(Singletons.InstanceVault.DependentVariableInstances.get(instanceID));

            outFile.write(ListUtilities.Join(rowItems, "\t") + "\n");
        }

        outFile.close();
    }

    /** This method generates a tab-delimited file with variables as columns and instances as rows.
     * @param includeInstanceIDs Whether to include the ID of each instance in the file
     * @return This instance
     * @throws Exception
     */
    public AnalysisFileCreator CreateTabDelimitedFile(boolean includeDependentVariable) throws Exception
    {
        ArrayList<String> headerDataPoints = ListUtilities.CreateStringList(_dataPointNames);
        
        if (includeDependentVariable)
            headerDataPoints.add(Settings.DEPENDENT_VARIABLE_NAME);
    	
        PrintWriter outFile = new PrintWriter(new BufferedWriter(new FileWriter(_outFilePath)));

        outFile.write("\t" + ListUtilities.Join(headerDataPoints, "\t") + "\n");

        for (String instanceID : _instanceIDs)
        {
            ArrayList<String> values = Singletons.InstanceVault.IndependentVariableInstances.GetDataPointValues(instanceID, _dataPointNames);

            if (includeDependentVariable)
                values.add(GetDependentVariableValue(instanceID));

            //values = ListUtilities.ReplaceAllExactMatches(values, Settings.MISSING_VALUE_STRING, "NA");

            outFile.write(instanceID + "\t" + ListUtilities.Join(values, "\t") + "\n");
        }
        
        outFile.close();

        return this;
    }
}
