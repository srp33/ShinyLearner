package shinylearner.dataprocessors;

import java.util.ArrayList;

import shinylearner.core.Singletons;
import shinylearner.helper.BigFileReader;
import shinylearner.helper.ListUtilities;

/** This class enables the user to import data directly from delimited (for example, by tabs or commas) text files. This class ignores the final column in the file (which it assumes contains the dependent variable values). The default delimiter is a tab.
 * @author Stephen Piccolo
 */
public class TransposedDelimitedDataProcessor extends AbstractDataProcessor
{
    private String _delimiter;

    public TransposedDelimitedDataProcessor(String filePath, String delimiter)
    {
        DataFilePath = filePath;
        _delimiter = delimiter;
    }

    @Override
    public void ParseInputData(String dataSource) throws Exception
    {
        BigFileReader reader = new BigFileReader(DataFilePath);
        
        ArrayList<String> instanceIDs = ListUtilities.CreateStringList(reader.ReadLine().split(_delimiter));
        
        // Remove name of first column because it should be ignored
        instanceIDs.remove(0);
        
        // Trim the last column name
        int lastIndex = instanceIDs.size() - 1;
        instanceIDs.set(lastIndex, instanceIDs.get(lastIndex).trim());
        
        for (String line : reader)
        {
        	ArrayList<String> rowValues = ListUtilities.CreateStringList(line.trim().split(_delimiter));
        	String dataPointName = rowValues.remove(0);
        	
            for (int j=0; j<rowValues.size(); j++)
				Singletons.IndependentVariableInstances.Add(dataSource, dataPointName, instanceIDs.get(j), rowValues.get(j));
        }
        
        reader.Close();
    }
}