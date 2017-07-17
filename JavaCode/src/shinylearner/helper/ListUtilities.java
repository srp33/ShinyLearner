package shinylearner.helper;

import java.util.*;

/** This class contains helper methods for dealing with Java collections and lists. Many of these implement functionality that circumvents some of the awkwardness and verbostity of dealing with lists in Java.
 * @author Stephen Piccolo
 */
public class ListUtilities
{
    /** Converts an array of String objects to a list of String objects.
     *
     * @param values Array of String objects
     * @return List of String objects
     */
    public static ArrayList<String> CreateStringList(String... values)
    {
        ArrayList<String> results = new ArrayList<String>();
        if (values.length > 0)
            Collections.addAll(results, values);
        return results;
    }

    /** Converts a generic collection of objects into a list of String objects.
     *
     * @param values Collection of objects
     * @return List of String objects
     */
    public static ArrayList<String> CreateStringList(Collection<String> values)
    {
        ArrayList<String> results = new ArrayList<String>();

        for (Object value : values)
            results.add(String.valueOf(value));

        return results;
    }
    
    /** Finds the intersection between two lists of String objects.
     *
     * @param list1 First list
     * @param list2 Second list
     * @return Intersection list (contains values that exist in both lists)
     */
    public static ArrayList<String> Intersect(ArrayList<String> list1, ArrayList<String> list2)
    {
        if (list1.size() == 0)
            return list2;

        Set<String> intersection = new HashSet<String>(list1);
        intersection.retainAll(new HashSet<String>(list2));
        return new ArrayList<String>(intersection);
    }

    /** This method converts a list of String objects to a single String representation and inserts a delimiter between each object.
     * 
     * @param list List of String objects
     * @param delimiter Delimiter
     * @return Formatted String representation
     */
    public static String Join(ArrayList<String> list, String delimiter)
    {
        if (list.isEmpty())
            return "";

        StringBuilder sb = new StringBuilder();

        for (String x : list)
            sb.append(x + delimiter);

        sb.delete(sb.length() - delimiter.length(), sb.length());

        return sb.toString();
    }

    /** Convenience methods that makes it easier to sort a collection
     *
     * @param list Collection to sort
     * @return Sorted list
     */
    public static ArrayList<String> Sort(Collection<String> list)
    {
        ArrayList<String> newList = new ArrayList<String>(list);
        Collections.sort(newList);
        return newList;
    }

    /** Convenience methods that makes it easier to sort a String list
     *
     * @param list List to sort
     * @return Sorted list
     */
	public static ArrayList<String> SortStringList(ArrayList<String> list)
    {
    	return (ArrayList<String>)Sort(list);
    }
}