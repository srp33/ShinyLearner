package shinylearner.dataprocessors;

import java.util.ArrayList;

import shinylearner.core.DataInstanceCollection;
import shinylearner.helper.BigFileReader;
import shinylearner.helper.ListUtilities;

/** This class enables the user to import data directly from delimited (for example, by tabs or commas) text files. This class ignores the final column in the file (which it assumes contains the dependent variable values). The default delimiter is a tab.
 * @author Stephen Piccolo
 */
public class DelimitedDataProcessor extends AbstractDataProcessor
{
    private String _filePath;
    private String _delimiter;

    public DelimitedDataProcessor(String filePath, String delimiter)
    {
        _filePath = filePath;
        _delimiter = delimiter;
    }

    @Override
    public DataInstanceCollection ParseInputData() throws Exception
    {
    	DataInstanceCollection dataInstances = new DataInstanceCollection();
    	
        BigFileReader reader = new BigFileReader(_filePath);
        
        ArrayList<String> dataPointNames = ListUtilities.CreateStringList(reader.ReadLine().split(_delimiter));

        // Remove name of first column because it should be ignored
        dataPointNames.remove(0);
        
        // Trim the last column name
        int lastIndex = dataPointNames.size() - 1;
		dataPointNames.set(lastIndex, dataPointNames.get(lastIndex).trim());
        
        for (String line : reader)
        {
        	ArrayList<String> rowValues = ListUtilities.CreateStringList(line.trim().split(_delimiter));
        	String instanceID = rowValues.remove(0);
        	
            for (int j=0; j<rowValues.size(); j++)
				dataInstances.Add(dataPointNames.get(j), instanceID, rowValues.get(j));
        }
        
        reader.Close();

        return dataInstances;
    }
}