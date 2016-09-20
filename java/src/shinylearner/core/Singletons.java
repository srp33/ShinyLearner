package shinylearner.core;

import com.linkedin.paldb.api.StoreReader;
import com.linkedin.paldb.api.StoreWriter;

public class Singletons
{
	public static InstanceVault InstanceVault;
	public static ExperimentItems ExperimentItems = null;
	public static String DatabaseFilePath = null;
	public static StoreWriter DatabaseWriter = null;
	public static StoreReader DatabaseReader = null;
}
