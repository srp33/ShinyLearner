package shinylearner.dataprocessors;


/** This abstract class coordinates all tasks required to parse raw data, transform the data, and describe the data. This class takes care of the generic functionality to accomplish these tasks yet allows the user to develop custom classes that inherit from this class.
 *
 * @author Stephen Piccolo
 */
public abstract class AbstractDataProcessor
{
	public String DataFilePath = null;
	
    public void ParseInputData(String dataSource) throws Exception
    {
        throw new Exception("Not implemented");
    }
}