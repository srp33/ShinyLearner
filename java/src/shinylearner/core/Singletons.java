package shinylearner.core;

import java.util.ArrayList;
import java.util.HashMap;

import com.linkedin.paldb.api.StoreReader;
import com.linkedin.paldb.api.StoreWriter;

public class Singletons
{
    public static HashMap<String, String> DependentVariableInstances = new HashMap<String, String>();
    public static ArrayList<String> DependentVariableOptions = new ArrayList<String>();
    public static DataInstanceCollection IndependentVariableInstances = new DataInstanceCollection();
	public static ExperimentItems ExperimentItems = null;
	public static String DatabaseFilePath = null;
	public static StoreWriter DatabaseWriter = null;
	public static StoreReader DatabaseReader = null;
}
